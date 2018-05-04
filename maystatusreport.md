status report
==============

So the [plan back in November](https://github.com/tedunderwood/noveltmmeta/blob/master/revisedproposal.md) was to

1. Start with a general list of all the fiction I could find in Hathi, and then

2. generate a deduplicated list (distinct title/author combinations). Then we would move on to

3. several subsets of the deduplicated list, selected to "represent" the literary past in different ways.

The status report today is that I've basically completed (1) and (2) -- though I'm going to be fine-tuning (2) for a couple more days -- and am getting ready to move to (3). I'm starting to think about which parts of (3) I can tackle with RAs here at Illinois, and which parts will need to be taken on by someone else, if they happen at all.

The master list described in stage (1) is **masterficmetadata.tsv**; the process of creating it is documenting in [**noveltmmeta/makemaster**](https://github.com/tedunderwood/noveltmmeta/tree/master/makemaster). It includes 210,305 volumes of fiction from HathiTrust Digital Library, 1700 - 2010.

deduplication
-------------

The process of deduplication has turned out to be complex enough that I've done it in two steps. These are documented in [**noveltmmeta/dedup**](https://github.com/tedunderwood/noveltmmeta/tree/master/dedup).

2a. The first step is to winnow duplicate copies of *the same printing.* In other words, after this first round of dedup, there will still be several copies of *Middlemarch* in the dataset: maybe a three-volume edition from the 1870s, as well as one-volume editions in 1892, 1924, 1960, and so on. But there should be only one copy of each volume, in each edition. This level of deduplication is roughly equivalent to [the "manifestation" level of description in FRBR.](https://en.wikipedia.org/wiki/Functional_Requirements_for_Bibliographic_Records). So I call this level **manifestationmeta.tsv**; it contains 176,650 volumes. In the process of producing this file, I also standardize author names a little, assign individual "short titles" to the vols of *Collected Works* where possible, and ensure that biographical information about an author (birth and death dates) propagates across all their records.

2b. The second step tries to collapse all the copies of *Middlemarch* into a single representation of the *work*--ideally the earliest representation (the three-volume edition from the 1870s). The file that results will be called **workmeta.tsv**, and will become the starting point for many subsequent operations. I'm a day or two away from completing this stage. There's a notebook currently in the github repository that tries to do it just using metadata (mostly title & record ID), but I have found I can get more accuracy if I also use information about content (cosine similarity on extracted features from HathiTrust is helping a model decide when two records are "the same book.") Exact number still not clear, but this is going to get us down in the range of 120k - 140k "works." I may further filter using authors' death dates to produce a list of ~100k works published, say, within 20 years of their authors' lifespan (**contemporaryworkmeta.tsv**).

Then we have to decide

How to sample further
---------------------

Back [in Nov, I was very ambitious](https://github.com/tedunderwood/noveltmmeta/blob/master/revisedproposal.md) about the range of subsets I expected to produce. As I get closer to the task, I'm being more realistic about my limits. Right now I anticipate something like.

3a. A random sample of **contemporaryworkmeta**: 2000 volumes of fiction where each work has an equal chance to be represented, no matter how often it was reprinted.

3b. A sample weighted by some proxy of contemporary popularity. As I collapse the list down to **contemporaryworkmeta**, I'm keeping track of how many individual records get "reduced" to produce a single work, and also how many of those come from the 20 yrs immediately after the work's first publication (in our list). So I can produce a sample of 2000 volumes where a work's chance of representation is loosely proportional to number-of-printings-bought-by-libraries in its first two decades.

3c. From 1895 forward, we also have American bestseller lists. I can provide a list of matching Hathi records.

3d. A gender-balanced sample where books by men and by women are equally represented.

3e. In the fall I proposed creating a sample that would attempt "demographic balance," including across ethnicities, but I think I want to ask other members of NovelTM whether it actually makes sense to attempt that.

3f. A 20c "best books" list, with matching Hathi records.

3g. In the fall I proposed assembling 70-100 Gutenberg texts that we could use for annotation, etc, but this is something I will probably let slip unless it's a priority for someone else.

3h. Other things, if anyone wants to take them on.

The creation of these samples will be strongly dependent on research assistants funded by NovelTM. The RAs will need to groom each sample to ensure that it contains only fiction, and that basic demographic information about each author is correct. They may also enrich genre tags, at least to separate novels from short stories, and possibly to propagate other LoC genre designations more evenly across the timeline. In doing this, I'll try to ensure that they learn some data analysis skills along with the grunt work.

Note that I am not proposing to *limit* these samples to novels, but rather to tag the novels as novels.

The final report
-----------------

I envision creating a report that documents the process of creation, and also does a little interpretive comparison between different samples. For instance, I think it would be interesting to take a trend (like the one defined in Stanford Lit Lab pamphlet #4), and show how it does, or doesn't, change across samples 3a-3d.

We can also easily package up extracted features for the subsamples. I'm not planning to jailbreak texts otherwise; increasingly feel that HTRC data capsules are the solution there.

If someone can show me how to generate VIAF identifiers for the volumes, I'll do that. Also, if someone wants to translate these lists into LOD/RDF format, I would welcome that as part of the overall data publication.
