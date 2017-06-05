in copyright data dictionary
============================

A key to the meaning of columns in **incopyrighthathifiction.csv.** This file should be in utf-8 and in default pandas csv format; it is the same file contained locally on Underwood's hard drive as filteredfiction.csv, and documented more fully in [a separate git repo called hathimetadata](https://github.com/tedunderwood/hathimetadata).

This is a list of 104,043 volumes that I believe to contain fiction. It has not been manually checked; it was produced by predictive modeling, and reflects estimated probabilities. If you have high standards for accuracy, probably the best approach is to view this as a starting-place for further work. 

I have tried to err on the side of inclusiveness. This collection will include many more volumes of fiction than you would get if you relied purely on genre tags in the existing MARC records. But it will also include a certain number of volumes that are better characterized as biography, travel writing, or folklore. 

I have included some of the probabilities calculated by predictive models as columns in the database. This may be useful for researchers who want to define fiction less inclusively: a simple starting-point would be, to filter the dataset by demanding a higher threshold for inclusion on some of these columns.

Note also that this collection *has not been deduplicated.* When there are multiple copies or reprints of a work, it will occur multiple times in this table.

**htid:** HathiTrust volume ID. This is an item-level identifier for volumes. IDs used for pairtree storage can come in two different forms; I have provided the ``clean'' versions of the IDs that are legal as filenames~\cite{pairtree}.

**recordid:** This is the HathiTrust record ID; in multivolume works, it may be the same for all volumes.

**oclc:** OCLC number, when available.

**locnum:** Library of Congress call number, when available.

**datetype, startdate, enddate, imprintdate:** The first three of these fields are extracted from [MARC controlfield 008](http://www.loc.gov/marc/archive/2000/concise/ecbd008s.html). The last is extracted from other text fields in MARC.

**inferreddate**: the date I usually use, extracted from the previous four codes using an algorithm that is documented in the function **infer_date** in [the module **SonicScredriver.py**](https://github.com/tedunderwood/library/blob/master/SonicScrewdriver.py).

Note that **inferreddate** will be reported as **zero** in cases where the algorithm couldn't reliably discern a true date. This is not an ideal way to handle missing data, but this is work in progress.

**place:** Place of publication code, as documented in MARC controlfield 008, to interpret it see the [MARC Code List for Countries.](https://www.loc.gov/marc/countries/)

**enumcron:** A field that distinguishes multiple volumes of a single record.

**subjects** and **geographics** are Library of Congress headings that a cataloger assigned to the work. Geographics indicate that the work is about a specific region.

**genres** are mostly Library of Congress genre/form headings, but this column has also been used to record some flags contained in [character position 33 of Marc field 008](https://www.loc.gov/marc/bibliographic/bd008b.html). You'll notice that in many cases this field states "Not fiction." That reflects the fact that a 0 (not fiction) was entered in this field. The unreliability of existing genre metadata is why I felt I needed to train predictive models.

**rawprobability** The initial probability of being fiction assigned by a model that was contrasting fiction to *everything else in HathiTrust*--i.e., poetry and drama as well as nonfiction

**englishtop1000pct** The fraction of the words in the book drawn from the top 1000 words in an English dictionary sorted by frequency. I used this to weed out works that weren't actually written in English, despite metadata saying they were.

**nonficprob** The probability that this work was nonfiction. The fiction/nonfiction boundary is tricky, so it was useful to train a model specifically for that boundary, leaving aside poetry, drama, etc.

**juvenileprob** I also trained a model to identify juvenile fiction. Volumes with a high probability in this column are set aside in a distinct table.

**metadatalikely** is a flag that is set to TRUE only if there was evidence in the **genres** field, or in the title, suggesting that this work was fiction

**metadatasuspicious** Indicates that there is evidence in the metadata militating against this being fiction. Only a very small number of these volumes are included, and several of those look like errors!
