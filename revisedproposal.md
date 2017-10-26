Proposal for a starter set of English-language fiction 1700-2007
================================================================

This is just a proposal intended to jumpstart discussion. This version revised in October to take account of new thinking as I move closer to implementation.

selection method(s)
--------------------

To summarize where I think we are:

We'd like to create several lists of fiction to help researchers enter this field.

1. One might be a list of everything we can find in Hathi. 100,000+ vols.
2. Another might be a deduplicated list: just distinct title/author combinations, with some special provisions for multivolume works. Still tens of thousands of vols.
3. Another might be a more selective list, let's say of 2,570 volumes. I would anticipate 500 fiction volumes for the 18c and then 2,070 evenly distributed from 1800-2007. (If people want to argue for more even coverage, I'm open to that.) Distribution is by date of publication (earliest known).

First two tasks are straightforward (the first is complete.) But how do we approach the third? 

I think our strategy needs several goals.

1. It needs to communicate that samples are provisional things: there is no such thing as a perfectly-balanced sample suited to answer every conceivable question. This means that any list we construct needs to have a basically plural character, and in presenting it, we need to stress, rhetorically, that it is not a single thing but a bunch of potential things folded together.
2. On the other hand, the social criteria we can use to select volumes tend to have a lifespan of a century or 150 years. There aren't a lot of criteria we can use to select volumes across the full span of 300 years. So if we construct the list *purely* as the union of a bunch of different sets created by different social criteria, it's going to be awfully lumpy, considered as a whole.
3. So I'm going to suggest that we allow the external outlines of the list (underline: external outlines) to be defined, more or less, by the one thing we have that does remain constant across 307 years, HathiTrust Digital Library itself. We'll aim at roughly the same UK/US balance and m/f balance that the library has in each period, and select volumes from authors that cover the same prominent-to-obscure spectrum found within the library. For this purpose, an author's prominence is defined as "number of volumes in the library, relative to the distribution of other authors born around the same time." (Underline "for this purpose.)
4. Going back to underline that three times: "external outlines." A user who wants to change the US/UK balance or m/f balance can do that through the magic of just selecting a subset. A user who wants only frequently-reviewed authors or volumes can select them (we'll have a metadata column listing number of book reviews in periodical indexes 1802-2007.) Bestsellers? Select them. Etcetera. The logic is: this collection mirrors the library because, like the library, it is a resource rather than a corpus. A researcher builds a corpus to represent the social object they're investigating: that part is on you.
5. The last desideratum for this list: we want a lot of metadata for authors. (At least nationality, gender, date of birth.) We already have several lists (Stanford, UIUC, Chicago) with enriched metadata. To save ourselves labor, it makes sense to select authors from those lists where we can. But "where we can" here means, where we have an author of the right prominence. When we need an obscure author, we'll take an obscure author whether or not we can find one in our existing lists. (The UIUC list does have a bunch in the 1820-1950 region.)

A possible objection to this strategy is that we won't have enough authors from certain minority categories to create a subset--racial or ethnic minorities, Americans before 1820, possibly women in a few periods, and so on. (Note, this is different from "balance." We're not trying to create balance overall. But we are trying to give people a resource that permits flexibility.)

So we could enrich our dataset with lists of minority authors wherever appropriate. I would simply add these to the list, while flagging that the method of selection was different. Eighteenth-century authors, certainly 18c American authors, might be one of these underrepresented minorities that need to be supplemented by a different means of selection. 

Metadata structure
------------------

Metadata columns anticipated for volumes:

* author name
* title
* publication date
* first pub date
* author's percentile prominence within the library
* author's percentile prominence measured by counting book reviews [I think I can get that :)]
* book appears on a bestseller list? (y/n)
* librarians' genre/subject categories (I don't propose adding these ourselves)
* best-book lists on which this appears, includes Modern Library, Mark A-H postcolonial survey, Goodreads, maybe Open Syllabus, etc.
* total number of book reviews for this book 1802-2007 in So & Underwood
* total number of book reviews for this author 1802-2007 in So & Underwood
* author gender
* author nationality

for authors:

* author name
* alternate names encountered, a list
* date of birth
* date of death, if known
* nationality
* gender
* total number of books in the library
* total number of book reviews for this author 1802-2007 in So & Underwood

I imagine organizing this as a .tsv. Where we don't know something, we leave the field blank.
Some fields could contain multiple entries: e.g. genre/form categories, alternate names. I'm willing to separate these with a pipe "|" unless someone screams and tells me that's nonstandard, inelegant etc.

Some of the columns for authors might be duplicated in the title database, to make selection-by easier for novices.

Providing actual data
---------------------

But so far we're just talking metadata. An equally big obstacle to research is getting at the text itself, either in the form of connected sentences or as wordcounts.

I'd like to do something to address that. We could aim our efforts at one or both of two targets:

* Breaking works out of intellectual property jail. This could be done by initiating conversation with Hathi/Google, or (maybe more simply) by using Internet Archive texts where available. This will only be useful before 1923 (maybe 1941 now!), and may only cover a subset even there.
* Trimming paratext. We could do that algorithmically or manually. But manually, we probably can't do a lot more than 2000-3000 volumes.

My instinct is to do both things. 1) Provide Internet Archive versions of our texts, where they're available. 2) Provide Hathi extracted features for *all* the texts, and trim the paratext algorithmically.

Another possibility. If we got really ambitious we could construct clean "Frankentext" versions of our novels by overlaying different OCR instances and editions. Errors and paratext would cancel out and you'd be left with a clean text of the narrative itself. Book historians would of course write articles saying that this is a wrong thing to do. Another reason not to do it: it's a lot of work, and doesn't solve the main problem we confront in sharing texts (intellectual property jail.) Third reason not to do it: may happen at Northeastern.

Anyway, this is just a proposal to jumpstart discussion.
