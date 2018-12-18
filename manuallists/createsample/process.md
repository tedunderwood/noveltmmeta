data correction process for short-form metadata
=======================================

As you go through each row,

**a)** decide whether this is fiction; if not, write **nonfic** or **poetry** under **category**, and skip to the next row

**b)** is this printing at **inferreddate** probably within 25 years of the book's composition? If the answer is clearly "no," write **reprint** under **category,** and skip to the next row

**c)** is this a special category of fiction other than adult novel-length? E.g., **shortstories** or **juvenile**? If so, keep correcting the metadata, but write the appropriate category. If it's a novel or novella for a (mostly) adult audience, write **novel** under **category**.

**d)** Authorial data. Try googling the author. Some authors will be impossible to find. Don't sweat it; we've got a lot of rows to get through. Leave nationality blank if you don't know. Leave gender blank if you can't guess, but feel free to guess from the name. If nationality is ambiguous (e.g. Henry James) feel free to leave this field blank.

**gender**: m/f/u/o

**nationality**: uk (England/Scotland)
us (USA)
ca (Canada)
ir (Ireland)
au (Australia)
nz (New Zealand)
sa (South Africa)
de (Germany)
fr (France)
it (Italy)
es (Spain)
me (Mexico)
ru (Russia)
be (Belgium)
ch (China)
gk (Greece)
aus (Austria)
lit (Lithuania)
cu (Cuba)
ni (Nigeria)
jp (Japan)
ar (Argentina)
nic (Nicaragua)
ph (Phillippines)
cmr (Cameroon)
pk (Pakistan)
swe (Sweden)
no (Norway)
in (India)
ba (Barbados)

add as needed

If you have info about authors' birth or death dates, add it, keeping to the format you find under a**uthordate.** Here and elsewhere, it is generally not helpful to add explanatory prose notes in a field where the program is going to expect to find a very limited & predictable range of options.

If a **realname** or **pseudonym** is salient, add it. If not (it's usually not) leave those fields blank.

**e) Work-specific questions.** Try to infer first publication date for the work. If you find something earlier than **inferreddate**, put it in the **firstpub** column. If not, leave that column blank. If the title implies that this is a volume of *Collected Works* (or similar generic title), see if you can infer the volume-specific title by copying the docid and pasting it into a HathiTrust URL. If so, put the more specific title in **shorttitle.** If not, that's fine; don't sweat this part.

**f)** Finally, make sure something is written under **category**; we're going to be using that field to distinguish completed rows from not-yet-examined rows. You may sort or reshuffle your data, so you won't be able to count on mere sequence to keep track of what you've done.


