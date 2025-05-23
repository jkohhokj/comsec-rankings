from fastapi import APIRouter, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from collections import Counter
from bs4 import BeautifulSoup
import uvicorn
import re
import json

app = FastAPI()
router = APIRouter()

# Enable CORS (like your previous headers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    "2025": "data/ieee_sp/sec25_contents.html",
}

def extract_universities(line: str):
    unis = set()
    for author in line.split(','):
        match = re.search(r'\((.*?)\)', author)
        if match:
            uni = match.group(1)
            uni = uni.replace("USA", "").replace("United States of America", "").replace("China", "")
            uni = uni.replace("The Netherlands", "").replace("Republic of Korea", "").replace("Switzerland", "")
            if ";" in uni:
                mini = uni.split(";")
                unis.update(map(str.strip, mini))
            elif "/" in uni:
                mini = uni.split("/")
                unis.update(map(str.strip, mini))
            else:
                unis.add(uni.strip())
    return list(unis)

def parse_html(source: str):
    with open(source, 'r', encoding='utf-8', errors="ignore") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    papers = soup.find_all('div', class_='list-group-item')

    total_universities = []
    for paper in papers:
        title_tag = paper.find('b')
        if not title_tag:
            continue
        author_line = title_tag.next_sibling
        while author_line and getattr(author_line, "name", None) != 'br':
            author_line = author_line.next_sibling

        if author_line and author_line.next_sibling:
            author_line = author_line.next_sibling.strip()
        else:
            author_line = ''
        universities = extract_universities(author_line)
        total_universities += universities

    return total_universities

def process_multiple_sources(sources: list):
    total_universities = []
    for source in sources:
        total_universities += parse_html(source)
    return dict(sorted(dict(Counter(total_universities)).items(), key=lambda item: item[1], reverse=True))

@router.get("/")
def get_universities(year_start: Optional[int] = Query(None), year_end: Optional[int] = Query(None)):
    if year_start is not None and year_end is not None:
        selected_files = [
            html_paths[str(year)]
            for year in range(year_start, year_end + 1)
            if str(year) in html_paths
        ]
    else:
        selected_files = list(html_paths.values())

    if not selected_files:
        return {"message": "No data for the given year range"}

    data = process_multiple_sources(selected_files)
    return {"data": data}

app.include_router(router)
# To run this: uvicorn ieee_sp_ranking:app --reload --port 8000
if __name__ == "__main__":
    uvicorn.run("ieee_sp_ranking:app", host="0.0.0.0", port=8000, reload=True)
