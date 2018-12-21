makemaster
===========

Code used to generate the master list of fiction metadata. The product of this work is stored in the [**/metadata**](https://github.com/tedunderwood/noveltmmeta/tree/master/metadata) subfolder of noveltmmeta as ```volumemeta.tsv.``` The components that were immediately fused to create it are exposed here, and described below.

If you want to go back even further and understand how these components were *themselves* created, see the scripts ```scrape_json.py``` and ```scrape_marc.py``` in [**DataMunging/HathiMetadata**](https://github.com/tedunderwood/DataMunging/tree/master/HathiMetadata).

pre1923hathifiction.csv
-----------------------
Metadata for fiction before 1923. Fiction was identified algorithmically, using methods documented in [Understanding Genre in a Collection of a Million Volumes.](https://figshare.com/articles/Understanding_Genre_in_a_Collection_of_a_Million_Volumes_Interim_Report/1281251)

Column definitions are explained in [**pre1923datadictionary.md**](https://github.com/tedunderwood/noveltmmeta/blob/master/pre1923datadictionary.md)

If you want to cite this as a resource, I would recommend that you consider citing [the stable form on Figshare:](https://figshare.com/articles/Page_Level_Genre_Metadata_for_English_Language_Volumes_in_HathiTrust_1700_1922/1279201) Underwood, Ted (2014): Page-Level Genre Metadata for English-Language Volumes in HathiTrust, 1700-1922. figshare. https://doi.org/10.6084/m9.figshare.1279201.v1

**pre1923hathifiction.csv** is substantively equivalent to **ficmeta.csv.zip** in the Figshare repo. Other files in the repo include page-level metadata.

The work that developed this dataset was funded by an ACLS Digital Innovation Grant, and by the National Endowment of the Humanities Digital Humanities Start-Up Grant,  Award# HD5178713. The views and results expressed don't necessarily reflect the views of the funding agencies.

Before this dataset was merged with others to create **masterficmetadata,** I ran **enrichpre23.py**, in order to add certain columns of metadata that I had learned to scrape from MARC only after the original dataset was created. These include, e.g., authors' dates of birth and death.

incopyrighthathifiction.csv
---------------------------
Metadata for HathiTrust fiction in copyright. Fiction was identified algorithmically, using a variant of the strategy mentioned above; code is contained in [the 20c genres repo.](https://github.com/tedunderwood/20cgenres)

Column definitions are explained in [**incopyrightdatadictionary.md**](https://github.com/tedunderwood/noveltmmeta/blob/master/incopyrightdatadictionary.md)

If you want to cite this as a resource, I would recommend citing [the stable form on IDEALS:](https://www.ideals.illinois.edu/handle/2142/97948) Ted Underwood, "A List of English-Language Fiction after 1922 in HathiTrust," IDEALS, 2017, https://www.ideals.illinois.edu/handle/2142/97948.

Page-level metadata for this dataset is in **incopyrightpagepredicts.** It's not organized very well yet, and it's bulky, but it's there.

The work that developed this dataset was funded by SSHRC via the NovelTM project, administered at McGill University, and by the Andrew W. Mellon foundation, via the WCSA+DC project, administered by HathiTrust Research Center. The views and results expressed don't necessarily reflect the views of the funding agencies.

oa supplement
-------------

The two datasets described above ("pre23" and "incopyright") don't actually cover everything, because some post-22 fiction is not strictly speaking in copyright. I generated a supplement to cover this; the work was done in **../oasupplement**; it runs to about 4,000 vols.

merging and cleaning the sources
---------------------------------

To merge the sources above, I ran **merge_sources_to_master.py**; this script also does a little data cleaning.

For more involved kinds of data cleaning, I wrote a Jupyter notebook, **master_cleaning.ipynb.** Consult that notebook especially for information about the process that produced the **parttitle** column, listing the separate titles for individual volumes of a multi-volume *Collected Works.*

This is also the notebook that produced the **latestcomp** column, inferring the latest possible date of composition for a volume.
