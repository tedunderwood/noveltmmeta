deduplication
=============

Code used in the deduplication process. Mainly Jupyter notebooks for legibility.

To understand these notebooks, you need to keep in mind that the names of the datasets were changed at the end of the process to be more intelligible to a wide audience.

1. The largest dataset, now called ```volumemeta.tsv``` will be referred to in these notebooks as ```masterficmeta.tsv.```

2. The next stage of deduplication, now called ```recordmeta.tsv,``` will be referred to in these notebooks as ```manifestationmeta.tsv.```

3. The last stage of deduplication, now called ```titlemeta.tsv,``` is referred to here as ```workmeta.tsv.```

With those provisos, I hope the code here is mostly intelligble.

first_deduplication.ipynb
-----------------------------

takes the dataset from **../masterficmeta.tsv** to **../manifestationmeta.tsv,** which has one copy of each volume (counting multiple reprintings as separate volumes). It also does some standarization of author names, and in the process produces **authorgroups.tsv**, recording names taken to be "the same person." **Manual_author_matches.tsv** are also used at this stage to standardize names.

second_deduplication.ipynb
---------------------------

takes the dataset from **../manifestationmeta.tsv** *most of the way* to **../workmeta.tsv,** which aspires to have one copy of each "work" or "title."

Most of the work here is done by a probabilistic model that predicts whether two volumes belong to the same work. Three variables are used:

**titlematch**, which is based on fuzzy matching between the first 35 characters of the titles

**cossim**, cosine distances between the 1000 most common features in the texts of the volumes

**hasworks**, which is **1** if the title of either volume contains "novels" or "works," and otherwise **0**

In the process, a lot of questionable decisions have to be made. Some of those decisions are memorialized in **ignoredgroups.tsv.** Inferences about authorial identity are recorded in **authorsets.tsv.** Linkages made in deduplication are recorded in **allgroups.tsv.** Sorry that these file names are not more immediately interpretable! You may need to consult the notebook to see what they mean.

Note that this notebook does not write the final form of **../workmeta.tsv.** That takes place in

third_deduplication.ipynb
---------------------------

This notebook undertakes a couple of clean-up projects, fixing details of **manifestationmeta** and **workmeta**. But it also, more importantly, adds **earlyedition,** a column in **workmeta** that records whether a volume was published within 25 years of its author's death. Books where **earlyedition == False** are later reprints; if you ignore these, **workmeta** has about 129,000 books: this is the population that will be sampled for most of our manually-corrected short lists.

