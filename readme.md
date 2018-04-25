Fiction metadata
================

This repository gives NovelTM a place to coordinate our work on metadata for English-language fiction.

Right now the primary source is **masterficmetadata.tsv**, which contains a list of 210,305 volumes of fiction from HathiTrust Digital Library, 1700 - 2010. More precisely, this is a list of volumes *predicted to be fiction*; for the process of genre estimation and associated error, see more detailed discussion in the **/makemaster** directory.

The columns in **masterficmetadata** are explained in **masterficdatadictionary.md.**

Over the next few months, shorter and more selective lists of fiction will be added. Eventually this whole repo will be frozen in a citable, stable form, and archived in the NovelTM Dataverse.

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
