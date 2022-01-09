'''
A simple tool to remove duplicate or near-duplicate PDF pages by comparing extracted text.
'''

import fitz
import easygui
import re

# File browser to open a file
inFile = easygui.fileopenbox(msg='Open a PDF file', title='File Browser', filetypes=['*.pdf', 'PDF Files'])

# File browser to save the file
outFile = easygui.filesavebox(msg='Save the PDF file', title='File Browser', filetypes=["*.pdf", 'PDF Files'])

# Keep track of pages to keep
keepPages = []

# Open file
f = fitz.open(inFile)

numOfPages = f.page_count

for pageNum in range(numOfPages-1):
    # Get current page and next page
    currPage = f[pageNum]
    nextPage = f[pageNum+1]

    # Extract text from both current and next page
    # Remove all whitespaces
    currText = currPage.get_text("text").encode("ascii", "ignore").decode('ascii')
    nextText = nextPage.get_text("text").encode("ascii", "ignore").decode('ascii')

    currStrip = re.sub(r"(\s|[0-9]+$)", "", currText)
    nextStrip = re.sub(r"(\s|[0-9]+$)", "", nextText)

    # Keep current page if next page doesn't already contain all text on current page
    if (currStrip not in nextStrip):
        keepPages.append(pageNum)

    # Sub-topic pages with titles that are used on the next page do not have page numbers written on the page
    elif (re.search("\n[0-9][0-9]*$", currText, re.MULTILINE) == None):
        keepPages.append(pageNum)

# Remember to add last page
keepPages.append(numOfPages-1)

# Create a new file using the page numbers of pages to keep
f.select(keepPages)
f.save('{0}.pdf'.format(outFile))
f.close()