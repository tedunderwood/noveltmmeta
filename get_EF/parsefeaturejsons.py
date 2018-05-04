#!/usr/bin/env python3

# parsefeaturejsons.py

# Classes and functions that can unpack the extracted feature files
# created by HTRC, and convert them into a .csv that is easier to
# manipulate. In doing this, it can also remove headers,
# normalize spelling, group certain categories of features
# (personal names, place names, days of the week, numbers)
# and calculate some additional features, like #meanwordlength.

# Finally, it's able to divide volumes into chunks, and skip
# a specified number of pages at the front or back of the
# volume before dividing them.

# it expects to have the following files living in the same
# folder:

# SonicScrewdriver.py
# PersonalNames.txt
# PlaceNames.txt
# RomanNumerals.txt
# CorrectionRules.txt
# VariantSpellings.txt

# Note that if you want to run this on your own machine,
# you will need to change the "rootpath," below --
# circa line 470 -- which is the
# folder where we expect to find Extracted Features living.

# Also, you'll need to create a metadata file that pairs
# docids with paths to the features.

# Example of USAGE:

# run parsefeaturejsons wholevolume ids2pathlist.tsv

import csv, os, sys, bz2, random, json
from collections import Counter

import numpy as np
import pandas as pd

# import utils
import SonicScrewdriver as utils

with open('PersonalNames.txt', encoding = 'utf-8') as f:
    personalnames = set([x.strip().lower() for x in f.readlines()])

with open('PlaceNames.txt', encoding = 'utf-8') as f:
    placenames = set([x.strip().lower() for x in f.readlines()])

with open('RomanNumerals.txt', encoding = 'utf-8') as f:
    romannumerals = set([x.strip().lower() for x in f.readlines()])

daysoftheweek = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
monthsoftheyear = {'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'}

# By default, this script does spelling normalization according to
# rules that update archaic spelling and normalize to British where
# practice differs across the Atlantic.

# It also corrects ocr errors.

translator = dict()

with open('CorrectionRules.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

with open('VariantSpellings.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

def slice_list(input_list, number_of_sublists):
    '''
    This function originally written by Paulo Scardini.
    It divides an input_list into number_of_sublists,
    and returns a list of lists.
    '''

    input_size = len(input_list)
    slice_size = input_size // number_of_sublists
    remain = input_size % number_of_sublists
    result = []
    iterator = iter(input_list)

    for i in range(number_of_sublists):
        result.append([])
        for j in range(slice_size):
            result[i].append(iterator.__next__())
        if remain:
            result[i].append(iterator.__next__())
            remain -= 1

    return result

def normalize_token(token):
    ''' Normalizes a token by lowercasing it and by bundling
    certain categories together. Returns a *list* of tokens
    so that we can count the parts of hyphenated words as
    separate words.
    '''

    global personalnames, placenames, daysoftheweek, monthsoftheyear, romannumerals

    if token == "I":
        return [token.lower()]
        # uppercase I is not usually a roman numeral!

    token = token.lower()

    if len(token) < 1:
        return [token]
    elif token[0].isdigit() and token[-1].isdigit():
        return ["#arabicnumeral"]
    elif token in daysoftheweek:
        return ["#dayoftheweek"]
    elif token in monthsoftheyear:
        return ["#monthoftheyear"]
    elif token in personalnames:
        return ["#personalname"]
    elif token in placenames:
        return ["#placename"]
    elif token in romannumerals:
        return ["#romannumeral"]
    elif '-' in token:
        return token.split('-')
        # I never want to treat hyphenated words as distinct
        # features; for modeling it's preferable to count the
        # pieces
    else:
        return [token]

def add_feature(feature, count, features):
    ''' Adds feature-count to a dictionary
    if feature is already in the dictionary.
    '''

    if feature in features:
        features[feature] = count


class VolumeFromJson:

    # A data object that contains page-level wordcounts read from
    # json.

    # It normalizes wordcounts by lower-casing, and by folding certain
    # categories of word together; see normalize_token above.

    # It also includes functions that allow a volume to divide itself
    # according to instructions. E.g.: "volume, cut yourself into
    # three parts, after leaving out certain pages!"

    def __init__(self, volumepath, volumeid):
        '''Initializes a LoadedVolume by reading wordcounts from
        a json file. By default it reads all the pages. But if
        skip-front and skip-back are set to positive values,
        it will skip n pages.'''

        if volumepath.endswith('bz2'):
            with bz2.open(volumepath, mode = 'rt', encoding = 'utf-8') as f:
                thestring = f.read()
        else:
            with open(volumepath, encoding = 'utf-8') as f:
                thestring = f.read()

        thejson = json.loads(thestring)

        self.volumeid = thejson['id']

        pagedata = thejson['features']['pages']

        self.numpages = len(pagedata)
        self.pagecounts = []
        self.totalcounts = Counter()
        self.totaltokens = 0
        self.bodytokens = 0

        self.sentencecount = 0
        self.linecount = 0
        typetokenratios = []

        chunktokens = 0
        typesinthischunk = set()
        # a set of types in the current 10k-word chunk; progress
        # toward which is tracked by chunktokens

        self.integerless_pages = 0
        self.out_of_order_pages = 0
        self.skipped_pages = 0
        compromise_pg = 0

        capitalizedbodytokens = 0

        for i in range(self.numpages):
            thispagecounts = Counter()
            thisbodytokens = 0
            thisheadertokens = 0
            thispage = pagedata[i]

            # There are really two ways of numbering pages. They come in an order,
            # which gives them an inherent ordinality (this is the *first* page). But
            # they also have cardinal *labels* attached, in the "seq" field. These labels
            # are usually, but not necessarily, convertible to integers. (Usually "00000001",
            # but could be "notes.") *Usually* they are == to the ordinal number,
            # but again, not necessarily! The world is full of fun edge cases!

            # In this loop, i is the ordinal page number, and cardinal_page is the cardinal
            # label; its value will be -1 if it can't be converted to an integer.

            # compromise_pg skips pages that have no integer seq, but otherwise
            # proceeds ordinally

            try:
                cardinal_page = int(thispage['seq'])
            except:
                cardinal_page = -1

            if cardinal_page > 0:
                compromise_pg += 1
            elif cardinal_page < 0:
                self.integerless_pages += 1

            if compromise_pg != cardinal_page:
                self.out_of_order_pages += 1

            if cardinal_page >= 0:

                linesonpage = int(thispage['lineCount'])
                sentencesonpage = int(thispage['body']['sentenceCount'])
                self.sentencecount += sentencesonpage
                self.linecount += linesonpage
                # I could look for sentences in the header or footer, but I think
                # that would overvalue accidents of punctuation.

                bodywords = thispage['body']['tokenPosCount']
                for token, partsofspeech in bodywords.items():

                    if token.isalpha() and len(token) > 1 and token[0].isupper():
                        capitalized = True
                    else:
                        capitalized = False

                    # Note that we do not count "I" as a capitalized word, because
                    # length is not > 1.

                    lowertoken = token.lower()
                    typesinthischunk.add(lowertoken)
                    # we do that to keep track of types -- notably, before normalizing

                    normaltokenlist = normalize_token(lowertoken)

                    # Notice that we treat each word as a list, to permit
                    # counting both parts of a hyphenated word.
                    # But usually this will be a list of one.

                    for normaltoken in normaltokenlist:

                        for part, count in partsofspeech.items():
                            thisbodytokens += count
                            chunktokens += count
                            thispagecounts[normaltoken] += count
                            if capitalized:
                                capitalizedbodytokens += count

                            if chunktokens > 10000:
                                typetoken = len(typesinthischunk) / chunktokens
                                typetokenratios.append(typetoken)
                                typesinthischunk = set()
                                chunktokens = 0

                headerwords = thispage['header']['tokenPosCount']
                for token, partsofspeech in headerwords.items():
                    lowertoken = token.lower()
                    normaltokenlist = normalize_token(lowertoken)

                    for normaltoken in normaltokenlist:
                        normaltoken = "#header" + normaltoken

                        for part, count in partsofspeech.items():
                            thisheadertokens += count
                            thispagecounts[normaltoken] += count

                # You will notice that I treat footers (mostly) as part of the body
                # Footers are rare, and rarely interesting.

                footerwords = thispage['footer']['tokenPosCount']
                for token, partsofspeech in footerwords.items():
                    if token.isalpha() and len(token) > 1 and token[0].isupper():
                        capitalized = True
                    else:
                        capitalized = False

                    # Note that we do not count "I" as a capitalized word, because
                    # length is not > 1.
                    lowertoken = token.lower()
                    typesinthischunk.add(lowertoken)
                    # we do that to keep track of types -- notably before normalizing
                    normaltokenlist = normalize_token(lowertoken)

                    for normaltoken in normaltokenlist:

                        for part, count in partsofspeech.items():
                            thisbodytokens += count
                            chunktokens += count
                            thispagecounts[normaltoken] += count
                            if capitalized:
                                capitalizedbodytokens += count

                self.pagecounts.append(thispagecounts)

                for key, value in thispagecounts.items():
                    self.totalcounts[key] += value

                self.totaltokens += thisbodytokens
                self.totaltokens += thisheadertokens
                self.bodytokens += thisbodytokens

            else:
                # print(i, cardinal_page, compromise_pg)
                self.skipped_pages += 1

        if len(typetokenratios) < 1 or chunktokens > 5000:
            # After all pages are counted, we may be left with a
            # chunk of fewer than 10000 words that we could use as further
            # evidence about typetoken ratios.

            # We do this only if we have to, or if the chunk is large
            # enough to make it reasonable evidence.

            chunktokens = chunktokens + 1     # Laplacian correction aka kludge
            typetoken = len(typesinthischunk) / chunktokens

            predictedtt = 4.549e-01 - (5.294e-05 * chunktokens) + (2.987e-09 * pow(chunktokens, 2))
            # That's an empirical quadratic regression on observed data from many genres

            extrapolatedtt =  0.2242 * (typetoken / predictedtt)
            # We infer what typetoken *would* be for a 10k word chunk of this vol, given that it's
            # typetoken for an n-word chunk.

            if extrapolatedtt > 0.6:
                extrapolatedtt = 0.6
            if extrapolatedtt < 0.1:
                extrapolatedtt = 0.1
            # Let's be realistic. We have some priors on the bounds.

            typetokenratios.append(extrapolatedtt)

        self.typetoken = sum(typetokenratios) / len(typetokenratios)
        self.sentencelength = self.bodytokens / (self.sentencecount + 1)
        self.linelength = self.totaltokens / self.linecount
        self.capitalizedbodytokens = capitalizedbodytokens

        # We are done with the __init__ method for this volume.

    def write_volume_features(self, outpaths, folder, override = False, translator = dict(), use_headers = False, skip_front = 0, skip_back = 0):

        ''' This writes volume features while normalizing word frequencies,
        after using a translation table to, for instance, convert American spellings
        to British. It will also divide the volume up into as many parts as it receives
        paths.

        It can be instructed to skip a certain number of pages at the front or back of the volume.
        '''

        numvols = len(outpaths)

        startposition = skip_front
        endposition = len(self.pagecounts) - skip_back

        pagedata = self.pagecounts[startposition: endposition]

        if numvols == 1:
            list_of_pagelists = [pagedata]
        else:
            list_of_pagelists = slice_list(pagedata, numvols)

        metadata_rows = []

        for idx, pagelist in enumerate(list_of_pagelists):

            # Each pagelist corresponds to a file we're going to write,
            # and to a chunk of pages (pagelist).

            thispath = outpaths[idx]

            featuredict = dict()

            # Certain features are global for the entire volume.
            # We could calculate these by chunk, but it would be a
            # pain to do so, and little would be gained. (In truth,
            # these features are rarely crucial.)

            featuredict['#sentencelength'] = self.sentencelength
            featuredict['#typetoken'] = self.typetoken
            featuredict['#pctcapitalized'] = ((self.capitalizedbodytokens * 100) / self.bodytokens)

            # other features need to be summed across pages

            chunkctr = Counter()
            totaltokensinchunk = 0
            listofwordlengths = []

            for page in pagelist:
                for token, count in page.items():
                    if token.startswith('#header') and not use_headers:
                        continue

                    chunkctr[token] += count
                    totaltokensinchunk += count

            for token, count in chunkctr.items():
                if token in translator:
                    token = translator[token]
                # here's where we normalize spelling

                featuredict[token] = count / totaltokensinchunk
                wordlen = len(token)
                listofwordlengths.extend([wordlen] * count)

            featuredict['#meanwordlength'] = sum(listofwordlengths) / len(listofwordlengths)

            if os.path.isfile(thispath) and not override:
                print('Error: you are asking me to override an existing')
                print('file without explicitly specifying to do so in your')
                print('invocation of write_volume_features.')

            with open(thispath, mode = 'w', encoding = 'utf-8') as f:
                writer = csv.writer(f, delimiter = '\t')
                writer.writerow(['feature', 'frequency'])
                for key, value in featuredict.items():
                    if value > 0:
                        writer.writerow([key, value])

            metarow = dict()
            metarow['docid'] = thispath.replace('.tsv', '').replace(folder, '')
            metarow['path'] = thispath
            metarow['totaltokens'] = totaltokensinchunk
            metarow['skipped_pages'] = self.skipped_pages
            metadata_rows.append(metarow)

        return metadata_rows

    def get_volume_features(self, features, override = False, translator = dict(), use_headers = False, skip_front = 0, skip_back = 0):

        ''' This returns a numpy vector of volume features keyed by lexindex,
        after using a translation table to, for instance, convert American spellings
        to British.

        It can be instructed to skip a certain number of pages at the front or back of the volume.
        '''

        startposition = skip_front
        endposition = len(self.pagecounts) - skip_back

        pagelist = self.pagecounts[startposition: endposition]


        # Certain features are global for the entire volume.

        add_feature('#sentencelength', self.sentencelength, features)
        add_feature('#typetoken', self.typetoken, features)
        add_feature('#pctcapitalized', ((self.capitalizedbodytokens * 100) / self.bodytokens), features)

        # other features need to be summed across pages

        totaltokensinchunk = 0
        listofwordlengths = []
        chunkctr = Counter()

        for page in pagelist:
            for token, count in page.items():
                if token.startswith('#header') and not use_headers:
                    continue

                chunkctr[token] += count
                totaltokensinchunk += count

        for token, count in chunkctr.items():
            if token in translator:
                token = translator[token]
            # here's where we normalize spelling!

            frequency = count / totaltokensinchunk
            add_feature(token, frequency, features)
            wordlen = len(token)
            listofwordlengths.extend([wordlen] * count)

        meanwordlen = sum(listofwordlengths) / len(listofwordlengths)
        add_feature('#meanwordlength', meanwordlen, features)

        return features

if __name__ == "__main__":

    args = sys.argv

    # This script can be used in several different ways.
    # It takes two command-line arguments

    # USAGE:
    # python3 parsefeaturejsons division-mode metadata-file

    # where division-mode is either
    #       wholevolume
    #       matrix
    # or    divided

    # If the *matrix* option is selected, a third command-line argument
    # will be needed, because the matrix requires also a lexicon of features
    # to be used as columns of the matrix.

    # Different division modes are possible, but this particular instance of parsefeaturejsons
    # was used for deduplication, and used solely to build a matrix where volumes are
    # represented as rows. So only the *matrix* part of this script
    # has been tested recently.

    # In practice the command used was

    # python3 parsefeaturejsons matrix ../get_EF/ids2paths.tsv fictionfrequencies.tsv

    # The root path where volumes are stored is hard-coded here:

    rootpath = '/Volumes/TARDIS/work/ef/fic/'
    outfolder = '../data/'

    # You will need to change that if you're using it on your own machine.

    if len(args) < 3:
        print('This script requires two command-line arguments:')
        print('a vol-division mode and a metadata file to use.')
        sys.exit(0)

    elif args[1] == 'matrix':
        print('You have selected the matrix option. This will read in all docids')
        print('from the metadata file provided, and create a matrix of feature')
        print('frequencies where each row corresponds to a docid.')

        if len(args) < 4:
            print('This option requires a third command-line argument; a list of')
            print('features to be used in the matrix.')
            sys.exit(0)
        else:
            lexpath = args[3]

        lexicon = []
        ctr = 0
        with open(lexpath, encoding = 'utf-8') as f:
            reader = csv.DictReader(f, delimiter = '\t')
            for row in reader:
                word = row['word']
                if len(word) > 0 and '\t' not in word and word != 'docid':
                    lexicon.append(word)
                    ctr += 1
                    if ctr > 999:
                        break

        featuretemplate = dict()
        for word in lexicon:
            featuretemplate[word] = 0

        missing = []
        path_to_meta = args[2]
        ctr = 0
        meta = pd.read_csv(path_to_meta, dtype = 'object', index_col = 'docid', sep = '\t')

        outfilename = outfolder + 'featurematrix.csv'
        if os.path.isfile(outfilename):
            existingdata = pd.read_csv(outfilename, index_col = 'docid')
            columns = list(existingdata.columns)
            for idx, col in enumerate(columns):
                if col != lexicon[idx]:
                    print('Danger, Will Robinson. The lexicon you are using to read in new')
                    print('files does not align with the column order implied by the existing')
                    print('matrix.\a')
                    sys.exit(0)

            alreadyinmatrix = set(existingdata.index)
        else:
            alreadyinmatrix = set()
            columns = list(lexicon)
            columns.insert(0, 'docid')
            with open(outfilename, mode = 'a', encoding = 'utf-8') as f:
                writer = csv.DictWriter(f, fieldnames = columns)
                writer.writeheader()

        iterations = int(input('Integer number of files to process and add to matrix: '))
        datalist = []

        for index, row in meta.iterrows():

            if index in alreadyinmatrix:
                continue

            inpath = rootpath + row['path']
            ctr += 1

            if ctr > iterations:
                break
            elif ctr % 1000 == 1:
                print(ctr)

            if not os.path.isfile(inpath):
                missing.append(index)
                continue

            vol = VolumeFromJson(inpath, index)
            features = dict(featuretemplate)

            features = vol.get_volume_features(features, override = True, translator = translator, use_headers = False, skip_front = 0, skip_back = 0)

            features['docid'] = index

            datalist.append(features)

        print(len(missing), ' missing volumes.')
        if len(missing) > 0:
            with open('missing_volumes.txt', mode = 'a', encoding = 'utf-8') as f:
                for m in missing:
                    f.write(m + '\n')

        columns = list(lexicon)
        columns.insert(0, 'docid')
        with open(outfilename, mode = 'a', encoding = 'utf-8') as f:
            writer = csv.DictWriter(f, fieldnames = columns)
            for row in datalist:
                writer.writerow(row)

        print('Done\a')

    elif args[1] == 'wholevolume':
        missing = 0
        path_to_meta = args[2]

        meta = pd.read_csv(path_to_meta, dtype = 'object', index_col = 'docid', sep = '\t')

        for index, row in meta.iterrows():
            inpath = rootpath + row['path']
            try:
                vol = VolumeFromJson(inpath, index)
                outpath = '../data/' + utils.clean_pairtree(index) + '.tsv'
                vol.write_volume_features([outpath], folder = '../data/', override = True, translator = translator, use_headers = False, skip_front = 0, skip_back = 0)
            except:
                missing += 1


        print(missing)

    elif args[1] == 'divided':

        path_to_meta = args[2]

        meta = pd.read_csv(path_to_meta, dtype = 'object', index_col = 'docid', sep = '\t')

        all_outrows = []

        for index, row in meta.iterrows():
            inpath = rootpath + row['path']
            vol = VolumeFromJson(inpath, index)

            if vol.bodytokens < 100 or vol.numpages < 10:
                print(index + ' is too short to use.')
                continue
            else:
                skip_front = round(vol.numpages * .03)
                if skip_front < 4:
                    skip_front = 4
                skip_back = round(vol.numpages * .015)
                if skip_back < 2:
                    skip_back = 2

            numvols = next(idx for idx, value in enumerate(cut_points) if value > vol.bodytokens)

            if numvols == 1:
                outpaths = ['../data/' + utils.clean_pairtree(index) + '.tsv']
            else:
                outpaths = []
                for i in range(numvols):
                    outpaths.append('../data/' + utils.clean_pairtree(index) + '_' + str(i) + '.tsv')

            # here we actually do the writing

            part_metadata = vol.write_volume_features(outpaths, override = True, translator = translator, use_headers = False, skip_front = skip_front, skip_back = skip_back,)

            for i, part in enumerate(part_metadata):
                part['htid'] = utils.clean_pairtree(index)
                all_outrows.append(part)

        columns = ['docid', 'htid', 'totaltokens', 'skipped_pages', 'path']
        with open('parsing_metadata_2.tsv', mode = 'w', encoding = 'utf-8') as f:
            scribe = csv.DictWriter(f, fieldnames = columns, delimiter = '\t')
            scribe.writeheader()

            for row in all_outrows:
                scribe.writerow(row)




