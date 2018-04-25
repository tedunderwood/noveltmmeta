June 4, 2017
============

In addition to a readme, this repository contains a labnotebook file that is just used to record what got done or added. Technically, the git commits are also a record of this, but it can be useful to have a narrative version TU

Tues Apr 24, 2018
-----------

Developed **oasupplement**, because I realized volumes of fiction after 1922 but *not* in copyright would have been neglected by the workflow that produced **incopyrightfiction.csv.**

Wrote **makemaster/enrichpre23.py,** in order to flesh out the **pre1923hathifiction** with more columns from MARC. This produced **makemaster/enrichedpre1923ficmeta.tsv.**

Merged the **oasupplement** with **incopyrightfiction** and **enrichedpre1923ficmeta**, to create **mergedficmetadata,** an intermediate file I have not pushed to repo.

Wed Apr 25, 2018
----------

Built master_cleaning.ipynb to take care of some messy and complicated kinds of data cleaning. This transformed **makemaster/mergedficmeta** into **masterficmeta**.



