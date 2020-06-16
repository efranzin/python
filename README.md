# Python scripts

## `citations.py`

Given an author identified by his/her BAI, this simple Python3 script counts the number of citations and the number of citations excluding self cites in the [Inspirehep](http://inspirehep.net/) database for each paper in a given collection.

**Usage:**

`citations.py [-b|--BAI=<BAI>] [-y|--year=<YEAR>] [-c|--collection=<COLLECTION>] [-r|--reversed] [-h|--help]`

**Options:**
* `-b <BAI>, --BAI=<BAI>`, specifies the author's BAI identifier
* `-y <YEAR>, --year=<YEAR>`, specifies the year
* `-c <COLLECTION>, --collection=<COLLECTION>`, specifies the collection: all, book, bookchapter, conferencepaper, introductory, lectures, proceedings, published, review, thesis
* `-r, --reversed`, sorts the items in chronological order

Default values are `E.Franzin.1` for the BAI, `published` for the collection and all the corresponding items in the Inspirehep database are sorted from the most recent.
