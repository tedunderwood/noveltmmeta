NovelTM Datasets for English-Language Fiction, 1700-2009
========================================================

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3766610.svg)](https://doi.org/10.5281/zenodo.3766610)

Metadata for 210,305 volumes in HathiTrust that have been identified as likely to contain English-language fiction.

For a fuller description of this data, see [the accompanying article in the *Journal of Cultural Analytics* by Ted Underwood, Patrick Kimutis, and Jessica Witte.](https://culturalanalytics.org/article/13147-noveltm-datasets-for-english-language-fiction-1700-2009) Levels of error are described statistically in that article. The authors do not plan to correct details in the dataset. This is a snapshot of a particular (imperfect) state of our knowledge circa 2019, not a resource we intend to update and maintain in perpetuity.

The [metadata itself](https://github.com/tedunderwood/noveltmmeta/tree/master/metadata)
-------------------

The dataset we have created is multifaceted. Instead of offering a single list of volumes, we provide seven lists constructed in different ways. Researchers can choose the list most suited to their needs--or, better still, choose several lists, in order to compare results.

All seven lists can be found in the **/metadata** subdirectory. They are tab-separated tables in UTF-8 encoding.

All this metadata is drawn ultimately from HathiTrust, and keyed to volume IDs in that library. But we have made an effort to standardize some columns (e.g. author name), so they may not correpond precisely to the values in Hathi. Many new columns have also been added, either through inference from the original metadata, or (in three cases) by manually adding new information.

Code directiories
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


Other directories
=================

plans
-----
Early draft plans for this project.

missing
-------
Sketches toward a list of titles surprisingly missing in Hathi. May be out of date.

incopyrightpagepredicts
-----------------------
Page-level genre predictions for volumes after 1923. Before 1923, see [the Figshare repository.](https://figshare.com/articles/Page_Level_Genre_Metadata_for_English_Language_Volumes_in_HathiTrust_1700_1922/1279201)

Note that I am not aggressively publicizing page-level data, because I don't yet have any way to ensure that it reflects current page IDs for these volumes. HathiTrust doesn't yet have persistent page identifiers.
