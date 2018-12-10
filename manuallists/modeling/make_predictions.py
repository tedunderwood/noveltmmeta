#!/usr/bin/env python3

# make_predictions.py

# This script actually applies the models trained earlier
# by train_probabilistic_models.py.

# It then adds new columns to recordmeta.tsv, holding the
# probabilities predicted by the models: juvenileprob and
# nonficprob.

# USAGE syntax:

import sys, os, csv, random
import numpy as np
import pandas as pd
import versatiletrainer2 as vt2

manifest = pd.read_csv('../../recordmeta.tsv', sep = '\t', index_col = 'docid')

def add_metafeatures(docid, row, unionmeta):
    ''' This extends a row of textual features by adding three features based on metadata:

    #noveltitle -- the work has "novel" in the title
    #juvaudience -- the work has "juvenile" in its subject or genre descriptors
    #notfiction -- the work is tagged "NotFiction" or "Description and travel"

    These features are a bit less reliable than one might imagine; e.g. tons of works of fiction
    are tagged "not fiction." But they're probably worth using
    '''

    title = unionmeta.loc[docid, 'shorttitle']
    if not pd.isnull(title):
        title = title.lower()
    else:
        title = ''

    subjects = unionmeta.loc[docid, 'subjects']
    if not pd.isnull(subjects):
        subjects = subjects.lower()
    else:
        subjects = ''

    genres = unionmeta.loc[docid, 'subjects']
    if not pd.isnull(genres):
        genres = genres.lower()
    else:
        genres = ''

    if 'novel' in title:
        title = 1
    else:
        title = 0

    if 'juvenile' in genres or 'juvenile' in subjects:
        juv = 1
    elif "children's" in genres or "children's" in subjects:
        juv = 1
    else:
        juv = 0

    notfic = 0
    if 'notfiction' in genres:
        notfic += 1
    if 'description and travel' in subjects:
        notfic += 1

    row = row.strip('\n')
    row = row + ',' + str(title) + ',' + str(juv) + ',' + str(notfic) + '\n'

    return row

frames = []

for g, df in manifest.groupby(np.arange(len(manifest)) // 5000):

    rows = []
    found = set()
    all_ids = set(df.index)

    with open('../../data/featurematrix.csv', encoding = 'utf-8') as f:
        for line in f:
            fields = line.split(',')
            if fields[0] == 'docid':
                header1 = line
            elif fields[0] in all_ids:
                line = add_metafeatures(fields[0], line, df)
                rows.append(line)
                found.add(fields[0])

    with open('/Volumes/TARDIS/work/ef/ficmatrix/featurematrix1.csv', encoding = 'utf-8') as f:
        for line in f:
            fields = line.split(',')
            if fields[0] == 'docid':
                header2 = line
            elif fields[0] in all_ids:
                line = add_metafeatures(fields[0], line, df)
                rows.append(line)
                found.add(fields[0])

    header = header1.strip('\n') + ",#noveltitle,#juvaudience,#notfiction\n"
    with open('holding_data.csv', mode = 'w', encoding = 'utf-8') as f:
        f.write(header)
        for r in rows:
            f.write(r)

    data = pd.read_csv('holding_data.csv', index_col = 'docid')

    newmeta = vt2.apply_pickled_model('output/juvmodel.pkl', df, data, 'juvenileprob')
    newmeta = vt2.apply_pickled_model('output/nonmodel.pkl', df, data, 'nonficprob')

    frames.append(newmeta)

enrichedrecord = pd.concat(frames, sort = False)

enrichedrecord.to_csv('../../enrichedrecordmeta.tsv', index_label = 'docid', sep = '\t')






