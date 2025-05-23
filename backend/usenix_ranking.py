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
    "2015": "data/usenix/sec15_contents.pdf",
    "2016": "data/usenix/sec16_contents.pdf",
    "2017": "data/usenix/sec17_contents.pdf",
    "2018": "data/usenix/sec18_contents.pdf",
    "2019": "data/usenix/sec19_contents.pdf",
    "2020": "data/usenix/sec20_contents.pdf",
    "2021": "data/usenix/sec21_contents.pdf",
    "2022": "data/usenix/sec22_contents.pdf",
    "2023": "data/usenix/sec23_contents.pdf",
    "2024": "data/usenix/sec24_contents.pdf"
}

def extract_all_text(pdf_path):
    """Extracts all text from a PDF file using PyMuPDF (fitz)."""
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text from each page

    return text

# Function to split the paper text into blocks, each separated by a delimiter line (e.g., ". . . x")
def split_papers(text):
    # Regular expression to detect delimiter lines (lines with ". . . x" where x is an integer)
    delimiter_pattern = r"^.*\.\s+\.\s+\.\s+\d+$"

    # Split the input text into lines
    lines = text.split("\n")
    blocks = []  # List to hold the blocks of text
    current_block = []  # Temporary list to store lines for the current block

    for line in lines:
        # If a delimiter line is found, start a new block
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
      # print(f"Block {i}:\n{block}\n")

      # Extract the title (first sentence before a period)
      title = block.split('\n')[0].split('.')[0]

      # Join the rest of the block content (credentials) into a single string
      credentials = ''.join(block.split('\n')[1:])

      # Split the credentials into groups based on the semicolon delimiter
      university_groups = credentials.split(';')

      # Initialize empty lists to hold authors and universities
      author_list = []
      university_list = []

      # Loop through each university group and extract authors and universities
      for university_group in university_groups:
          university_group = university_group.split(',')

          if "and" not in ''.join(university_group):
              # If no "and" found, assume first part is the author
              author_list.append(university_group[0])
              university_list.append(','.join(university_group[1:]))
          else:
              # Split the authors and universities at "and"
              i = 0
              while 'and' not in university_group[i]:
                  author_list.append(university_group[i])
                  i += 1
              author_list += university_group[i].split(' and ')
              university_list.append(','.join(university_group[i+1:]))

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
#    uvicorn.run("usenix_ranking:app", host="0.0.0.0", port=8000, reload=True)
