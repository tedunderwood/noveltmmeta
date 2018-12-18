manifestation metadata dictionary
==================================

A key to the meaning of columns in **manifestationmeta.tsv.** This is a tab-separated tabular file in utf-8 encoding.

This is a list of 176,650 volumes that I believe to contain fiction. It has not been manually checked; it was produced by predictive modeling, and reflects estimated probabilities. Some of these volumes will actually be biography or folklore, for instance. If you have high standards for precision and recall, probably the best approach is to view this as a starting-place for further winnowing.

This file was derived from **masterficmetadata.tsv**, and passed through the deduplication process documented in **dedup/first_deduplication.ipynb**. Author names have been lightly standardized (esp. re: variations of punctuation and initials --> full names) but no effort has been made to collapse multiple reprintings of a book by the same author. Some effort *has* been made to exclude duplicate copies of *the same reprinting*. I used Hathi "record ids" and "volume numbers" to identify duplicate copies; this level of deduplication is roughly equivalent to the "manifestation" level of description [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). Thus the title of the file.

the meanings of columns
-----------------------

These columns are mostly the same as in **masterficmetadata.tsv.** Only one column has been added:

**instances** The number of copies of this volume (of this printing) collapsed in deduplication.

The other columns remain the same:

**docid** HathiTrust volume ID. This is an item-level identifier for volumes. IDs used for [pairtree storage](https://confluence.ucop.edu/display/Curation/PairTree) can come in two different forms; I have provided the "clean" versions of the IDs that are legal as filenames.

**oldauthor** This is the author name as recorded in HathiTrust.

**author** A version of the author name that has undergone some cleaning and standardization. For instance, honorifics like "Sir" and "Mrs" have been moved to the end of the name, as have parenthetical expansions of initials. For more details on the cleaning process, see **makemaster/clean_master.ipynb***, where this column is described as *cleanauth*.

**authordate** Birth and death dates, to the extent that they were available in Hathi.

**inferreddate** The earliest date of publication attested in various MARC date fields. But note, this is a date of publication, not a date of *first* publication. Inference is made by the function **infer_date** in [the module **SonicScredriver.py**](https://github.com/tedunderwood/library/blob/master/SonicScrewdriver.py).

Note that **inferreddate** will be reported as **zero** in cases where the algorithm couldn't reliably discern a true date. This is not an ideal way to handle missing data, but this is work in progress.

**latestcomp** The latest possible date of composition given everything else we know. It will be earlier than inferreddate if we know either 1) the author's date of death or 2) a copyright / first publication date for the title. For this process of inference, see **makemaster/clean_master.ipynb***.

**datetype, startdate, enddate, imprintdate:** The first three of these fields are extracted from [MARC controlfield 008](http://www.loc.gov/marc/archive/2000/concise/ecbd008s.html). The last is extracted from other text fields in MARC.

**imprint** Imprint text stored in MARC.

**contents** usually describe *parts* of the work; these could be individual short stories in a collection, or volumes of a multi-volume *Collected Works*. When possible, I have used this guidance to assign specific titles to volumes.

**subjects** and **geographics** are Library of Congress headings that a cataloger assigned to the work. Geographics indicate that the work is about a specific region.

**genres** are mostly Library of Congress genre/form headings, but this column has also been used to record some flags contained in [character position 33 of Marc field 008](https://www.loc.gov/marc/bibliographic/bd008b.html). You'll notice that in many cases this field states "Not fiction." That reflects the fact that a 0 (not fiction) was entered in this field. The unreliability of existing genre metadata is why I felt I needed to train predictive models.

**oclc:** OCLC number, when available.

**locnum:** Library of Congress call number, when available.

**place:** Place of publication code, as documented in MARC controlfield 008, to interpret it see the [MARC Code List for Countries.](https://www.loc.gov/marc/countries/)

**recordid:** This is the HathiTrust record ID; in multivolume works, it may be the same for all volumes.

**enumcron** A field that usually distinguishes multiple volumes of a single record. Sometimes it has other uses.

**volnum** The numeric part of **enumcron,** if it seems to be a volume number.

**title** The full title, as listed in HathiTrust.

**shorttitle** The title, minus certain formatting characters and statements about authorship. *Collected Works* have been replaced by volume-specific titles where possible.

**parttitle** The volume-specific title, where one has been inferred.
