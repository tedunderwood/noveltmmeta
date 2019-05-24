Column definitions for the manually-checked title subset.
=========================================================

The **manual_title_subset.tsv** is largely a subset of **titlemeta.tsv,** and definitions for most of the columns can be found in [**titlemeta_data_dictionary.md**](https://github.com/tedunderwood/noveltmmeta/blob/master/metadata/titlemeta_data_dictionary.md).

However, there are a few added columns that need explanation.

**realname** and **pseudonym** gave us places to manually enter information about names for an author other than the name used in library metadata. If a pseudonym is generally used in metadata, we may provide a **realname,** for instance. However, this aspect of data correction was done casually; we do not promise to have made all possible corrections, and we have not tried to link authors to a name authority.

**gender** is recorded as (m)asculine, (f)eminine, or (u)nknown or other. We agree that better, more complex schemes of gender encoding exist, but we decided that it was better to have some information here than none.

**firstpub** records date of first publication for the work, as best as we could infer.

We recorded **nationality**, when known, using the following codes:

uk (England/Scotland)

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

da (Denmark)

po (Poland)

ru (Russia)

bu (Bulgaria)

kn (Kenya)

is (Israel)

gui (Guinea)

cz (Czech Republic)

pr (Puerto Rico)

We corrected **shorttitle** in cases where it was clearly in error, for instance, when a volume bore a title like *Collected Works* instead of something more specific.

**category** contains a rough genre categorization. Options include *poetry, drama, notfiction, juvenile, shortfiction,* and *longfiction.* We avoided terms like "novel" and "short story" because we don’t want to bog down in debates about whether, for instance, sketches and folk tales are short stories *sensu stricto.* Since genre, form, and audience are in principle separable, it would be possible to assign multiple tags to indicate, for instance, that a volume is juvenile nonfiction. In practice this report is focused on fiction, so we assigned only a single value in this column; we have not attempted to subdivide poetry, drama, or nonfiction by audience.

Please note that columns not mentioned above do *not* contain our own judgments about a work, but rather metadata extracted from MARC records. For instance, the **genres** column is extracted from several different MARC fields, and will often contain wrong, missing, or contradictory information.

