Fiction metadata
================

This repository gives NovelTM a place to coordinate our work on metadata for English-language fiction.

The metadata itself
--------------------

There are three lists, each with a different level of deduplication / consolidation. All this metadata is drawn ultimately from HathiTrust, and keyed to volume IDs in that library. But an effort is made to standardize some columns (e.g. author name), and certain new columns are added.

The biggest dataset is **masterficmetadata.tsv**, which contains a list of 210,305 volumes of fiction from HathiTrust Digital Library, 1700 - 2010. More precisely, this is a list of volumes *predicted to be fiction*; for the process of genre estimation and associated error, see more detailed discussion in the **/makemaster** directory.

The next is **manifestationmeta.tsv**, which contains 176,650 volumes. This file tries to exclude duplicate copies of *the same reprinting*, using Hathi "record ids" and "volume numbers" to identify duplicate copies. This level of deduplication is roughly equivalent to the "manifestation" level of description [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). Thus the name of the file.

The last is **workmeta.tsv**, which contains 135,325 volumes. This file tries to identify one copy of each fiction "title"--by preference the earliest copy available in Hathi. This is roughly the level of description characterized as "work" [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). Fuzzy matching was used for deduplication; this is an imperfect process, and entails errors documented in the **dedup** folder.

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

bestsellersources
-----------------

A folder containing a range of metadata about bestsellers in England and America.

"reviewed" or "obscure" fiction 1850-1950
-----------------------------------------

Not included in this repo, but see [the file **prestigeficmeta.csv** in the **horizon** repo.](https://github.com/tedunderwood/horizon/tree/master/chapter3/metadata)
