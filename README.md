# examPDFmerger
A simple script for merging multiple exam PDFs downloaded from a platform like RU's Brightspace into a single file for printing.
Adds a watermark with RU student numbers and optionally different exam version (inferred from the folder structure) onto each page.
Inserts empty pages to allow for convenient duplex printing.
Python 2.7 due to library availabilty.


## Example use
pip install -r requirements.txt
python merger.py SOURCE_DIRECTORY NAME.pdf

Will merge the files under SOURCE_DIRECTORY and store the results in NAME.pdf in the same directory.

Note that the folder structure currently has to look as follows 

    ├── SOURCE_DIRECTORY
			├──VERSION 1
				├──SUBMISSION DIRECTORY
				├──SUBMISSION DIRECTORY
			├──VERSION 2
				├──SUBMISSION DIRECTORY
and so on.

If you only have a single version, make sure to add a folder as to conform to the structure, e.g.

    ├── SOURCE_DIRECTORY
			├──DUMMY FOLDER
				├──SUBMISSION DIRECTORY
				├──SUBMISSION DIRECTORY
				
## Known issues
* Does not automatically infer correct folder structure
* Only works for RU student numbers
