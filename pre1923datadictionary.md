pre1923 data dictionary
========================

A key to the meaning of columns in **pre1923hathifiction.csv.** This file should be in utf-8 and in default pandas csv format; it is the same file [contained on figshare as ficmeta.csv.zip.](https://figshare.com/articles/Page_Level_Genre_Metadata_for_English_Language_Volumes_in_HathiTrust_1700_1922/1279201)

For full metadata records associated with volumes, we refer researchers to [the range of HathiTrust bibliographic services](http://www.hathitrust.org/data). This is a summary version.

**htid:** HathiTrust volume ID. This is an item-level identifier for volumes. IDs used for pairtree storage can come in two different forms; I have provided the ``clean'' versions of the IDs that are legal as filenames~\cite{pairtree}.

**recordid:** This is the HathiTrust record ID; in multivolume works, it may be the same for all volumes.

**oclc:** OCLC number, when available.

**locnum:** Library of Congress call number, when available.

**datetype, startdate, enddate, imprintdate:** The first three of these fields are extracted from [MARC controlfield 008](http://www.loc.gov/marc/archive/2000/concise/ecbd008s.html). The last is extracted from other text fields in MARC.

**place:** Place of publication code, as documented in MARC controlfield 008.

**enumcron:** A field that distinguishes multiple volumes of a single record.

**prob80precise:** The probability that more than 80\% of the pages assigned to the genre in this volume are correctly so assigned.

**genrepages, totalpages:** The number of pages in the relevant genre, and the total number of pages in the volume.
