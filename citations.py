#!/usr/bin/env python3

"""
Given an author identified by his/her BAI, this simple Python3 script counts the
number of citations and the number of citations excluding self cites in the
Inspirehep database (https://inspirehep.net/) for each paper in a given collection.
"""

__author__ = 'Edgardo Franzin'
__version__ = '1.0.3'
__license__ = 'GPL'
__email__ = 'edgardo<dot>franzin<at>gmail<dot>com'


import string, re, sys
from optparse import OptionParser

# Parse options
usage = sys.argv[0] + ' [-b|--BAI=<BAI>] [-c|--collection=<COLLECTION>] [-r|--reversed] [-h|--help]'

parser = OptionParser(usage)

parser.add_option('-b', '--BAI', dest='BAI',
                  help='BAI identifier; default: E.Franzin.1', default='E.Franzin.1')
parser.add_option('-c', '--collection', dest='collection',
                  help='collections: all, book, citeable, conferencepaper, introductory, lectures, proceedings, published, review, thesis; default: published', default='published')
parser.add_option('-r', '--reversed', action='store_true', dest='order',
                  help='list the items in chronological order')

(options, args) = parser.parse_args()

BAI = options.BAI
collection = options.collection
order = options.order

# Import the library used to query a website
# and the Beautiful soup functions to parse the data returned from the website
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup as bs

# Open the INSPIRE-HEP profile
inspirehepprofile = 'https://old.inspirehep.net/search?p=author:' + BAI
if collection == 'published':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Published&rg=250'), 'html.parser')
elif collection == 'all':
    profile = bs(urllib.request.urlopen(inspirehepprofile), 'html.parser')
elif collection == 'citeable':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Citeable&rg=250'), 'html.parser')
elif collection == 'book':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Book&rg=250'), 'html.parser')
elif collection == 'conferencepaper':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:ConferencePaper&rg=250'), 'html.parser')
elif collection == 'introductory':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Introductory&rg=250'), 'html.parser')
elif collection == 'lectures':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Lectures&rg=250'), 'html.parser')
elif collection == 'thesis':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Thesis&rg=250'), 'html.parser')
elif collection == 'review':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Review&rg=250'), 'html.parser')
elif collection == 'proceedings':
    profile = bs(urllib.request.urlopen(inspirehepprofile + '+collection:Proceedings&rg=250'), 'html.parser')

# Find and store the recordids
recordids = []
ids = profile.find_all('a', class_='moreinfo')
for id in range(len(ids)):
    if ids[id].string == 'Detailed record':
        record = ids[id].get('href').replace('/record/','').replace('?ln=en','')
        recordids.append(record)

# Default: from most recent
if order == True:
    recordids.reverse()

totcits = totcitssc = 0

# For each record print the title, the number of citations and the number of citations excluding self cites
for record in range(len(recordids)):
    article = bs(urllib.request.urlopen('https://old.inspirehep.net/record/' + recordids[record]), 'html.parser')
    citations = bs(urllib.request.urlopen('https://old.inspirehep.net/search?ln=en&p=recid:' + recordids[record] + '&of=hcs2'), 'html.parser')
    citesummary = citations.find('table', id='citesummary')
    rows = citesummary.findAll('tr')
    cells = rows[2].findAll('td')
    print('\033[1m' + article.title.string.replace(' - INSPIRE-HEP','') + '\033[0m')
    if collection == 'published':
        print('Number of citations: ' + cells[4].string + '; Excluding self cites: ' + cells[5].string)
        totcits = totcits + int(float(cells[4].string))
        totcitssc = totcitssc + int(float(cells[5].string))
    else:
        print('Number of citations: ' + cells[1].string + '; Excluding self cites: ' + cells[2].string)
        totcits = totcits + int(float(cells[1].string))
        totcitssc = totcitssc + int(float(cells[2].string))

# Print the total number of citations and the total number of citations excluding self cites
if len(recordids) > 0:
    print('Total number of citations: ', totcits, '; Excluding self cites: ', totcitssc, sep='')
