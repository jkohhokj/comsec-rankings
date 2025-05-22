from bs4 import BeautifulSoup
import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from collections import Counter



html_paths = {
    "2016": "data/ieee_sp/sec16_contents.html",
    "2017": "data/ieee_sp/sec17_contents.html",
    "2018": "data/ieee_sp/sec18_contents.html",
    "2019": "data/ieee_sp/sec19_contents.html",
    "2020": "data/ieee_sp/sec20_contents.html",
    "2021": "data/ieee_sp/sec21_contents.html",
    "2022": "data/ieee_sp/sec22_contents.html",
    "2023": "data/ieee_sp/sec23_contents.html",
    "2024": "data/ieee_sp/sec24_contents.html",
    "2025": "data/ieee_sp/sec25_contents.html"
}



def extract_universities(line):
    unis = set()
    for author in line.split(','):
        match = re.search(r'\((.*?)\)', author)
        if match:
            uni = match.group(1)
            uni = uni.replace("USA","").replace("United States of America","").replace("China","")
            uni = uni.replace("The Netherlands","").replace("Republic of Korea","").replace("Switzerland","")
            if ";" in uni: # there might be multiple associations
                mini = uni.split(";")
                unis.add(mini[0].strip())
                unis.add(mini[1].strip())
            elif "/" in uni: # there might be multiple associations
                mini = uni.split("/")
                unis.add(mini[0].strip())
                unis.add(mini[1].strip())
            else:
                unis.add(uni.strip())
    return list(unis)
        

def parse_html(source):
 # Read HTML
    with open(source, 'r', encoding='utf-8', errors="ignore") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the papers (they are inside divs with class list-group-item)
    papers = soup.find_all('div', class_='list-group-item')

    total_universities = []
    # Process each paper
    for paper in papers:
        title_tag = paper.find('b')
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)

        # The rest of the text (after <br />)
        author_line = title_tag.next_sibling
        while author_line and author_line.name != 'br':
            author_line = author_line.next_sibling

        if author_line and author_line.next_sibling:
            author_line = author_line.next_sibling.strip()
        else:
            author_line = ''
        universities = extract_universities(author_line)
        total_universities += universities


    return total_universities

def process_multiple_sources(sources):
    total_universities = []
    for source in sources:
        total_universities += parse_html(source)
    
    university_frequency = {}
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
                if key in html_paths:  # Assuming pdf_paths is defined elsewhere
                    selected_pdfs.append(html_paths[key])
        print(selected_pdfs)
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
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler)
    print("Server running on http://localhost:8000")
    # print(process_multiple_sources([html_paths['2020'],html_paths['2021']]))
    httpd.serve_forever()
