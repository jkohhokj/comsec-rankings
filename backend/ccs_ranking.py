import re
from collections import Counter
import json
import fitz  # PyMuPDF

from fastapi import FastAPI, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn


router = APIRouter()

pdf_paths = {
    "2004": "data/ccs/sec04_contents.pdf",
    "2005": "data/ccs/sec05_contents.pdf",
    "2006": "data/ccs/sec06_contents.pdf",
    "2007": "data/ccs/sec07_contents.pdf",
    "2008": "data/ccs/sec08_contents.pdf",
    "2009": "data/ccs/sec09_contents.pdf",
    "2010": "data/ccs/sec10_contents.pdf",
    "2011": "data/ccs/sec11_contents.pdf",
    "2012": "data/ccs/sec12_contents.pdf",
    "2013": "data/ccs/sec13_contents.pdf",
    "2014": "data/ccs/sec14_contents.pdf",
    "2015": "data/ccs/sec15_contents.pdf",
    "2016": "data/ccs/sec16_contents.pdf",
    "2017": "data/ccs/sec17_contents.pdf",
    "2018": "data/ccs/sec18_contents.pdf",
    "2019": "data/ccs/sec19_contents.pdf",
    "2020": "data/ccs/sec20_contents.pdf",
    "2021": "data/ccs/sec21_contents.pdf",
    "2022": "data/ccs/sec22_contents.pdf",
    "2023": "data/ccs/sec23_contents.pdf",
    "2024": "data/ccs/sec24_contents.pdf"
}


def extract_all_text(pdf_path):
    """Extracts all text from a PDF file using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text from each page

    text = text.split("Organization")[1] # only get people who published
    text = text.split("Poster")[0].split("POSTER")[0]
    return text

# Function to split the paper text into blocks, each separated by a delimiter line (e.g., ". . . x")
def split_papers(text):
    # Regular expression to detect delimiter lines (lines with ". . . x" where x is an integer)
    delimiter_pattern = r".*\.\.\.+\s*\d+"

    # Split the input text into lines
    lines = text.split("\n")
    blocks = []  # List to hold the blocks of text
    current_block = []  # Temporary list to store lines for the current block

    for line in lines:
        if re.match(delimiter_pattern, line):
            if current_block:
                blocks.append("\n".join(current_block))  # Save the previous block
            current_block = [line]  # Start a new block with the delimiter line
        else:
            current_block.append(line)  # Add line to the current block

    # Append the last block if exists
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks


def display_stats(total_authors, total_universities):

  # Create frequency dictionaries for authors and universities
  author_frequency = dict(Counter(total_authors))
  university_frequency = dict(Counter(total_universities))

  # Print the sorted frequency dictionaries from greatest to least
  print("Author Frequency (sorted):")
  print(dict(sorted(author_frequency.items(), key=lambda item: item[1], reverse=True)))

  print("University Frequency (sorted):")
  print(dict(sorted(university_frequency.items(), key=lambda item: item[1], reverse=True)))


def parse_blocks(blocks, total_authors, total_universities):
  # Loop through each block of paper text
    for i, block in enumerate(blocks, 1):
        matches = re.findall(r"\(([^)]+)\)", block)
        university_list = list(set(matches))

        author_list = []
        # Clean up the author and university lists by removing leading/trailing spaces and duplicates
        author_list = [s.strip() for s in author_list if s.strip()]
        author_list = list(dict.fromkeys(author_list))  # Remove duplicates while preserving order
        university_list = [s.strip() for s in university_list if s.strip()]
        university_list = list(dict.fromkeys(university_list))  # Remove duplicates while preserving order

        # Add the authors and universities to the totals
        total_authors += author_list
        total_universities += university_list


    #   display_stats(total_authors, total_universities)
    return total_authors, total_universities


def process_multiple_sources(pdf_paths):
    # Initialize lists to store authors and universities across all blocks
    total_authors = []
    total_universities = []
    university_frequency = {}
    for pdf_path in pdf_paths:
        extracted_text = extract_all_text(pdf_path)
        blocks = split_papers(extracted_text)
        parse_blocks(blocks, total_authors, total_universities)

    university_frequency = dict(Counter(total_universities))
    return dict(sorted(university_frequency.items(), key=lambda item: item[1], reverse=True))
        

@router.get("/")
def get_universities(year_start: Optional[int] = Query(None), year_end: Optional[int] = Query(None)):
    if year_start is not None and year_end is not None:
        selected_files = [
            pdf_paths[str(year)]
            for year in range(year_start, year_end + 1)
            if str(year) in pdf_paths
        ]
    else:
        selected_files = list(pdf_paths.values())

    if not selected_files:
        return {"message": "No data for the given year range"}

    data = process_multiple_sources(selected_files)
    return {"data": data}
app = FastAPI()
app.include_router(router)

# To run this: uvicorn yourfilename:app --reload --port 8000
#if __name__ == "__main__":
#    uvicorn.run("ccs_ranking:app", host="0.0.0.0", port=8000, reload=True)
