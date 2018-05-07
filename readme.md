Fiction metadata
================

This repository gives NovelTM a place to coordinate our work on metadata for English-language fiction.

The metadata itself
--------------------

There are three lists, each with a different level of deduplication / consolidation. All this metadata is drawn ultimately from HathiTrust, and keyed to volume IDs in that library. But an effort is made to standardize some columns (e.g. author name), and certain new columns are added.

The biggest dataset is **masterficmetadata.tsv**, which contains a list of 210,305 volumes of fiction from HathiTrust Digital Library, 1700 - 2010. More precisely, this is a list of volumes *predicted to be fiction*; for the process of genre estimation and associated error, see more detailed discussion in the **/makemaster** directory.

The next is **manifestationmeta.tsv**, which contains 176,650 volumes. This file tries to exclude duplicate copies of *the same reprinting*, using Hathi "record ids" and "volume numbers" to identify duplicate copies. This level of deduplication is roughly equivalent to the "manifestation" level of description [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). Thus the name of the file.

The last is **workmeta.tsv**, which contains 138,164 volumes. This file tries to identify one copy of each fiction "title"--by preference the earliest copy available in Hathi. This is roughly the level of description characterized as "work" [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). A probabilistic model was used for deduplication; this is an imperfect process, and entails errors documented in [**dedup/second_deduplication.ipynb.**](https://github.com/tedunderwood/noveltmmeta/blob/master/dedup/second_deduplication.ipynb)

Each of the above files comes with an associated "data dictionary" that documents the meanings of columns.

Eventually this whole repo will be frozen in a citable, stable form, and archived in the NovelTM Dataverse.

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
