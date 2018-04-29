June 4, 2017
------------

In addition to a readme, this repository contains a labnotebook file that is just used to record what got done or added. Technically, the git commits are also a record of this, but it can be useful to have a narrative version TU

Tues Apr 24, 2018
-----------

Developed **oasupplement**, because I realized volumes of fiction after 1922 but *not* in copyright would have been neglected by the workflow that produced **incopyrightfiction.csv.**

Wrote **makemaster/enrichpre23.py,** in order to flesh out the **pre1923hathifiction** with more columns from MARC. This produced **makemaster/enrichedpre1923ficmeta.tsv.**

Merged the **oasupplement** with **incopyrightfiction** and **enrichedpre1923ficmeta**, to create **mergedficmetadata,** an intermediate file I have not pushed to repo.

Wed Apr 25, 2018
----------

Built master_cleaning.ipynb to take care of some messy and complicated kinds of data cleaning. This transformed **makemaster/mergedficmeta** into **masterficmeta**.

Sun, April 29, 2018
-------------------

Wrote and ran **dedup/first_deduplication.ipynb** and **dedup/second_deduplication.ipynb.** Spot checked the results (**manifestationmeta** and **workmeta**).

I think the deduplication is pretty good, and probably good-enough, but it hasn't by any means been optimized yet. Need to switch gears right now to a different project, but if I get time, I might run textual comparisons btw all volumes of the same author and use that measurement, along with title comparison, as input to train an actual model making decisions about the similarity cutoff.



