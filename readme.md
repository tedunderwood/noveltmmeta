NovelTM Metadata for English-Language Fiction, 1700-2009
========================================================

Metadata for 210,305 volumes in HathiTrust that have been identified as likely to contain English-language fiction. A full guide to this repository is under submission at *The Journal of Cultural Analytics.*

Ted Underwood, Patrick Kimutis, and Jessica Witte

The [metadata itself](https://github.com/tedunderwood/noveltmmeta/tree/master/metadata)
-------------------

The dataset we have created is multifaceted. Instead of offering a single list of volumes, we provide seven lists constructed in different ways. Researchers can choose the list most suited to their needs--or, better still, choose several lists, in order to compare results.

All seven lists can be found in the **/metadata** subdirectory. They are tab-separated tables in UTF-8 encoding.

All this metadata is drawn ultimately from HathiTrust, and keyed to volume IDs in that library. But we have made an effort to standardize some columns (e.g. author name), so they may not correpond precisely to the values in Hathi. Many new columns have also been added, either through inference from the original metadata, or (in three cases) by manually adding new information.

Subdirectories
==============

The code we used to create the metadata has been archived in subdirectories, so that researchers can understand where this information is coming from.

However, please note that this is not a situation where you can simply push a button and expect to re-run the entire pipeline. That definitely will not work. This was a several-year process; there was a lot of manual intervention along the way, and files had to be renamed and moved at the end for reasons of expository clarity, which broke a lot of path names in earlier scripts. Please understand the code as documentation of what we did, not as a reproducible workflow. To be honest, "reproducing" this project would involve several years of labor; you'd be better off just making your own dataset and comparing it to our results.

eda
-------
Ipython notebooks doing some exploratory analysis on the manually corrected data, and producing figures that were used in the report.

makemaster
----------

Describes the process used to construct the largest dataset: volumemeta.tsv.

dedup
-----

Contains code documenting the deduplication process that moved us from the largest list (volumemeta) down to recordmeta and titlemeta.

manuallists
-----------

Documents the process that produced smaller, manually checked subsets (the manual_title_subset, gender_balanced_subset, and frequently_reprinted_subset).


get_EF
------

Code used to download extracted features, which were used as part of the dedup process, in order to decide when two volumes (or records) were so similar as to be probably "the same work." I have not stored the extracted-feature data itself in the repo; it comes to several gigabytes.

