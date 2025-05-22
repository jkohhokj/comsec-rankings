from ieee_sp_ranking import process_multiple_sources as process_ieee
from usenix_ranking import process_multiple_sources as process_usenix
from ccs_ranking import process_multiple_sources as process_ccs
from ieee_sp_ranking import html_paths as paths_ieee
from usenix_ranking import pdf_paths as paths_usenix
from ccs_ranking import pdf_paths as paths_ccs


import json
import string
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


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
                if key in paths_usenix:  # Assuming pdf_paths is defined elsewhere
                    selected_pdfs.append(paths_usenix[key])
        if selected_pdfs:
            data_usenix = process_usenix(selected_pdfs)  # Assuming process_pdfs is defined elsewhere
        else:
            data_usenix = {}
        # Filter valid years within the range
        selected_pdfs = []
        if year_start and year_end:
            for year in range(year_start, year_end+1):
                key = str(year)
                if key in paths_ieee:  # Assuming pdf_paths is defined elsewhere
                    selected_pdfs.append(paths_ieee[key])
        if selected_pdfs:
            data_ieee = process_ieee(selected_pdfs)  # Assuming process_pdfs is defined elsewhere
        else:
            data_ieee = {}


        # Filter valid years within the range
        selected_pdfs = []
        if year_start and year_end:
            for year in range(year_start, year_end+1):
                key = str(year)
                if key in paths_ccs:  # Assuming pdf_paths is defined elsewhere
                    selected_pdfs.append(paths_ccs[key])
        if selected_pdfs:
            data_ccs = process_ccs(selected_pdfs)  # Assuming process_pdfs is defined elsewhere
        else:
            data_ccs = {}

        data_combined = defaultdict(int)
        for d in [data_usenix, data_ieee, data_ccs]:
            for k, v in d.items():
                data_combined[k] += v

        # Respond with JSON data
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({"data": dict(data_combined)}).encode("utf-8")
        self.wfile.write(response)


if __name__ == "__main__":
    server_address = ('', 8003)
    httpd = HTTPServer(server_address, handler)
    print("Server running on http://localhost:8003")
    httpd.serve_forever()
