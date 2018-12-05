import csv

import pandas as pd

manual = pd.read_csv('/Users/tunder/Dropbox/python/noveltmmeta/manuallists/manual_title_subset.tsv', sep = '\t')
weighted = pd.read_csv('/Users/tunder/Dropbox/python/noveltmmeta/manuallists/weighted_subset.tsv', sep = '\t')

all_ids = set(manual.docid).union(set(weighted.docid))

print(len(all_ids))

holding = all_ids
all_ids = set()

for h in holding:
    if ':/' in h:
        h = h.replace(':', '+')
        h = h.replace('/', '=')
    all_ids.add(h)

rows = []
found = set()

with open('../../data/featurematrix.csv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.split(',')
        if fields[0] == 'docid':
            header1 = line
        elif fields[0] in all_ids:
            rows.append(line)
            found.add(fields[0])

with open('/Volumes/TARDIS/work/ef/ficmatrix/featurematrix1.csv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.split(',')
        if fields[0] == 'docid':
            header2 = line
        elif fields[0] in all_ids:
            rows.append(line)
            found.add(fields[0])

if header1 != header2:
    print('error')

print(len(rows))

with open('samplematrix.csv', mode = 'w', encoding = 'utf-8') as f:
    f.write(header1)
    for r in rows:
        f.write(r)

print(all_ids - found)


