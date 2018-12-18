Proposal for a starter set of English-language fiction 1700-2007
================================================================

A proposal for a starter set of English-language fiction, revised after the NovelTM meeting to incorporate suggestions in Montréal.

selection method(s)
--------------------

To summarize where I think we are:

We'd like to create several lists of fiction to help researchers enter this field.

1. One might be a list of everything we can find in Hathi. 206,000+ vols. Metadata will often be sparse; there will be a significant number of false positives. Lots of stuff in translation.

2. Another might be a deduplicated list: just distinct title/author combinations, with some special provisions for multivolume works. Still tens of thousands of vols. Still no enriched metadata.

3. Then there will be eight alternative subsets of the deduplicated list. To be frank, presenting these as "eight alternative lists" is to some extent a rhetorical choice. In my inmost soul, I still think of this as a single flexible resource designed to allow the *user* to define criteria of representation and select their own subset. And, in fact, it can still be used that way. But I've been persuaded that the flexibility of the list is best communicated by example: i.e., let's go ahead and select a bunch of different subsets. The first five of these would each be ~2,000 volumes long.

    a. A random sample that echoes nationality / gender / reprint-frequency proportions in Hathi. Works in translation excluded; we balance nationality purely inside an Anglo-American context. Even distribution across time 1700-2007.

    b. A sample of the authors most commonly reprinted in the library. Works in translation are not excluded. Even distribution 1700-2007.

    c. A sample of the authors most commonly reviewed across 1800-2007 (not just in their lifetimes). (So & Underwood will provide information about *when* these authors were reviewed in a separate data publication.) Works in translation will not be excluded here, but works are selected by frequency of review in Anglo-American publications. Only 1800-2007, because we won't have review info before 1800.

    d. A gender-balanced list. 1700-2007. Selection otherwise as per (a).

    e. A list balanced to approximate demographic representation as best we can given works available. I.e, we can actually look up the American/UK population and ethnic composition in each decade, and try to include works that echo those proportions (to the extent that we can find enough works in Hathi -- and flag places where we just can't). Works in translation excluded. This list will require a lot of collaboration. Someone will have to do the demographic research; someone will have to create a list of books by nonwhite authors in Hathi. The list can only be supplemented with non-Hathi volumes if someone wants to take on the labor of tokenizing those volumes in a way compatible with Hathi extracted features.

    f. A couple of 20c best-books lists (short).

    g. A short list of 70-100 volumes that we want to use for pedagogical/annotation purposes. Created by you all manually adding things to a Google spreadsheet, using whatever mixture of criteria you like. If you want to use Gutenberg texts rather than Hathi for this, that's fine, and possibly a good idea. Then we could actually provide the texts. This is another place where someone else could take on some of the labor. There's no reason this process has to be coordinated with a-f above.

    h. Finally, a superset of all the volumes included in a-f above. We're going to try to make these lists overlap as much as possible, so hopefully the superset is only like 5,000-6,000 works tops. [I don't want to create a manual metadata nightmare for us (or for me).] All the metadata is available, so users of the dataset who don't feel a through g represent the thing they want to study are politely exhorted to define their own list, using whatever mixture of criteria they like. If we want to build a beautiful web interface to help users turn the dials, someone else will need to volunteer to do that. 

4. There's also a list of authors inclided in 3(a-h).

Benchmarking
------------

We'll provide some measure of OCR quality for all the volumes. I'm open to suggestions about the best measure; will probably ask David Bamman when I get close to doing this. We will also use this measure to indicate how mean OCR quality varies across the timeline.

People may want to know how Hathi itself compares to other possible samples of the literary past. We'll do some benchmarking against Garside and Publishers Weekly, to produce a diachronic illustration.

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
* a flag, originally composed in English (True/False)
* mode(s) of selection; this may boil down to, which of the eight lists prompted its inclusion
* estimated OCR quality
* whatever linked-data identifier is available

for authors:

* author name
* alternate names encountered, a list
* date of birth
* date of death, if known
* nationality
* gender
* total number of books in the library
* total number of book reviews for this author 1802-2007 in So & Underwood
* whatever linked-data identifier is available

I imagine organizing this as a .tsv. Where we don't know something, we leave the field blank.
Some fields could contain multiple entries: e.g. genre/form categories, alternate names. I'm willing to separate these with a pipe "|" unless someone screams and tells me that's nonstandard, inelegant etc.

Some of the columns for authors might be duplicated in the title database, to make selection-by easier for novices.

Linked open data
----------------

Once I've assembled the lists, I'll ask Susan Brown how best to generate standard identifiers for volumes and authors, using VIAF or some analogous authority. If someone wants to translate our metadata itself into RDF, they're welcome to, but I don't propose to undertake that project myself.

Providing actual data
---------------------

But so far we're just talking metadata. An equally big obstacle to research is getting at the text itself, either in the form of connected sentences or as wordcounts.

I'd like to do something to address that. We could aim our efforts at one or both of two targets:

* Breaking works out of intellectual property jail. This could be done by initiating conversation with Hathi/Google, or (maybe more simply) by using Internet Archive texts where available. This will only be useful before 1923 (maybe 1941 now!), and may only cover a subset even there.
* Trimming paratext. We could do that algorithmically or manually. But manually, we probably can't do a lot more than 2000-3000 volumes.

My instinct is to do both things. 1) Provide Internet Archive versions of our texts, where they're available. 2) Provide Hathi extracted features for *all* the texts, and trim the paratext algorithmically.

Another possibility. If we got really ambitious we could construct clean "Frankentext" versions of our novels by overlaying different OCR instances and editions. Errors and paratext would cancel out and you'd be left with a clean text of the narrative itself. Book historians would of course write articles saying that this is a wrong thing to do. Another reason not to do it: it's a lot of work, and doesn't solve the main problem we confront in sharing texts (intellectual property jail.) Third reason not to do it: may happen at Northeastern.

Anyway, this is just a proposal to jumpstart discussion.
