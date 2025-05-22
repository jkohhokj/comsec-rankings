import requests
headers = {
    'If-None-Match': '"O0qEMh7+oA1ckgB5O2uwzyYyhiA="',
    'Referer': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'If-Modified-Since': 'Tue, 01 Jan 1980 00:00:00 GMT',
}
### USENIX
def get_usenix():
    for year in range(2015,2024):
        r = requests.get(f"https://www.usenix.org/sites/default/files/sec{str(year)[2:]}_contents.pdf", headers=headers)
        with open(f"data/test/sec{str(year)[2:]}_contents.pdf","wb") as f:
            f.write(r.content)

# get_usenix()

### IEEE S&P
def get_ieee_sp():
    for year in range(2016,2026):
        r = requests.get(f"https://www.ieee-security.org/TC/SP{year}/program-papers.html", headers=headers)
        with open(f"data/ieee_sp/sec{str(year)[2:]}_contents.html","w", errors='ignore') as f:
            f.write(r.text)

# get_ieee_sp()

### ACM CCS
# CCS requires a little more effort, the pages are listed as downloadable PDFs but it's more complicated than downloading HTML.
# Additionally finding the exact page requires going onto the website to find the corresponding paper ID.

# The list of paper IDs can be found here https://dl.acm.org/conference/ccs/proceedings


# Currently a WIP, figure out how to bypass botting restriction
ccs_ids = {
    "2001" : "501983",
    "2002" : "586110",
    "2003" : "948109",
    "2004" : "1030083",
    "2005" : "1102120",
    "2006" : "1180405",
    "2015" : "2810103",
}

def get_ccs():
    for year in range(2015,2016):
        params = {
            'doi': '10.1145/2810103',
        }
        r = requests.get('https://dl.acm.org/action/showFmPdf', params=params, headers=headers)
        print(r.status_code)
        with open(f"data/test/ccssec{str(year)[2:]}_contents.pdf","wb") as f:
            f.write(r.content)

get_ccs()

