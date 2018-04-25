#!/usr/bin/env python3

# merge_sources_to_master.py

# Loads three sources; normalizes author names; retains only columns present
# in all sources; concatenates them to create a master fiction metadata file.

import numpy as np
import pandas as pd
import random, sys, os, csv

# import utils
currentdir = os.path.dirname(__file__)
libpath = os.path.join(currentdir, '../lib')
sys.path.append(libpath)

import SonicScrewdriver as utils

csv.field_size_limit(sys.maxsize)
# cause some of those fields are long

autherrors = 0

def normalize_author(author):
    '''
    We try to ensure that the author's last name is the first
    word in the 'author' field. The most common problem is that
    the full names provided to spell out initials may come first
    in the field.
    '''
    global autherrors
    delim = "), "

    if author is None or type(author) == float:
        return ''

    if not author.startswith('('):
        return author.strip(',. ')
    else:
        if not delim in author:
            if ")," in author:
                parts = author.split('),')
            else:
                autherrors += 1
                return author.strip(',. ')
        else:
            parts = author.split(delim)

        firstpart = parts[1].strip('., ')
        name = firstpart + " " + parts[0] + ")"
        return name

pre = pd.read_csv('enrichedpre1923ficmeta.tsv', sep = '\t', index_col = 'docid')
post = pd.read_csv('incopyrightfiction.csv', index_col = 'docid')
oa = pd.read_csv('../oasupplement/new_oa_fiction.tsv', sep = '\t', index_col = 'docid')

precols = set(pre.columns)
postcols = set(post.columns)

pre.drop(axis = 1, labels = list(precols-postcols), inplace = True)
post.drop(axis = 1, labels = list(postcols-precols), inplace = True)

oacols = set(oa.columns)

oatodrop = oacols - precols.intersection(postcols)

oa.drop(axis = 1, labels = oatodrop, inplace = True)

merged = pd.concat([pre, post, oa])

merged['author'] = merged['author'].map(normalize_author)

# We drop rows that have the same docid. This is not really
# deduplication, just error control.

dedup = merged[~merged.index.duplicated(keep = 'first')]

dedup.to_csv('mergedficmetadata.tsv', sep = '\t')





