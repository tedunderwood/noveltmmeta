#!/usr/bin/env python3

# bad_id_tester.py

import csv, os, sys
from collections import Counter

import numpy as np
import pandas as pd

# import utils
import SonicScrewdriver as utils

# USAGE:
# run bad_id_tester ../recordmeta.tsv

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
            pass
        elif 'uc1.b' in docid:
            newdoc = docid.replace('uc1.b', 'uc1.$b')
            path, postfix = utils.pairtreepath(newdoc, '')
            inpath = rootpath + path + postfix + '/' + utils.clean_pairtree(newdoc) + '.json.bz2'
            if os.path.isfile(inpath):
                translations[docid] = newdoc
            else:
                missing += 1
                print(missing, inpath, 'not found.')
        else:
            missing += 1
            print(missing, inpath, 'not found.')

    with open('../data/filename_translator.tsv', mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = ['badname', 'goodname'])
        writer.writeheader()
        for k, v in translations.items():
            r = dict()
            r['badname'] = k
            r['goodname'] = v
            writer.writerow(r)





