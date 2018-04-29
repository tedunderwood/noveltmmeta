work metadata dictionary
==================================

A key to the meaning of columns in **workmeta.tsv,** a tab-separated tabular file in utf-8 encoding.

This is a list of 135,325 volumes that I believe to contain fiction. It has not been manually checked; it was produced by predictive modeling, and reflects estimated probabilities. Some of these volumes will actually be biography or folklore, for instance. If you have high standards for precision and recall, probably the best approach is to view this as a starting-place for further winnowing.

This file was derived from **manifestmeta.tsv**, and passed through the further deduplication process documented in **dedup/second_deduplication.ipynb**. Basically, the goal was to identify one copy of each fiction "title"--by preference the earliest copy available in Hathi. Fuzzy matching was used for deduplication; this is an imperfect process. So, for instance, I collapsed many copies of *Mary Barton* down to one in 1848. But this dataset still includes another copy in 1993 that bore the full title *Mary Barton, a Tale of Manchester Life*. Fuzzy matching of titles was not sufficient to identify this as "the same book."

Conversely, deduplication will sometimes discard things that ought to be kept. For instance, if you consult **dedup/dubiouscalls.txt** you will notice that I have collapsed *The Bobbsey Twins at Home* and *The Bobbsey Twins at School.* These are presumably different stories, but their titles weren't quite distinct enough to escape the collapsing power of fuzzy-matching. (Many other Bobbsey Twins titles were distinct enough to be preserved.)

Better algorithms can be envisioned; if I get time, I'll improve this by adding textual comparisons between the extracted features for works by the same author. A certain amount of manual standardization of author names (for very prolific authors) would also improve accuracy.

I have roughly aimed for the level of description characterized as "work" [in FRBR](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). Thus the title of the file.

the meanings of columns
-----------------------

These columns are mostly the same as in **masterficmetadata.tsv.** Only three columns have been added:

**instances** The number of copies of this manifestation (recordID + volnum) collapsed in deduplication.

**allcopiesofwork** The number of copies of this work (author + title) collapsed in deduplication.

**copiesin25yrs** The number of copies of this work that were dated within 25 years of the earliest copy in Hathi (which is presumably this copy.)

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
