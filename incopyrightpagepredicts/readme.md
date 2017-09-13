page-level predictions for post-1922 fiction
============================================

This is bulky and not well organized, but I'm making it available anyway. Basically, I've gone through all the IDs in my list of **incopyrightfiction.csv** and made page-level predictions of the likelihood that each page *is fiction.*

The files here are really .jsonl rather than .json. That's to say, each line is a separate json object.

The data format is fairly self-explanatory. **docid** is the HathiTrust volume ID. **pagepredictions** points to a list of real numbers indicating the probability-of-being-fiction for each page. These pages are in the same order as HathiTrust Extracted Features *in 2016* (see below for the problem of persistence). If you just want to "get the fiction," you can take a sequence of pages from **firstpage** to **lastpage,** inclusive.

What I don't have yet is a beautiful index telling you which volume is in which file. Right now, your only alternative is to download them all. **TODO:** fix that.

Problem of persistence:
-----------------------

These predictions are keyed to HathiTrust Extracted Features in 2016. But pagination of volumes can change. The number of pages in a volume can and does change on subsequent OCR passes, so there is no absolutely reliable way to persistently indicate a single page in HathiTrust. I don't have a good solution for this problem, other than recommending that researchers who want to use this data hold onto the 2016 version of Extracted Features. Alternately, and ideally, we should re-create this data for subsequent versions.