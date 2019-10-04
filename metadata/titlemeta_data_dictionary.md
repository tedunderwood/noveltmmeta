Data dictionary for the title list.
==================================

A key to the meaning of columns in **titlemeta.tsv,** a tab-separated tabular file in utf-8 encoding.

This is a list of 138,164 volumes that we believe to contain fiction. It has not been manually checked; it was produced by predictive modeling, and reflects estimated probabilities. Errors are of two broad kinds. Some volumes are mistakenly included: for instance, some of these volumes will actually be biography or folklore. Some volumes will also have been mistakenly overlooked, either in the initial sweep for fiction, or in the process of deduplication that boiled this down. To understand all the possible sources of error, you might need to consult the code in the **/makemaster** and **/dedup** directories.

This file was derived from **recordmeta.tsv**, and passed through the further deduplication processes documented in **dedup/second_deduplication.ipynb** and **dedup/third_deduplication.ipynb**. Basically, the goal was to identify one copy of each fiction "title"--by preference the earliest copy available in Hathi. Probabilistic modeling was used: this is an imperfect process. So, for instance, I collapsed eight duplicate copies of *Mary Barton* down to one in 1848. But this dataset still includes another copy in 1993 that bore the full title *Mary Barton, a Tale of Manchester Life*. Fuzzy matching of titles, and even volume text, was not sufficient to identify this as "the same book."

However, you can often further reduce duplication by using the **earlyedition** column, which flags books published *within 25 years of the latest possible date of composition for the book*. Usually this means "within 25 years of the author's death.""

the meanings of new columns:
----------------------------

These columns are mostly the same as in **recordmeta.tsv.** Only four columns have been added:

**instances** The number of copies of this manifestation (recordID + volnum) collapsed in deduplication.

**allcopiesofwork** The number of copies of this work (author + title) collapsed in deduplication.

**copiesin25yrs** The number of copies of this work that were dated within 25 years of the earliest copy in Hathi (which is presumably this copy.)

**earlyedition** This column reports **True** for volumes where

    **inferreddate** < **latestcomp** + 25

For the most part, this means volumes published within 25 years of their author's lifespan. (Though do sometimes have additional information that allows us to locate a "latest possible date of composition" before the death of the author.)

Columns shared with masterficmetadata:
--------------------------------------

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

**subjects** and **geographics** are Library of Congress headings that a cataloger assigned to the work. Geographics indicate that the work is about a specific region. Compound subject headings have not always been preserved intact; for instance, a date range is sometimes separated from the noun that it modified.

**genres** are mostly Library of Congress genre/form headings. At an early stage of processing, this column was used to record some flags contained in [character position 33 of Marc field 008](https://www.loc.gov/marc/bibliographic/bd008b.html), but that information was so unreliable and confusing that we removed it from the final release.

**oclc:** OCLC number, when available.

**locnum:** Library of Congress call number, when available.

**place:** Place of publication code, as documented in MARC controlfield 008, to interpret it see the [MARC Code List for Countries.](https://www.loc.gov/marc/countries/)

**recordid:** This is the HathiTrust record ID; in multivolume works, it may be the same for all volumes.

**enumcron** A field that usually distinguishes multiple volumes of a single record. Sometimes it has other uses.

**volnum** The numeric part of **enumcron,** if it seems to be a volume number.

**title** The full title, as listed in HathiTrust.

**shorttitle** The title, minus certain formatting characters and statements about authorship. *Collected Works* have been replaced by volume-specific titles where possible.

**parttitle** The volume-specific title, where one has been inferred.
