#!/usr/bin/env python3

# generate_path_list.py

# This script takes a list of metadata files as
# arguments. It takes the contents of the 'docid'
# columns from those files, and finds matching
# paths in the HathiTrust extracted feature
# database.

# Then it prints the list of paths in a form
# that can be used to download (rsync) the
# extracted features for those volumes.

# If it can't find certain volumes,
# it reports the title and author
# of the missing volumes.

# USAGE is:
# python3 generate_path_list.py file1.csv file2.csv etc.

# import utils

import os, sys

currentdir = os.path.dirname(__file__)
libpath = os.path.join(currentdir, '../../lib')
sys.path.append(libpath)

import pandas as pd
import SonicScrewdriver as utils

args = sys.argv

list_of_dataframes = []
idset = set()

list_of_files = args[1:]
root = '../'
list_of_paths = [root + x for x in list_of_files]

for p in list_of_paths:
    df = pd.read_csv(p, index_col = 'docid', sep = '\t')
    list_of_dataframes.append(df)
    idset = idset | set(df.index)

ids = []
for anid in idset:
    ids.append(utils.clean_pairtree(str(anid)))

allpaths = set()
with open('/Volumes/TARDIS/work/ef/htrc-ef-all-files.txt', encoding = 'utf-8') as f:
    for line in f:
        line = line.strip()
        allpaths.add(line)

missing = set()
found = set()
mapping = dict()
path2id = dict()

already = set()

for anid in ids:
    if anid in already:
        continue
    path, postfix = utils.pairtreepath(anid, '')
    totalpath = path + postfix + '/' + utils.clean_pairtree(anid) + '.json.bz2'
    if totalpath not in allpaths:
        newid = anid.replace('uc1.b', 'uc1.$b')
        path, postfix = utils.pairtreepath(newid, '')
        totalpath = path + postfix + '/' + utils.clean_pairtree(newid) + '.json.bz2'
        if totalpath in allpaths:
            mapping[anid] = newid
            found.add(totalpath)
            path2id[totalpath] = anid
        else:
            missing.add(anid)
    else:
        found.add(totalpath)
        path2id[totalpath] = anid


with open('ids2pathlist.tsv', mode = 'w', encoding = 'utf-8') as f:
    for path, anid in path2id.items():
        f.write(anid + '\t' + path + '\n')

with open('justpathlist.txt', mode = 'w', encoding = 'utf-8') as f:
    for path, anid in path2id.items():
        f.write(path + '\n')







