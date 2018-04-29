deduplication
=============

Code used in the deduplication process. Mainly Jupyter notebooks for legibility.

**first_deduplication.ipynb** takes the dataset from masterficmeta.tsv to manifestationmeta.tsv, which has one copy of each volume (counting multiple reprintings as separate volumes). It also does some standarization of author names, and in the process produces **authorgroups.tsv**, recording names taken to be "the same person."

**second_deduplication.ipynb** takes the dataset from manifestationmeta.tsv to workmeta.tsv, which aspires to have one copy of each "work" or "title." In the process, a lot of questionable decisions have to be made, and those decisions are memorialized in **dubiouscalls.txt** and **ignoredgroups.tsv.**
