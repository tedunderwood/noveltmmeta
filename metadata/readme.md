metadata
=========

Three of our lists are very long (138k - 201k volumes). They were created by predictive

The biggest dataset is **masterficmetadata.tsv**, which contains a list of 210,305 volumes of fiction from HathiTrust Digital Library, 1700 - 2010. More precisely, this is a list of volumes *predicted to be fiction*; for the process of genre estimation and associated error, see more detailed discussion in the **/makemaster** directory.

The next is **manifestationmeta.tsv**, which contains 176,650 volumes. This file tries to exclude duplicate copies of *the same reprinting*, using Hathi "record ids" and "volume numbers" to identify duplicate copies. This level of deduplication is roughly equivalent to the "manifestation" level of description [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). Thus the name of the file.

The last is **workmeta.tsv**, which contains 138,164 volumes. This file tries to identify one copy of each fiction "title"--by preference the earliest copy available in Hathi. This is roughly the level of description characterized as "work" [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). A probabilistic model was used for deduplication; this is an imperfect process, and entails errors documented in [**dedup/second_deduplication.ipynb.**](https://github.com/tedunderwood/noveltmmeta/blob/master/dedup/second_deduplication.ipynb)

Each of the above files comes with an associated "data dictionary" that documents the meanings of columns.

Eventually this whole repo will be frozen in a citable, stable form, and archived in the NovelTM Dataverse.
