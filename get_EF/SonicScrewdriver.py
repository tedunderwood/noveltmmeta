#!/usr/bin/env python3

# SonicScrewdriver.py
# Version January 1, 2015

def addtodict(word, count, lexicon):
	'''Adds an integer (count) to dictionary (lexicon) under
	the key (word), or increments lexicon[word] if key present. '''

	if word in lexicon:
		lexicon[word] += count
	else:
		lexicon[word] = count

def appendtodict(key, value, dictoflists):

    if key in dictoflists:
        dictoflists[key].append(value)
    else:
        dictoflists[key] = [value]

def sortkeysbyvalue(lexicon, whethertoreverse = False):
	'''Accepts a dictionary where keys point to a (presumably numeric) value, and
	returns a list of keys sorted by value.'''

	tuplelist = list()
	for key, value in lexicon.items():
		tuplelist.append((value, key))

	tuplelist = sorted(tuplelist, reverse = whethertoreverse)
	return tuplelist

def sortvaluesbykey(lexicon):
    '''Accepts a dictionary of numeric keys, such as page numbers, and
    returns a tuplelist of key-value pairs sorted by the key.'''

    tuplelist = list()
    for key, value in lexicon.items():
        tuplelist.append((key, value))

    tuplelist = sorted(tuplelist)
    return tuplelist

def add_dicts(source, target):
    '''Adds the values in source to corresponding
    keys in target, or creates them if missing.'''

    for key, value in source.items():
        if key in target:
            target[key] += value
        else:
            target[key] = value

def clean_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if ':' in postfix:
        postfix = postfix.replace(':','+')
        postfix = postfix.replace('/','=')
    if '.' in postfix:
        postfix = postfix.replace('.',',')
    cleanname = prefix + "." + postfix
    return cleanname

def dirty_pairtree(htid):
    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if '=' in postfix:
        postfix = postfix.replace('+',':')
        postfix = postfix.replace('=','/')
    if ',' in postfix:
        postfix = postfix.replace(',','.')
    dirtyname = prefix + "." + postfix
    return dirtyname

def pairtreepath(htid,rootpath):
    ''' Given a HathiTrust volume id, returns a relative path to that
    volume. While the postfix is part of the path, it's also useful to
    return it separately since it can be a folder/filename in its own
    right.'''

    period = htid.find('.')
    prefix = htid[0:period]
    postfix = htid[(period+1): ]
    if ':' in postfix:
        postfix = postfix.replace(':','+')
        postfix = postfix.replace('/','=')
    if '.' in postfix:
        postfix = postfix.replace('.',',')
    path = rootpath + prefix + '/pairtree_root/'

    if len(postfix) % 2 != 0:
        for i in range(0, len(postfix) - 2, 2):
            next_two = postfix[i: (i+2)]
            path = path + next_two + '/'
        path = path + postfix[-1] + '/'
    else:
        for i in range(0, len(postfix), 2):
            next_two = postfix[i: (i+2)]
            path = path + next_two + '/'

    return path, postfix

## REVISED utility
## that reads my standard tab-separated metadata table,
## and returns three data objects: 1) a list of row indexes
## stored in the first column (e.g. volume ids).
## 2) a list of column names, and
## 3) a dictionary-of-dictionaries called table where
## table[columnname][rowindex] = the value of that cell.
## the difference here is thatthe first column, containing
## row indexes, is also returned as a column of the table.
## In the original version, it stupidly wasn't.
##
## This is equivalent to FileUtils.readtsv2

def readtsv(filepath):
    with open(filepath, encoding='utf-8') as file:
        filelines = file.readlines()

    header = filelines[0].rstrip()
    fieldnames = header.split('\t')
    numcolumns = len(fieldnames)
    indexfieldname = fieldnames[0]

    mincols = 1000
    for line in filelines:
        colnum = len(line.split('\t'))
        if colnum < mincols:
            mincols = colnum

    if mincols < numcolumns:
        numcolumns = mincols
        fieldnames = fieldnames[0:numcolumns]

    table = dict()
    indices = list()

    for i in range(0, numcolumns):
        table[fieldnames[i]] = dict()

    for line in filelines[1:]:
        line = line.rstrip()
        if len(line) < 1:
        	continue
        fields = line.split('\t')
        rowindex = fields[0]
        indices.append(rowindex)
        for thisfield in range(0, numcolumns):
            thiscolumn = fieldnames[thisfield]
            if len(fields) > thisfield:
                thisentry = fields[thisfield]
            else:
                thisentry = ""

            table[thiscolumn][rowindex] = thisentry

    return indices, fieldnames, table

def writetsv(columns, rowindices, table, filepath):

    import os

    headerstring = ""
    numcols = len(columns)
    filebuffer = list()

    ## Only create a header if the file does not yet exist.

    if not os.path.exists(filepath):

        headerstring = ""
        for index, column in enumerate(columns):
            headerstring = headerstring + column
            if index < (numcols -1):
                headerstring += '\t'
            else:
                headerstring += '\n'

        filebuffer.append(headerstring)

    for rowindex in rowindices:
        rowstring = ""
        for idx, column in enumerate(columns):
            rowstring += table[column][rowindex]
            if idx < (numcols -1):
                rowstring += '\t'
            else:
                rowstring += '\n'

        filebuffer.append(rowstring)

    with open(filepath, mode='a', encoding = 'utf-8') as file:
        for line in filebuffer:
            file.write(line)

    return len(filebuffer)

def easywritetsv(columns, rowindices, table, filepath):
    '''This version does not assume the table contains a dict for rowindices'''
    firstcolumn = columns[0]
    table[firstcolumn] = dict()
    for idx in rowindices:
        table[firstcolumn][idx] = idx

    import os

    headerstring = ""
    numcols = len(columns)
    filebuffer = list()

    ## Only create a header if the file does not yet exist.

    if not os.path.exists(filepath):

        headerstring = ""
        for index, column in enumerate(columns):
            headerstring = headerstring + column
            if index < (numcols -1):
                headerstring += '\t'
            else:
                headerstring += '\n'

        filebuffer.append(headerstring)

    for rowindex in rowindices:
        rowstring = ""
        for idx, column in enumerate(columns):
            rowstring += table[column][rowindex]
            if idx < (numcols -1):
                rowstring += '\t'
            else:
                rowstring += '\n'

        filebuffer.append(rowstring)

    with open(filepath, mode='a', encoding = 'utf-8') as file:
        for line in filebuffer:
            file.write(line)

    return len(filebuffer)

def pairtreefile(htid):
    ''' Given a dirty htid, returns a clean one that can be used
    as a filename.'''

    if ':' in htid or '/' in htid:
        htid = htid.replace(':','+')
        htid = htid.replace('/','=')

    return htid

def pairtreelabel(htid):
    ''' Given a clean htid, returns a dirty one that will match
    the metadata table.'''

    if '+' in htid or '=' in htid:
        htid = htid.replace('+',':')
        htid = htid.replace('=','/')

    return htid

def infer_date(datetype, firstdate, seconddate, textdate):
    '''Receives a date type and three dates, as strings, with no guarantee that any
    of the dates will be numeric. The logic of the data here is defined by
    MARC standards for controlfield 008:

    http://www.loc.gov/marc/bibliographic/concise/bd008a.html

    Returns a date that represents either a shaky consensus
    about the earliest attested date for this item, or 0, indicating no
    consensus.
    '''

    try:
        intdate = int(firstdate)
    except:
        # No readable date
        if firstdate.endswith('uu'):
            # Two missing places is too many.
            intdate = 0
        elif firstdate.endswith('u'):
            # but one is okay
            try:
                decade = int(firstdate[0:3])
                intdate = decade * 10
            except:
                # something's weird. fail.
                intdate = 0
        else:
            intdate = 0

    if intdate == 0:
        try:
            intdate = int(textdate)
        except:
            intdate = 0

    try:
        intsecond = int(seconddate)
    except:
        intsecond = 0

    if intsecond - intdate > 80 and intsecond < 2100:
        # A gap of more than eighty years is too much.
        # This is usually an estimated date that could be anywhere within
        # the nineteenth century.
        # note that we specify intsecond < 2100 because otherwise things
        # dated 9999 throw an error
        intdate = 0

    if datetype == 't' and intsecond > 0 and intsecond < intdate:
        intdate = intsecond
        # This is a case where we have both a publication date and
        # a copyright date. Accept the copyright date. We're going
        # for 'the earliest attested date for the item.'

    if intdate < 1000 and intsecond > 1700 and intsecond < 2100:
        intdate = intsecond

    return intdate

def simple_date(row, table):
    datetype = table["datetype"][row]
    firstdate = table["startdate"][row]
    secondate = table["enddate"][row]
    textdate = table["textdate"][row]
    intdate = infer_date(datetype, firstdate, secondate, textdate)
    return intdate

def date_row(row):
    datetype = row["datetype"]
    firstdate = row["startdate"]
    secondate = row["enddate"]
    if "imprintdate" in row:
        textdate = row["imprintdate"]
    else:
        textdate = row["textdate"]
    intdate = infer_date(datetype, firstdate, secondate, textdate)
    return intdate

