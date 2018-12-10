#!/usr/bin/env python3

# main_experiment.py

# USAGE syntax:

# python3 main_experiment.py *command*

import sys, os, csv, random
import numpy as np
import pandas as pd
import versatiletrainer2
import metaselector
from math import sqrt
import matplotlib.pyplot as plt

from scipy import stats

def train_juvmodel():
    sourcefolder = 'samplematrix.csv'
    sizecap = 700

    c_range = [.00001, .0001, .001, .01, 0.1, 1, 10, 100]
    featurestart = 1003
    featureend = 1103
    featurestep = 100
    modelparams = 'logistic', 12, featurestart, featureend, featurestep, c_range
    metadatapath = '../union_of_subsets.csv'

    name = 'juvmodel'
    vocabpath = 'dummyvariable'

    tags4positive = {'juvenile'}
    tags4negative = {'longfiction', 'shortfiction', 'nonfiction', 'poetry', 'drama'}
    floor = 1800
    ceiling = 2011

    metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, excludebelow = floor, excludeabove = ceiling, forbid4positive = {'nothing'}, forbid4negative = {'nothing'}, force_even_distribution = False, negative_strategy = 'random', numfeatures = 7500)

    matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, 'output/' + name + '.csv')

def train_nonmodel():
    sourcefolder = 'samplematrix.csv'
    sizecap = 700

    c_range = [.00001, .0001, .001, .01, 0.1, 1, 10, 100]
    featurestart = 1003
    featureend = 1103
    featurestep = 100
    modelparams = 'logistic', 12, featurestart, featureend, featurestep, c_range
    metadatapath = '../union_of_subsets.csv'

    name = 'nonmodel'
    vocabpath = 'dummyvariable'

    tags4positive = {'notfiction'}
    tags4negative = {'longfiction', 'shortfiction', 'juvenile', 'poetry', 'drama'}
    floor = 1800
    ceiling = 2011

    metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist = versatiletrainer2.get_simple_data(sourcefolder, metadatapath, vocabpath, tags4positive, tags4negative, sizecap, excludebelow = floor, excludeabove = ceiling, forbid4positive = {'nothing'}, forbid4negative = {'nothing'}, force_even_distribution = False, negative_strategy = 'random', numfeatures = 7500)

    matrix, maxaccuracy, metadata, coefficientuples, features4max, best_regularization_coef = versatiletrainer2.tune_a_model(metadata, masterdata, classvector, classdictionary, orderedIDs, authormatches, vocablist, tags4positive, tags4negative, modelparams, name, 'output/' + name + '.csv')

## MAIN

command = sys.argv[1]

if command == "juv":
    train_juvmodel()
if command == "non":
    train_nonmodel()
