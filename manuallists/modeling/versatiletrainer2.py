#!/usr/bin/env python3

# versatiletrainer.py
#
# A significant refactoring of this module
# by Ted Underwood
# December 2017
#
# The goal of the module is to construct predictive
# models of corpus *subsets*, in a very flexible way.
# This is necessary because my literary-historical
# interest in modeling is very rarely just
# "model everything and see what we get." I usually
# want to model chronological subsets, or experiment
# with different definitions of classes, or apply a
# model trained on subset A to subset B.
#
# Three problems in particular have to be solved:
#
# a) multilabel modeling
#
# I'm likely to have a corpus where each text bears
# several different class tags. The groups of texts
# identified by class tags will often overlap, and this
# can make it tricky to define positive and negative classes
# for a given modeling pass. Our goal is to ensure
# that no volumes with a positive tag are present in
# the negative class. At the same time,
#
# b) balancing distributions across time
#
# It is vital to ensure that the positive and negative
# classes have similar distributions across
# the timeline. Otherwise you will *definitely* get
# a model that is partly a model of language change.
# Other metadata categories (nationality and gender)
# might also need to be balanced across the positive
# and negative classes, if/when possible.
#
# finally, c) holding out authors
#
# If you just treat volumes as individuals and select a
# test set as a random sample, information about authors can
# leak from test into training, and give you unrealistically
# high accuracy. (You're learning to recognize Radcliffe, not
# learning to recognize the Gothic.) To avoid this, we make sure
# that groups of volumes by the same author are always in the same
# "fold" of crossvalidation.
#
# (Note that the success of this strategy depends on a previous
# fuzzy-matching pass across the corpus to make sure that authors
# have precisely the same name in every row, without extra initials
# or commas, etc).


import numpy as np
import pandas as pd
import csv, os, random, sys, datetime, pickle
from collections import Counter
from multiprocessing import Pool
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

import modelingprocess
import metaselector

usedate = False
# Leave this flag false unless you plan major
# surgery to reactivate the currently-deprecated
# option to use "date" as a predictive feature.

# FUNCTIONS GET DEFINED BELOW.

def get_features(wordcounts, wordlist):
    numwords = len(wordlist)
    wordvec = np.zeros(numwords)
    for idx, word in enumerate(wordlist):
        if word in wordcounts:
            wordvec[idx] = wordcounts[word]

    return wordvec

def sliceframe(dataframe, yvals, excludedrows, testrow):
    numrows = len(dataframe)
    newyvals = list(yvals)
    for i in excludedrows:
        del newyvals[i]
        # NB: This only works if we assume that excluded rows
        # has already been sorted in descending order !!!!!!!

    if len(excludedrows) > 0:
        trainingset = dataframe.drop(dataframe.index[excludedrows])

    newyvals = np.array(newyvals)
    testset = dataframe.iloc[testrow]

    return trainingset, newyvals, testset

def normalizearray(featurearray, usedate):
    '''Normalizes an array by centering on means and
    scaling by standard deviations. Also returns the
    means and standard deviations for features, so that
    they can be pickled.
    '''

    numinstances, numfeatures = featurearray.shape
    means = list()
    stdevs = list()
    lastcolumn = numfeatures - 1
    for featureidx in range(numfeatures):

        thiscolumn = featurearray.iloc[ : , featureidx]
        thismean = np.mean(thiscolumn)

        thisstdev = np.std(thiscolumn)

        if (not usedate) or featureidx != lastcolumn:
            # If we're using date we don't normalize the last column.
            means.append(thismean)
            stdevs.append(thisstdev)
            featurearray.iloc[ : , featureidx] = (thiscolumn - thismean) / thisstdev
        else:
            print('FLAG')
            means.append(thismean)
            thisstdev = 0.1
            stdevs.append(thisstdev)
            featurearray.iloc[ : , featureidx] = (thiscolumn - thismean) / thisstdev
            # We set a small stdev for date.

    return featurearray, means, stdevs

def create_vocablist(volspresent, n, vocabpath, forbidden):
    '''
    Makes a list of the top n words in sourcedir, and writes it
    to vocabpath. Notice that we are ranking words by document
    frequency: that is, by the number of documents they occur in.
    '''

    sourcepaths = [x[1] for x in volspresent]
    # volspresent is a list of id, path 2-tuples created by get_volume_lists

    wordcounts = Counter()

    for path in sourcepaths:

        with open(path, encoding = 'utf-8') as f:
            for line in f:
                fields = line.strip().split('\t')
                if len(fields) > 2 or len(fields) < 2:
                    continue
                if fields[1] != 'frequency':
                    word = fields[0]
                    if word not in forbidden and len(word) > 0:
                        wordcounts[word] += 1

    with open(vocabpath, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'docfreq'])
        for word, count in wordcounts.most_common(n):
            writer.writerow([word, count])

    vocabulary = [x[0] for x in wordcounts.most_common(n)]

    return vocabulary

def get_vocablist(vocabpath, volspresent, n, forbidden):
    '''
    Gets the vocablist stored in vocabpath or, alternately, if that list
    doesn't yet exist, it creates a vocablist and puts it there.

    If the list stored in vocabpath has more than n features,
    we only use the top n.
    '''

    if not os.path.isfile(vocabpath):
        vocablist = create_vocablist(volspresent, n, vocabpath, forbidden)

    else:
        vocablist = []
        with open(vocabpath, encoding = 'utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word']
                if word not in forbidden:
                    vocablist.append(word)

        if len(vocablist) > n:
            vocablist = vocablist[0: n]

    return vocablist

def model_call(quintuplets, algorithm):
    '''
    Invokes multiprocessing to distribute n-fold crossvalidation
    simultaneously across multiple threads. Since I'm usually doing this
    on a computer with 12 cores, I set 12 threads.
    '''

    print('Beginning multiprocessing.')
    pool = Pool(processes = 12)

    if algorithm == 'logistic':
        res = pool.map_async(modelingprocess.model_volume_list, quintuplets)
    else:
        res = pool.map_async(modelingprocess.svm_model, quintuplets)

    # After all files are processed, write metadata, errorlog, and counts of phrases.
    res.wait()
    resultlist = res.get()
    pool.close()
    pool.join()
    print('Multiprocessing concluded.')

    return resultlist

def crossvalidate(data, classvector, folds, algorithm, regu_const):
    '''
    Creates a set of tuples that can be sent to a multiprocessing Pool,
    one "quintuplet" for each thread.
    '''
    quintuplets = list()
    foldindices = []
    for fold in folds:
        foldindices, foldids = tuple(zip(*fold))
        foldindices = list(foldindices)
        foldids = list(foldids)
        # we package each fold as a zipped list of numeric-index, id pairs

        aquintuple = data, classvector, foldids, foldindices, regu_const
        quintuplets.append(aquintuple)

    # Now do crossvalidation.
    resultlist = model_call(quintuplets, algorithm)

    assert len(resultlist) == len(folds)

    predictions = dict()
    for results, fold in zip(resultlist, folds):
        assert len(results) == len(fold)
        foldindices, foldids = tuple(zip(*fold))
        for r, volid in zip(results, foldids):
            predictions[volid] = r

    return predictions

def calculate_accuracy(orderedIDs, predictions, classdictionary, verbose):
    '''
    What it says on the tin.
    '''

    truepositives = 0
    truenegatives = 0
    falsepositives = 0
    falsenegatives = 0
    totalcount = 0

    for volid in orderedIDs:

        totalcount += 1

        # The donttrainset contains volids that are *only* ever
        # being predicted, and do not appear in the training set for
        # any fold of crossvalidation.

        # We're not going to count the donttrainset in assessing
        # accuracy during gridsearch, because we're not trying to
        # *optimize* on it.

        probability = predictions[volid]
        realclass = classdictionary[volid]

        if probability > 0.5 and classdictionary[volid] > 0.5:
            truepositives += 1
        elif probability <= 0.5 and classdictionary[volid] < 0.5:
            truenegatives += 1
        elif probability <= 0.5 and classdictionary[volid] > 0.5:
            falsenegatives += 1
        elif probability > 0.5 and classdictionary[volid] < 0.5:
            falsepositives += 1

    print()

    accuracy = (truepositives + truenegatives) / totalcount

    if verbose:
        print('True positives ' + str(truepositives))
        print('True negatives ' + str(truenegatives))
        print('False positives ' + str(falsepositives))
        print('False negatives ' + str(falsenegatives))
        precision = truepositives / (truepositives + falsepositives)
        recall = truepositives / (truepositives + falsenegatives)
        F1 = 2 * (precision * recall) / (precision + recall)
        print("F1 : " + str(F1))

    return accuracy

def gridsearch(featurestart, featureend, featurestep, c_range, masterdata, orderedIDs, folds, algorithm, classdictionary, classvector):
    '''
    Does a grid search cross a range of feature counts and
    C values. The assumption is that we're always taking the top
    x words in the vocabulary.

    Note that the matrix will actually display with the "x axis"
    on the side, and the "y axis" at the bottom. Sorry!
    '''

    showmap = False
    # deactivating at the moment

    xaxis = [x for x in range(featurestart, featureend, featurestep)]
    yaxis = c_range

    xlen = len(xaxis)
    ylen = len(yaxis)
    matrix = np.zeros((xlen, ylen))

    for xpos, variablecount in enumerate(xaxis):
        data = masterdata.iloc[ : , 0 : variablecount]

        for ypos, regu_const in enumerate(yaxis):

            print('variablecount: ' + str(variablecount) + "  regularization: " + str(regu_const))

            predictions = crossvalidate(data, classvector, folds, algorithm, regu_const)

            accuracy = calculate_accuracy(orderedIDs, predictions, classdictionary, False)
            print('Accuracy: ' + str(accuracy))
            print()
            matrix[xpos, ypos] = accuracy

    if showmap:
        plt.rcParams["figure.figsize"] = [9.0, 6.0]
        plt.matshow(matrix, origin = 'lower', cmap = plt.cm.YlOrRd)
        plt.show()

    coords = np.unravel_index(matrix.argmax(), matrix.shape)
    print(coords)
    print(xaxis[coords[0]], yaxis[coords[1]])
    features4max = xaxis[coords[0]]
    c4max = yaxis[coords[1]]

    return matrix, features4max, c4max, matrix.max()

def create_folds(k, orderedIDs, authormatches, classdictionary):
    '''
    Does k-fold crossvalidation. Returns a list of "folds," which will
    be a list of lists [ [], [], [], etc. ],
    where each sublist is a list of two-tuples (), (), ()
    of which the first element is the index of a volume in orderedIDs,
    and the second element the volume ID itself.
    '''

    folds = [[] for x in range(k)]
    # e.g. k == 10 will produce: [[], [], [], [], [], [], [], [], [], []]

    assignedinclass = dict()
    assignedinclass[0] = [0 for x in range(k)]
    assignedinclass[1] = [0 for x in range(k)]

    # we make an effort to keep the classes balanced across folds


    ids_to_distribute = set(orderedIDs)
    nextbin = 0

    randomizedtuples = list(zip(list(range(len(orderedIDs))), orderedIDs))
    random.shuffle(randomizedtuples)

    for i, anid in randomizedtuples:
        if anid in ids_to_distribute:
            classlabel = classdictionary[anid]
            thisclasscounts = assignedinclass[classlabel]
            ascending = sorted(thisclasscounts)
            whichlowest = thisclasscounts.index(ascending[0])

            nextbin = whichlowest

            folds[nextbin].append((i, anid))
            assignedinclass[classlabel][nextbin] += 1
            ids_to_distribute.remove(anid)

            for anotheridx in authormatches[i]:
                if anotheridx == i:
                    continue
                    # for some reason I've made everything a member
                    # of its own authormatch list

                anotherid = orderedIDs[anotheridx]
                folds[nextbin].append((anotheridx, anotherid))
                classlabel = classdictionary[anotherid]
                assignedinclass[classlabel][nextbin] += 1

                if anotherid in ids_to_distribute:
                    ids_to_distribute.remove(anotherid)
                    # but notice, we assign anotherid even if it has already
                    # been assigned elsewhere; all the donottrain volumes
                    # need to be in all folds

    print(assignedinclass[0])
    print(assignedinclass[1])

    return folds

def leave_one_out_folds(orderedIDs, authormatches, classdictionary):
    '''
    Makes folds for leave-one-out crossvalidation.
    '''

    folds = []
    alreadyassigned = set()

    # our strategy is to create folds only if they contain an index
    # not already assigned

    for matchlist in authormatches:
        allassigned = True
        for idx in matchlist:
            if idx not in alreadyassigned:
                allassigned = False

        if not allassigned:
            afold = [(x, orderedIDs[x]) for x in matchlist]
            folds.append(afold)
            for item in matchlist:
                alreadyassigned.add(item)

    # confirm we got everything

    print([len(x) for x in folds])
    print(len(folds))

    assert alreadyassigned == set(range(len(orderedIDs)))

    return folds

def get_classvector(volspresent, classdictionary):
    '''
    Given a vocabulary list, and list of volumes, this actually creates the
    pandas dataframe with volumes as rows and words (or other features) as
    columns.
    '''

    classvector = list()

    for volid in volspresent:

        classflag = classdictionary[volid]
        classvector.append(classflag)

    return classvector

def get_simple_data(sourcefile, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, forbid4positive = {'allnegative'}, forbid4negative = {'allpositive'}, excludebelow = 0, excludeabove = 3000, verbose = False, datecols = ['firstpub'], indexcol = ['docid'], extension = '.tsv', genrecol = 'category', numfeatures = 5000, negative_strategy = 'random', overlap_strategy = 'random',force_even_distribution = False, forbiddenwords = set()):

    ''' Loads metadata, selects instances for the positive and
    negative classes, creates a lexicon if one doesn't
    already exist, and creates a pandas dataframe storing
    texts as rows and words/features as columns. A refactored
    and simplified version of get_data_for_model().
    '''

    holdout_authors = True

    # Keeps works by author X out of the test set when she's in the
    # training set. In production, always run with holdout_authors
    # set to True. The only reason to set it to False is to confirm that
    # this flag is actually making a difference.

    freqs_already_normalized = True

    # By default we assume that frequencies have already been normalized
    # (divided by the total number of words in the volume). This allows us
    # to use some features (like type/token ratio) that would become
    # meaningless if we divided everything by total wordcount. But it means
    # offloading some important feature-engineering decisions to the
    # data prep stage.

    # The following function confirms that the testconditions are legal.

    data = pd.read_csv(sourcefile, index_col = 'docid')

    # Get a list of files.
    volspresent = data.index.tolist()

    metadata = metaselector.load_metadata(metadatapath, volspresent, excludebelow, excludeabove, indexcol = indexcol, datecols = datecols, genrecol = genrecol)

    # That function returns a pandas dataframe which is guaranteed to be indexed by indexcol,
    # and to contain a numeric column 'std_date' as well as a column 'tagset' which contains
    # sets of genre tags for each row. It has also been filtered so it only contains volumes
    # in the folder, and none whose date is below excludebelow or above excludeabove.

    orderedIDs, classdictionary = metaselector.select_instances(metadata, sizecap, tags4positive, tags4negative, forbid4positive, forbid4negative, negative_strategy = negative_strategy, overlap_strategy = overlap_strategy, force_even_distribution = force_even_distribution)

    metadata = metadata.loc[orderedIDs]
    # Limits the metadata data frame to rows we are actually using
    # (those selected in select_instances).

    minimumdate = min(metadata.std_date)
    maximumdate = max(metadata.std_date)

    print()
    print(str(len(orderedIDs)) + " volumes range in date from " + str(minimumdate) + " to " + str(maximumdate) + ".")
    print()

    # We now create an ordered list of id-path tuples.

    vocablist = data.columns.tolist()

    numfeatures = len(vocablist)

    print()
    print("Number of features: " + str(numfeatures))

    # For each volume, we're going to create a list of volumes that should be
    # excluded from the training set when it is to be predicted. More precisely,
    # we're going to create a list of their *indexes*, so that we can easily
    # remove rows from the training matrix.

    authormatches = [ [] for x in orderedIDs]

    # Now we proceed to enlarge that list by identifying, for each volume,
    # a set of indexes that have the same author. Obvs, there will always be at least one.
    # We exclude a vol from it's own training set.

    if holdout_authors:
        for idx1, anid in enumerate(orderedIDs):
            thisauthor = metadata.loc[anid, 'author']
            authormatches[idx1] = list(np.flatnonzero(metadata['author'] == thisauthor))

    for alist in authormatches:
        alist.sort(reverse = True)

    print()
    print('Authors matched.')
    print()

    # I am reversing the order of indexes so that I can delete them from
    # back to front, without changing indexes yet to be deleted.
    # This will become important in the modelingprocess module.

    classvector = get_classvector(orderedIDs, classdictionary)
    data = data.loc[orderedIDs]

    return metadata, data, classvector, classdictionary, orderedIDs, authormatches, vocablist

def get_fullmodel(data, classvector, vocablist, regularization):
    '''
    Instead of crossvalidating (producing multiple models),
    this function runs a single model on the whole set.
    '''

    trainingset = data
    yvals = np.array(classvector)

    newmodel = LogisticRegression(C = regularization)

    stdscaler = StandardScaler()
    stdscaler.fit(trainingset)
    scaledtraining = stdscaler.transform(trainingset)

    newmodel.fit(scaledtraining, yvals)

    coefficients = newmodel.coef_[0] * 100

    coefficientuples = list(zip(coefficients, (coefficients / stdscaler.var_), vocablist))
    coefficientuples.sort()

    return coefficientuples, newmodel, stdscaler

def export_model(modelitself, algorithm, scaler, vocabulary, positive_tags, negative_tags, c, n, modelname, outpath):
    '''
    Creates a dictionary with spots for a scikit-learn model and associated data objects that will
    be needed to apply it to texts. E.g., a vocabulary, which tells you which words occupy which
    columns, and a StandardScaler object, which stores the means and variances needed to normalize
    your data (convert frequencies to z scores). Other useful metadata is also stored; the whole
    dictionary is picked and written to file.
    '''
    model = dict()
    model['vocabulary'] = vocabulary
    model['itself'] = modelitself
    model['algorithm'] = algorithm
    model['scaler'] = scaler
    model['positivelabel'] = positive_tags
    model['negativelabel'] = negative_tags
    model['c'] = c
    model['n'] = n
    modelname = outpath.split('/')[-1].replace('.pkl', '')
    model['name'] = modelname
    with open(outpath, 'wb') as output:
        pickle.dump(model, output)

def apply_pickled_model(amodelpath, metadata, masterdata, label):
    '''
    Loads a model pickled by the export_model() function above, and applies it to
    a new folder of texts. Returns a pandas dataframe with a new column, alien_model,
    for the predictions created by this model.

    The metapath here will ordinarily be metadata produced by a different model.
    This allows you to correlate logistic and alien_model columns.
    '''

    with open(amodelpath, 'rb') as input:
        modeldict = pickle.load(input)

    vocablist = modeldict['vocabulary']
    algorithm = modeldict['algorithm']
    model = modeldict['itself']
    scaler = modeldict['scaler']
    modelname = modeldict['name']

    standarddata = scaler.transform(masterdata)
    probabilities = [x[1] for x in model.predict_proba(standarddata)]

    # we create a column named for the model
    probabilities = pd.Series(probabilities, index = masterdata.index)
    # we index the results using the volumes we actually found

    metadata[label] = probabilities
    # indexes will automatically align, putting NaN for any vols
    # not found

    return metadata

def tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, positive_tags, negative_tags, modelparams, modelname, outputpath, verbose = True, write_fullmodel = False):
    '''
    This has become the central workhorse class in the module. It takes
    a set of parameters defining positive and negative subsets of a corpus,
    and gathers data for those subsets.

    Then it runs a grid search, modeling the texts using a range of parameters
    defined by modelparams. This involves trying different numbers of features
    while simultaneously varying C. Logistic regression and SVMs are both
    supported as options; the constant C has a different meaning in those two
    algorithms, but the process of tuning parameters is basically analogous.

    After finding the best number of features, and value of C, we run the
    model again using those parameters, to get predicted probabilities
    for volumes. Technically, I suppose we could have saved all
    the predictions from the grid search to avoid this step, but omg, needless
    complexity.

    We also run the model one last time *without* crossvalidation to get
    a list of coefficients and a model object that can be saved to be applied
    to other corpora. For this we invoke get_fullmodel(). We skip crossvalidation
    here in order to get a single model object that reflects the whole training
    set.

    We write coefficients, predictions, and model object to file, using variations
    of the outputpath contained in the "path" tuple.
    '''

    algorithm, k, featurestart, featureend, featurestep, crange = modelparams

    # Create folds for crossvalidation.
    # To request leave-one-out crossvalidation, set k to zero

    if k < 1:
        folds = leave_one_out_folds(orderedIDs, authormatches, classdictionary)
    else:
        folds = create_folds(k, orderedIDs, authormatches, classdictionary)

    matrix, features4max, best_regularization_coef, maxaccuracy = gridsearch(featurestart, featureend, featurestep, crange, masterdata, orderedIDs, folds, algorithm, classdictionary, classvector)

    datasubset = masterdata.iloc[ : , 0 : features4max]

    predictions = crossvalidate(datasubset, classvector, folds, algorithm, best_regularization_coef)
    accuracy = calculate_accuracy(orderedIDs, predictions, classdictionary, verbose)

    print(accuracy, maxaccuracy)
    # those two should be effectively the same

    coefficientuples, fullmodel, scaler = get_fullmodel(datasubset, classvector, vocablist,best_regularization_coef)

    modelpath = outputpath.replace('.csv', '.pkl')
    export_model(fullmodel, algorithm, scaler, vocablist[0 : features4max], positive_tags, negative_tags, best_regularization_coef, len(orderedIDs), modelname, modelpath)

    coefficientpath = outputpath.replace('.csv', '.coefs.csv')
    with open(coefficientpath, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        for triple in coefficientuples:
            coef, normalizedcoef, word = triple
            writer.writerow([word, coef, normalizedcoef])

    if write_fullmodel:
        # If we want to, we can write predictions created by a model
        # trained on all the data.
        standarddata = scaler.transform(datasubset)
        predicted = [x[1] for x in fullmodel.predict_proba(standarddata)]

    else:
        # But the default is to write the crossvalidated predictions.
        predicted = [predictions[x] for x in orderedIDs]

    metadata = metadata.assign(probability = predicted)
    metadata = metadata.assign(realclass = classvector)
    metadata.drop('tagset', axis = 1, inplace = True)
    metadata.to_csv(outputpath)

    return matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef

if __name__ == '__main__':

    # If this class is called directly, it creates a single model using the default
    # settings set below.

    ## PATHS.

    # sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/texts/'
    # extension = '.fic.tsv'
    # metadatapath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/masterficmeta.csv'
    # outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/predictions.csv'

    sourcefolder = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/fromEF'
    extension = '.tsv'
    metadatapath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/snootymeta.csv'
    vocabpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/lexica/snootyreviews.txt'

    ## modelname = input('Name of model? ')
    modelname = 'snootyreviews1850-1950'

    outputpath = '/Users/tunder/Dropbox/GenreProject/python/reception/fiction/results/' + modelname + '.csv'

    # We can simply exclude volumes from consideration on the basis on any
    # metadata category we want, using the dictionaries defined below.

    ## EXCLUSIONS.

    excludeif = dict()
    excludeifnot = dict()
    excludeabove = dict()
    excludebelow = dict()

    ## daterange = input('Range of dates to use in the model? ')
    daterange = '1850,1950'
    if ',' in daterange:
        dates = [int(x.strip()) for x in daterange.split(',')]
        dates.sort()
        if len(dates) == 2:
            assert dates[0] < dates[1]
            excludebelow['firstpub'] = dates[0]
            excludeabove['firstpub'] = dates[1]

    # allstewgenres = {'cozy', 'hardboiled', 'det100', 'chimyst', 'locdetective', 'lockandkey', 'crime', 'locdetmyst', 'blcrime', 'anatscifi', 'locscifi', 'chiscifi', 'femscifi', 'stangothic', 'pbgothic', 'lochorror', 'chihorror', 'locghost'}
    # excludeif['negatives'] = allstewgenres

    sizecap = 600

    # CLASSIFY CONDITIONS

    # We ask the user for a list of categories to be included in the positive
    # set, as well as a list for the negative set. Default for the negative set
    # is to include all the "random"ly selected categories. Note that random volumes
    # can also be tagged with various specific genre tags; they are included in the
    # negative set only if they lack tags from the positive set.

    ## tagphrase = input("Comma-separated list of tags to include in the positive class: ")
    tagphrase = 'elite'
    positive_tags = [x.strip() for x in tagphrase.split(',')]
    ## tagphrase = input("Comma-separated list of tags to include in the negative class: ")
    tagphrase = 'vulgar'

    # An easy default option.
    if tagphrase == 'r':
        negative_tags = ['random', 'grandom', 'chirandom']
    else:
        negative_tags = [x.strip() for x in tagphrase.split(',')]

    # We also ask the user to specify categories of texts to be used only for testing.
    # These exclusions from training are in addition to ordinary crossvalidation.

    print()
    print("You can also specify positive tags to be excluded from training, and/or a pair")
    print("of integer dates outside of which vols should be excluded from training.")
    print("If you add 'donotmatch' to the list of tags, these volumes will not be")
    print("matched with corresponding negative volumes.")
    print()
    ## testphrase = input("Comma-separated list of such tags: ")
    testphrase = ''
    testconditions = set([x.strip() for x in testphrase.split(',') if len(x) > 0])

    datetype = "firstpub"
    numfeatures = 6000
    regularization = .000075
    # "regularization" has become a dummy parameter, superseded by modelparams below
    # numfeatures, likewise, now only sets the ceiling for gridsearch

    paths = (sourcefolder, extension, metadatapath, outputpath, vocabpath)
    exclusions = (excludeif, excludeifnot, excludebelow, excludeabove, sizecap)
    classifyconditions = (positive_tags, negative_tags, datetype, numfeatures, regularization, testconditions)

    c_range = [.00005, .0001, .0003, .0006, .001, .002, .004, .01, .1, 1]

    # c_range = [.001, .002, .004, .01, .1, 1, 3, 6, 9, 12]

    modelparams = 'logistic', 24, 3000, 6000, 200, c_range
    # this is algorithm, k-fold crossvalidation, ftstart, ftend, ftstep, range for C

    matrix, rawaccuracy, allvolumes, coefficientuples = tune_a_model(paths, exclusions, classifyconditions, modelparams)

    print('If we divide the dataset with a horizontal line at 0.5, accuracy is: ', str(rawaccuracy))
    tiltaccuracy = diachronic_tilt(allvolumes, 'linear', [])

    print("Divided with a line fit to the data trend, it's ", str(tiltaccuracy))

