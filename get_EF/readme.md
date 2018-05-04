get extracted features
=======================

Probably down in the weeds for most people browsing the repository, but if you really want to know ...

This folder contains code used to get and parse extracted features. I did that *so that* I could compare the textual similarity of volumes as part of the deduplication workflow. So we are definitely gathering flowers high in a Tibetan meadow, in order feed yaks that will eventually be shaved, in order to create one yak-hair pillow.

But like I say, if you really want to know ...

**generate_path_list.py** was used to transform **../manifestationmeta.tsv** into a list of paths that I could use to retrieve features from HTRC.

Then the command

    rsync -a --files-from=/Users/tunder/Dropbox/python/noveltmmeta/get_EF/justpathlist.txt data.analytics.hathitrust.org::features fic

was used to actually download the files.

Then I ran **parsefeaturejsons.py** to parse the jsons into a matrix of feature counts, using the features listed in **fictionfrequencies.tsv**.
