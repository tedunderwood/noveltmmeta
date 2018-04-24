#!/usr/bin/env python3

# gather_oa.py

# The goal here is to enrich our metadata for pre-1923 fiction, if possible,

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

ficmeta = dict()

with open('../pre1923hathifiction.csv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        docid = row['htid']
        row['docid'] = docid
        row.pop('htid', None)
        ficmeta[docid] = row

ficset = set(ficmeta.keys())

files2read = ['new_restricted.tsv', 'new_oa.tsv', 'new_pd_google_1.tsv', 'new_pd_google_2.tsv', 'new_pd_google_3.tsv']

root = '/Volumes/TARDIS/work/fullmeta/newmeta/'

founddocs = set()
improved = 0

for filename in files2read:
    print(filename)
    filepath = os.path.join(root, filename)
    with open(filepath, encoding = 'utf-8') as f:
        reader = csv.DictReader(f, delimiter = '\t')
        for row in reader:
            docid = row['docid']
            if docid not in ficset:
                continue

            newauthor = row['author']
            author = ficmeta[docid]['author']

            newtitle = row['title']
            title = ficmeta[docid]['title']

            ficmeta[docid]['authordate'] = row['authordate']
            ficmeta[docid]['contents'] = row['contents']
            ficmeta[docid]['subjects'] = row['subjects']
            ficmeta[docid]['genres'] = row['genres']
            ficmeta[docid]['geographics'] = row['geographics']

            founddocs.add(docid)

            if len(author) < 1 and len(newauthor) > 1:
                improved += 1


            # if newauthor != author:
            #     print('New author: ', newauthor)
            #     print('old author: ', author)
            #     user = input('? ')

            # if newtitle != title:
            #     print('New title: ', newtitle)
            #     print('old title: ', title)
            #     user = input('? ')

            ficmeta[docid]['title'] = newtitle
            ficmeta[docid]['author'] = newauthor
            ficmeta[docid]['inferreddate'] = utils.date_row(row)

fieldnames.insert(13, 'genres')
fieldnames.insert(13, 'geographics')
fieldnames.insert(13, 'contents')
fieldnames.insert(6, 'inferreddate')
fieldnames.insert(5, 'authordate')
fieldnames.pop(0)
fieldnames.insert(0, 'docid')

missing = ficset - founddocs

with open('../enrichedpre1923ficmeta.tsv', mode = 'w', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = fieldnames, delimiter = '\t')
    writer.writeheader()
    for key, row in ficmeta.items():
        if key in missing:
            row['contents'] = ''
            row['genres'] = ''
            row['geographics'] = ''
            row['authordate'] = ''
            row['inferreddate'] = utils.date_row(row)
        writer.writerow(row)

print(improved)





