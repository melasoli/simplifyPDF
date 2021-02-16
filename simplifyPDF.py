'''
A simple tool to remove duplicate or near-duplicate PDF pages by comparing extracted text.
'''

from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz
import easygui
import re

# File browser to open a file
inFile = easygui.fileopenbox(msg='Open a PDF file', title='File Browser', filetypes=['*.pdf', 'PDF Files'])

# File browser to save the file
outFile = easygui.filesavebox(msg='Save the PDF file', title='File Browser', filetypes=["*.pdf", 'PDF Files'])

# Keep track of pages to keep
keepPages = []

with open(inFile, 'rb') as f:
    reader = PdfFileReader(f)
    numOfPages = reader.getNumPages()

    for pageNum in range(numOfPages-1):
        # Get current page and next page
        currPage = reader.getPage(pageNum)
        nextPage = reader.getPage(pageNum+1)

        # Extract Text from both current and next page
        currText = currPage.extractText().strip()
        nextText = nextPage.extractText().strip()
       
        # Keep current page if next page doesn't already contain all text on current page
        if (currText not in nextText):
            keepPages.append(pageNum)

        # Sub-topic pages with titles that are used on the next page do not have page numbers written on the page
        elif (re.search("\n[0-9][0-9]*$", currText, re.MULTILINE) == None):
            keepPages.append(pageNum)

    # Remember to add last page
    keepPages.append(numOfPages-1)

# Create a new file using the page numbers of pages to keep
pdf = fitz.open(inFile)
pdf.select(keepPages)
pdf.save(outFile)
pdf.close()