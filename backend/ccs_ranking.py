import re
from collections import Counter
import json
import fitz  # PyMuPDF


from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

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
        



class handler(BaseHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Allow methods
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')  # Allow headers
        super().end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight request
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_GET(self):
        # Parse query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        year_start = query_params.get('year_start', [None])[0]
        year_end = query_params.get('year_end', [None])[0]

        try:
            year_start = int(year_start) if year_start is not None else None
            year_end = int(year_end) if year_end is not None else None
        except ValueError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid year_start or year_end"}).encode('utf-8'))
            return

        # Filter valid years within the range
        selected_pdfs = []
        if year_start and year_end:
            for year in range(year_start, year_end+1):
                key = str(year)
                if key in pdf_paths:  # Assuming pdf_paths is defined elsewhere
                    selected_pdfs.append(pdf_paths[key])
        if selected_pdfs:
            data = process_multiple_sources(selected_pdfs)  # Assuming process_pdfs is defined elsewhere
        else:
            data = {"message": "No data for the given year range"}

        # Respond with JSON data
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({"data": data}).encode("utf-8")
        self.wfile.write(response)


if __name__ == "__main__":
    server_address = ('', 8002)
    httpd = HTTPServer(server_address, handler)
    print("Server running on http://localhost:8002")
    httpd.serve_forever()
