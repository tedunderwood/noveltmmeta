Fiction metadata
================

This repository gives NovelTM a place to coordinate our work on metadata for English-language fiction. Right now it contains mainly two large datasets that include all volumes recognized as "fiction" by an algorithmic sweep through HathiTrust. The nature of the creation process means that these lists incorporate a certain amount of error.

Over the next few months, shorter and more selective lists of fiction will be added. Eventually this whole repo may be frozen in a citable, stable form using Zenodo or (more likely) the NovelTM Dataverse. Right now, the constituent parts (described below) are mostly already available in a stable, citable form.

pre1923hathifiction.csv
-----------------------
Metadata for fiction before 1923. Fiction was identified algorithmically, using methods documented in [Understanding Genre in a Collection of a Million Volumes.](https://figshare.com/articles/Understanding_Genre_in_a_Collection_of_a_Million_Volumes_Interim_Report/1281251)

Column definitions are explained in [**pre1923datadictionary.md**](https://github.com/tedunderwood/noveltmmeta/blob/master/pre1923datadictionary.md)

If you want to cite this as a resource, I would recommend that you consider citing [the stable form on Figshare:](https://figshare.com/articles/Page_Level_Genre_Metadata_for_English_Language_Volumes_in_HathiTrust_1700_1922/1279201) Underwood, Ted (2014): Page-Level Genre Metadata for English-Language Volumes in HathiTrust, 1700-1922. figshare. https://doi.org/10.6084/m9.figshare.1279201.v1

**pre1923hathifiction.csv** is substantively equivalent to **ficmeta.csv.zip** in the Figshare repo. Other files in the repo include page-level metadata.

The work that developed this dataset was funded by an ACLS Digital Innovation Grant, and by the National Endowment of the Humanities Digital Humanities Start-Up Grant,  Award# HD5178713. The views and results expressed don't necessarily reflect the views of the funding agencies.

incopyrighthathifiction.csv
---------------------------
Metadata for HathiTrust fiction in copyright. Fiction was identified algorithmically, using a variant of the strategy mentioned above; code is contained in [the 20c genres repo.](https://github.com/tedunderwood/20cgenres)

Column definitions are explained in [**incopyrightdatadictionary.md**](https://github.com/tedunderwood/noveltmmeta/blob/master/incopyrightdatadictionary.md)

If you want to cite this as a resource, I would recommend citing [the stable form on IDEALS:](https://www.ideals.illinois.edu/handle/2142/97948) Ted Underwood, "A List of English-Language Fiction after 1922 in HathiTrust," IDEALS, 2017, https://www.ideals.illinois.edu/handle/2142/97948.

Page-level metadata for this dataset is in **incopyrightpagepredicts.** It's not organized very well yet, and it's bulky, but it's there.

The work that developed this dataset was funded by SSHRC via the NovelTM project, administered at McGill University, and by the Andrew W. Mellon foundation, via the WCSA+DC project, administered by HathiTrust Research Center. The views and results expressed don't necessarily reflect the views of the funding agencies.

bestsellersources
-----------------

A folder containing a lot of different metadata about bestsellers in England and America.

"reviewed" or "obscure" fiction 1850-1950
-----------------------------------------

Not included in this repo, but see [the file **prestigeficmeta.csv** in the **horizon** repo.](https://github.com/tedunderwood/horizon/tree/master/chapter3/metadata)
