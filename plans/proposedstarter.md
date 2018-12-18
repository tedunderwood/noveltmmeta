Proposal for a starter set of English-language fiction 1700-2007
================================================================

This is just a proposal intended to jumpstart discussion.

To summarize where I think we are:

We'd like to create several lists of fiction to help researchers enter this field.

1. One might be a list of everything we can find in Hathi. 100,000+ vols.
2. Another might be a deduplicated list: just distinct title/author combinations, with some special provisions for multivolume works. Still tens of thousands of vols.
3. Another might be a more selective list.

First two tasks are straightforward (the first is complete.) But how do we approach the third? I think we've agreed that we want to select the list in several ways (or allow it to be created as the union of several lists). Partly this is a strategy to communicate that samples are provisional things: there is no such thing as a perfectly-balanced sample suited to answer every conceivable question.

But okay, granted that we're going to select volumes in several ways -- what are those ways?

* One strategy is to select volumes that seem important for some reason. Say:
    1. Works listed as "canonical" in the Open Syllabus project, or frequently reviewed in Goodreads (these are of course contemporary perspectives).
    2. *Publishers Weekly* bestsellers, after 1895.
    3. Works frequently reviewed by reviewers at the time. (Several sources for this, but none yet that will cover the whole period 1700-2007.)
    4. Works frequently reprinted, or works by authors who were frequently reprinted.
    5. Other lists of best books, e.g. mediated by Algee-Hewitt/McGurl.
* Two problems with that strategy:
    1. Many research questions require some kind of contrast between prominent and obscure works, but we'll have no obscure works.
    2. Our lists are likely to cover different timespans. E.g., I have a sample of reviewed authors 1820-1950. Goodreads and Open Syllabus will skew contemporary. Algee-Hewitt/McGurl cover the 20c. Disjoint timespans are okay, but it would be nice to have a more integrated list that covers 1700-2007 evenly.
* So here's a suggested amendment/addition to our "list of lists." Instead of just doing (iv) above (taking works frequently reprinted), let's construct a sample explicitly stratified to cover different levels of prominence or obscurity. I would suggest this approach: sort authors based on the number of volumes they have in the library (across all periods). Then divide that list into three parts. Select 1000 volumes from the top third (authors frequently reprinted). Then 1000 volumes from the middle third, and 1000 volumes from the bottom. With the proviso that each list of 1000 has to be evenly distributed across decades. Let's call this the stratified list.
    - a problem here: the eighteenth century is so sparse in Hathi that it might not work to distribute texts evenly across decades
    - Another problem: the division into thirds creates a needless discontinuity that will overprivilege authors near the bottom of each "third." It probably works better to divide the corpus into percentiles, and balance probabilities so each percentile has an equal chance of representation. Then we can report percentiles in the metadata.
* Another problem: demographic balance. This could be addressed by rebalancing the lists described above, or by creating supplementary lists. Both approaches are probably needed. If we have lists of authors from minority ethnicities, those lists may be small enough that we could simply add them, in toto, to our starter set. Where gender is concerned, I would be inclined to create an additional version of the stratified list where we guarantee a) that the whole list includes equal numbers of men and women and b) that the sorting of authors is done separately for men and women so they have equal chances to be in each "third."

We can compose a selective list by taking the union of all of the above. We'll have a column for each mode of selection to indicate whether a given volume was included in *that* list. We can enrich metadata for authors, using existing metadata gathered at Stanford and Chicago.

Doing all that may produce a list of 8000 or 9000 works. That may be too large for some purposes, and the whole apparatus of selection may be too complex for people just starting out to think about. If we want to construct a super-simple starter subset of 1000 volumes I have no objection. But how to do that? One solution would be: just take the top third of the gender-balanced stratified list (described in the last bullet point above).

But so far we're just talking metadata. An equally big obstacle to research is getting at the text itself, either in the form of connected sentences or as wordcounts.

I'd like to do something to address that. We could aim our efforts at one or both of two targets:

* Breaking works out of intellectual property jail. This could be done by initiating conversation with Hathi/Google, or (maybe more simply) by using Internet Archive texts where available. This will only be useful before 1923, and may only cover a subset even there.
* Trimming paratext. We could do that algorithmically or manually. But manually, we probably can't do a lot more than 2000-3000 volumes.

My instinct is to do both things. 1) Provide Internet Archive versions of our texts, where they're available. 2) Provide Hathi extracted features for *all* the texts, and trim the paratext algorithmically.

Another possibility. If we got really ambitious we could construct clean "Frankentext" versions of our novels by overlaying different OCR instances and editions. Errors and paratext would cancel out and you'd be left with a clean text of the narrative itself. Book historians would of course write articles saying that this is a wrong thing to do. Another reason not to do it: it's a lot of work, and doesn't solve the main problem we confront in sharing texts (intellectual property jail.)

Anyway, this is just a proposal to jumpstart discussion.
