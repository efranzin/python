#!/usr/bin/env python3

"""
Given an author identified by his/her BAI, this simple Python3 script counts the
number of citations and the number of citations excluding self cites in the
Inspirehep database (https://inspirehep.net/) for each paper in a given collection.
"""

__author__ = 'Edgardo Franzin'
__version__ = '2.2'
__license__ = 'GPL'
__email__ = 'edgardo<dot>franzin<at>gmail<dot>com'


import sys
from optparse import OptionParser

# Parse options
usage = sys.argv[0] + ' [-b|--BAI=<BAI>] [-y|--year=<YEAR>] [-c|--collection=<COLLECTION>] [-r|--reversed] [-h|--help]'

parser = OptionParser(usage)

parser.add_option('-b', '--BAI', dest='BAI',
                  help='BAI identifier; default: E.Franzin.1', default='E.Franzin.1')
parser.add_option('-y', '--year', dest='year',
                  help='results for a given year')
parser.add_option('-c', '--collection', dest='collection',
                  help='collections: all, book, bookchapter, conferencepaper, introductory, lectures, proceedings, published, review, thesis; default: published', default='published')
parser.add_option('-r', '--reversed', action='store_true', dest='order',
                  help='list the items in chronological order')

(options, args) = parser.parse_args()

BAI = options.BAI
year = options.year
collection = options.collection
order = options.order

# Import the modules to open and reading URLs and the JSON encoder
import urllib.request, json

# Open the INSPIRE-HEP profile
inspirehep_profile = 'https://inspirehep.net/api/literature?sort=mostrecent&size=1000&q=a%20' + BAI

# Select the year
if year is not None:
    inspirehep_profile = inspirehep_profile + '%20date%20' + year

# Select the collection
if collection == 'published':
    inspirehep_profile = inspirehep_profile + '&doc_type=published'
elif collection == 'all':
    inspirehep_profile = inspirehep_profile
elif collection == 'book':
    inspirehep_profile = inspirehep_profile + '&doc_type=book'
elif collection == 'bookchapter':
    inspirehep_profile = inspirehep_profile + '&doc_type=book%20chapter'
elif collection == 'conferencepaper':
    inspirehep_profile = inspirehep_profile + '&doc_type=conference%20paper'
elif collection == 'introductory':
    inspirehep_profile = inspirehep_profile + '&doc_type=introductory'
elif collection == 'lectures':
    inspirehep_profile = inspirehep_profile + '&doc_type=lectures'
elif collection == 'thesis':
    inspirehep_profile = inspirehep_profile + '&doc_type=thesis'
elif collection == 'review':
    inspirehep_profile = inspirehep_profile + '&doc_type=review'
elif collection == 'proceedings':
    inspirehep_profile = inspirehep_profile + '&doc_type=proceedings'

# Load the data
data = json.loads(urllib.request.urlopen(inspirehep_profile).read())
total_hits = data['hits']['total']

# Sorting: default is from most recent
hits = range(total_hits)
if order == True:
    hits = reversed(range(total_hits))

# For each record print the title, the number of citations and the number of citations excluding self cites
totcits = totcits_noself = totcits_published = totcits_noself_published = 0

for i in hits:
    title = data['hits']['hits'][i]['metadata']['titles'][0]['title']
    cits = data['hits']['hits'][i]['metadata']['citation_count']
    cits_noself = data['hits']['hits'][i]['metadata']['citation_count_without_self_citations']
    if 'refereed' in data['hits']['hits'][i]['metadata']:
        totcits_published = totcits_published + cits
        totcits_noself_published = totcits_noself_published + cits_noself
    print('\033[1m' + title + '\033[0m')
    print('Number of citations: ', cits, '; Excluding self cites: ', cits_noself, sep='')
    totcits = totcits + cits
    totcits_noself = totcits_noself + cits_noself

# Print the total number of citations and the total number of citations excluding self cites
if total_hits > 0:
    print('\nTotal number of citations: ', totcits, '; Excluding self cites: ', totcits_noself, sep='')
if collection == 'all':
    print('Total number of citations: ', totcits_published, '; Excluding self cites: ', totcits_noself_published, ' (Published only)', sep='')
