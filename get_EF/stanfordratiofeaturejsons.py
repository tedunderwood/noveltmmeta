#!/usr/bin/env python3

# parsefeaturejsons.py

# Classes and functions that can unpack the extracted feature files
# created by HTRC, and convert them into a .csv that is easier to
# manipulate.

# This version of parsefeaturejsons has been greatly simplified
# in order to simply calculate the proportion of words in a book
# that come from the Stanford list of "hard seeds."

# Example of USAGE:

# run parsefeaturejsons wholevolume ids2pathlist.tsv

import csv, os, sys, bz2, random, json
from collections import Counter

import numpy as np
import pandas as pd

# import utils
import SonicScrewdriver as utils

stanford = set()
with open('stanford.csv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split(',')
        if fields[1] == 'hard':
            stanford.add(fields[0])

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

    if token == "I":
        return [token.lower()]
        # uppercase I is not usually a roman numeral!

    token = token.lower()

    if len(token) < 1:
        return [token]
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

        global stanford

        if volumepath.endswith('bz2'):
            with bz2.open(volumepath, mode = 'rt', encoding = 'utf-8') as f:
                thestring = f.read()
        else:
            with open(volumepath, encoding = 'utf-8') as f:
                thestring = f.read()

        thejson = json.loads(thestring)

        self.volumeid = thejson['id']

        pagedata = thejson['features']['pages']


        self.allcounts = 0
        self.stanfordcounts = 0

        for thispage in pagedata:

            bodywords = thispage['body']['tokenPosCount']
            for token, partsofspeech in bodywords.items():

                lowertoken = token.lower()

                normaltokenlist = normalize_token(lowertoken)

                # Notice that we treat each word as a list, to permit
                # counting both parts of a hyphenated word.
                # But usually this will be a list of one.

                for normaltoken in normaltokenlist:

                    for part, count in partsofspeech.items():
                        self.allcounts += count
                        if normaltoken in stanford:
                            self.stanfordcounts += count


            headerwords = thispage['header']['tokenPosCount']
            for token, partsofspeech in headerwords.items():
                lowertoken = token.lower()
                normaltokenlist = normalize_token(lowertoken)

                for normaltoken in normaltokenlist:

                    for part, count in partsofspeech.items():
                        self.allcounts += count
                        if normaltoken in stanford:
                            self.stanfordcounts += count

            # You will notice that I treat footers (mostly) as part of the body
            # Footers are rare, and rarely interesting.

            footerwords = thispage['footer']['tokenPosCount']
            for token, partsofspeech in footerwords.items():
                lowertoken = token.lower()
                normaltokenlist = normalize_token(lowertoken)

                for normaltoken in normaltokenlist:

                    for part, count in partsofspeech.items():
                        self.allcounts += count
                        if normaltoken in stanford:
                            self.stanfordcounts += count

        # We are done with the __init__ method for this volume.

if __name__ == "__main__":

    args = sys.argv

    # The root path where volumes are stored is hard-coded here:

    rootpath = '/Volumes/TARDIS/work/ef/fic/'

    # You will need to change that if you're using it on your own machine.

    translations = dict()

    with open('../data/filename_translator.tsv', encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            translations[row['badname']] = row['goodname']

    metasource = pd.read_csv(args[1], sep = '\t')

    outputfile = args[2]

    if not os.path.isfile(outputfile):
        with open(outputfile, mode = 'w', encoding = 'utf-8') as f:
            f.write('docid\tallwords\tstanfordwords\n')

    missing = 0

    docstoprocess = metasource.docid

    for idx, docid in enumerate(docstoprocess):

        if idx % 100 == 1:
            print(idx)

        if docid in translations:
            docid = translations[docid]

        path, postfix = utils.pairtreepath(docid, '')
        inpath = rootpath + path + postfix + '/' + utils.clean_pairtree(docid) + '.json.bz2'

        if os.path.isfile(inpath):
            vol = VolumeFromJson(inpath, docid)
            with open(outputfile, mode = 'a', encoding = 'utf-8') as f:
                f.write(docid + '\t' + str(vol.allcounts) + '\t' + str(vol.stanfordcounts) + '\n')
        elif 'uc1.b' in docid:
            newdoc = docid.replace('uc1.b', 'uc1.$b')
            path, postfix = utils.pairtreepath(newdoc, '')
            inpath = rootpath + path + postfix + '/' + utils.clean_pairtree(newdoc) + '.json.bz2'
            if os.path.isfile(inpath):
                vol = VolumeFromJson(inpath, docid)
                with open(outputfile, mode = 'a', encoding = 'utf-8') as f:
                    f.write(newdoc + '\t' + str(vol.allcounts) + '\t' + str(vol.stanfordcounts) + '\n')
                translations[docid] = newdoc
        else:
            missing += 1
            print(missing, inpath, 'not found.')
            with open(outputfile, mode = 'a', encoding = 'utf-8') as f:
                f.write(docid + '\t\t\n')


    with open('../data/filename_translator.tsv', mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = ['badname', 'goodname'])
        writer.writeheader()
        for k, v in translations.items():
            r = dict()
            r['badname'] = k
            r['goodname'] = v
            writer.writerow(r)





