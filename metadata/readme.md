metadata
=========

Our datasets can be broadly divided into three long lists (> 100,000 volumes) and four shorter lists (< 3,000 volumes), of which three have been manually corrected by human readers. Our long lists were created by probabilistic models that entail significant levels of error. The manually-corrected lists reduce that error, at the cost of providing a smaller sample.

three long lists
=================

1  The volume list.
--------------------

This list includes all the volumes we found and identified as fiction: 210,305 volumes between 1700 and 2010. It includes many duplicates: multiple editions/printings of the same title, as well as multiple copies of each printing. The outer boundary of this list was shaped by probabilistic models that identified fiction and attempted to filter out other genres (error enters at this step of the process).

2  The record list.
--------------------

This list tries to exclude duplicate copies of the same printing, using Hathi “record ids” and “volume numbers” to identify duplicate copies. At this level of deduplication, we have 176,650 distinct records. This is roughly analogous to the "manifestation" level of description in Functional Requirements for Bibliographic Records.   (Please note that the analogy is only rough.)

3  The title list.
-------------------

This list tries to identify one copy of each fiction "title"—by preference the earliest copy available in Hathi. In other words, different editions of a novel, possibly with different prefatory material or even different language in the text itself, will usually be collapsed into a single title. This is roughly the level of description characterized as “work” in FRBR—although again, the analogy is only approximate. This level of deduplication produces a list of 138,164 distinct titles. To identify different records as examples of “the same title” we used a probabilistic model, which again, introduces a source of error.

four shorter lists
===================

Three of these lists were manually checked by Patrick Kimutis, Jessica Witte, and Ted Underwood, in an effort to filter out certain categories of obvious error. This is not to say that our judgments are objectively correct. The questions we coded include judgments about genre and authorial nationality that are open to different opinions. Different human readers often answer differently, as we found by comparing our judgments about a set of shared volumes. The goal of manual checking was not to produce standpoint-free objectivity, but on the contrary to construct a known and recognizable vantage point (the opinions of three people trained as literary historians, including a model of the range of variation one typically finds in such a group).

4  The manually-checked title subset.
-------------------------------------

This is simply a random subset of the title list distributed evenly across the timeline. We manually add columns for authorial gender and nationality, and for the genre (category) of the title. We also manually confirm dates of first publication.

5  The weighted subset.
------------------------

This list overlaps in part with list #4, and is (like that list) a manually-checked subset of the larger title list. But where list #4 was produced by giving each title an equal chance of inclusion, our goal here was to produce a subset of the title list weighted by the frequency of reprinting—so that the list will be slightly biased toward titles that recur frequently in libraries.

If we had done this in the simplest possible way, the effect would have been roughly to produce a subset of the volume list (which has, after all, one row for each copy of a title). But we limited our count of reprints to volumes reprinted within 25 years of a title’s first appearance in Hathi. In other words, writers like Walter Scott and George Eliot will benefit from their substantial nineteenth-century circulation. But a writer like Jane Austen, whose reputation was slower to reach its current level, will see less benefit from reprinting in this list.

6  The gender-balanced subset.
-------------------------------

This is strictly a subset of list #4, reduced in size to ensure equal representation of writers who identified as men and those who identified as women in each five-year segment of time. We have also included a proportional sample of works where gender was marked “unknown or other,” but further work would be needed to explicitly address nonbinary gender identities. Nor does this list address ethnic and racial imbalances in literary history, or limitations of class perspective. In fact, we don’t intend to claim that this list has created a more just or more correctly balanced representation of the past at all. It is simply a different representation. We created it partly so we that could ask how much difference the rebalancing makes for various questions.

7  The frequently reprinted subset.
-------------------------------------

This subset of the title list has been selected by choosing the volumes where we had the largest number of editions and instances attested within 25 years of a title’s first appearance in HathiTrust. Unlike the weighted list, which gives rarely-purchased books a small chance of inclusion, this list is composed purely of popular titles.

We estimate reprinting by counting copies in a digital library. This is not intended as a claim about the actual number of reprintings scholarly bibliographers would find, if they had time to trace all the reprintings of 135,000 titles. However, we can be pretty sure that this measure will filter out obscure books printed only once or twice—which are the majority of titles in a digital library. It will thus produce a list very different from a random sample of titles—a list strongly biased toward the books most commonly bought by academic libraries (within 25 years of first publication). Since the present project aims to provide social parallax rather than bibliographic exactness, this will suffice. This list was not manually checked; we simply didn’t have time.

