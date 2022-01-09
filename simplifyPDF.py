'''
A simple tool to remove duplicate or near-duplicate PDF pages by comparing extracted text.
'''

import fitz 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re

# Open main window
window = tk.Tk()
window.geometry('300x100')
window.title('simplifyPDF')

# Open file, select pages that have only "complete" content, save file
def keepPages():

    # File browser to open a file
    inFile = askopenfilename(filetypes=[('PDF Files', '*.pdf')])

    # File browser to save the file
    outFile = asksaveasfilename(filetypes=[('PDF Files', '*.pdf')])

    # Keep track of pages to keep
    toKeep = []

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
            toKeep.append(pageNum)

        # Sub-topic pages with titles that are used on the next page do not have page numbers written on the page
        elif (re.search("\n[0-9][0-9]*$", currText, re.MULTILINE) == None):
            toKeep.append(pageNum)

    # Remember to add last page
    toKeep.append(numOfPages-1)

    # Create a new file using the page numbers of pages to keep
    f.select(toKeep)
    f.save('{0}.pdf'.format(outFile))
    f.close()

# Add button to open file browser
btn = ttk.Button(window, text="Open PDF File", command=lambda : keepPages())
btn.pack(side='top', pady=20)

window.mainloop()