#!/usr/bin/env python3

# gather_oa.py

# COMMENT

import numpy as np
import pandas as pd
import random, sys, os, csv

# import utils
currentdir = os.path.dirname(__file__)
libpath = os.path.join(currentdir, '../../lib')
sys.path.append(libpath)

import SonicScrewdriver as utils

csv.field_size_limit(sys.maxsize)
# cause some of those fields are long

icf = pd.read_csv('../incopyrightfiction.csv', low_memory = False)

icdocs = set(icf.docid)
alreadyhad = 0
errors = 0

files2read = ['new_restricted.tsv', 'new_oa.tsv', 'new_pd_google_1.tsv', 'new_pd_google_2.tsv', 'new_pd_google_3.tsv']

rowlist = []
root = '/Volumes/TARDIS/work/fullmeta/newmeta/'

for filename in files2read:
    print(filename)
    filepath = os.path.join(root, filename)
    with open(filepath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        cols = reader.fieldnames
        for row in reader:
            if row['language'] != 'eng':
                continue

            if row['startdate'] is None:
                errors += 1
                continue

            inferreddate = utils.date_row(row)
            if inferreddate < 1923 or inferreddate > 2017:
                continue

            genres = set(row['genres'].lower().split('|'))
            if 'fiction' not in genres and 'novel' not in genres and 'short stories' not in genres:
                continue

            docid = row['docid']
            if docid in icdocs:
                alreadyhad += 1
                continue
            else:
                row['inferreddate'] = inferreddate
                rowlist.append(row)

cols.insert(7, 'inferreddate')

with open('new_oa_fiction.tsv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, delimiter = '\t', fieldnames = cols)
    writer.writeheader()
    for row in rowlist:
        writer.writerow(row)

print(alreadyhad)
print(errors)


