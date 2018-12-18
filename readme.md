NovelTM Metadata for English-Language Fiction, 1700-2009
========================================================

Metadata for 210,305 volumes in HathiTrust that have been identified as likely to contain English-language fiction. A full guide to this repository is under submission at *The Journal of Cultural Analytics.*

Ted Underwood, Patrick Kimutis, and Jessica Witte

The metadata
-------------

The dataset we have created is multifaceted. Instead of offering a single list of volumes, we provide seven lists constructed in different ways. Researchers can choose the list most suited to their needs--or, better still, choose several lists, in order to compare results.

All seven lists can be found in the **/metadata*** subdirectory. They are tab-separated tables in UTF-8 encoding.

All this metadata is drawn ultimately from HathiTrust, and keyed to volume IDs in that library. But we have made an effort to standardize some columns (e.g. author name), so they may not correpond precisely to the values in Hathi. Many new columns have also been added, either through inference from the original metadata, or (in three cases) by manually adding new information.

Subdirectories
==============

dedup
-----

Contains code documenting the deduplication process.

makemaster
----------

Describes the process used to construct masterfictionmetadata.tsv. This folder also includes several source files covering shorter segments of the timeline; I may have referenced these in other repositories.

oasupplement
------------

Code and data used to catch works of fiction after 1922 but not in copyright.

get_EF
------

Code used to download extracted features, which were used as part of the dedup process, in order to decide when two volumes (or records) were so similar as to be probably "the same work." I have not stored the extracted-feature data itself in the repo; it comes to several gigs.

bestsellersources
-----------------

A folder containing a range of metadata about bestsellers in England and America.

"reviewed" or "obscure" fiction 1850-1950
-----------------------------------------

Not included in this repo, but see [the file **prestigeficmeta.csv** in the **horizon** repo.](https://github.com/tedunderwood/horizon/tree/master/chapter3/metadata)
