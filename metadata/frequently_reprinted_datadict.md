frequently reprinted subset
==================================

A key to the meaning of columns in **frequently_reprinted_subset.tsv,** a tab-separated tabular file in utf-8 encoding.

This is a list of 2100 volumes selected by taking volumes with the highest "copiesin25yrs" values in titlemeta.tsv. Specifically, 100 volumes were selected for each year between 1800 and 2009 inclusive.

the meanings of columns:
----------------------------

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

**instances** The number of copies of this manifestation (recordID + volnum) collapsed in deduplication.

**allcopiesofwork** The number of copies of this work (author + title) collapsed in deduplication. For the actual logic of this calculation, see a notebooks called [**final_polish_titlemeta**](https://github.com/tedunderwood/noveltmmeta/blob/master/finalpolish/final_polish_titlemeta.ipynb); to be honest, this aspect of the process got complex and had to be fixed late in the game.

**copiesin25yrs** The number of copies of this work that were dated within 25 years of the earliest copy in Hathi. See above for a notebook that clarifies the calculation.

**enumcron** A field that usually distinguishes multiple volumes of a single record. Sometimes it has other uses.

**volnum** The numeric part of **enumcron,** if it seems to be a volume number.

**title** The full title, as listed in HathiTrust.

**shorttitle** The title, minus certain formatting characters and statements about authorship. *Collected Works* have been replaced by volume-specific titles where possible.

**parttitle** The volume-specific title, where one has been inferred.

**earlyedition** This column reports **True** for volumes where

    **inferreddate** < **latestcomp** + 25

For the most part, this means volumes published within 25 years of their author's lifespan. (Though do sometimes have additional information that allows us to locate a "latest possible date of composition" before the death of the author.)

**nonficprob** The probability this is nonfiction. For the scripts that did the prediction, see [the **modeling** folder](https://github.com/tedunderwood/noveltmmeta/tree/master/manuallists/modeling).

**juvenileprob** The probability this is juvenile fiction. For the scripts that did the modeling, see the link above.
