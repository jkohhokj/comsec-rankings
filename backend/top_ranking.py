from ieee_sp_ranking import process_multiple_sources as process_ieee_sp
from usenix_ranking import process_multiple_sources as process_usenix
from ccs_ranking import process_multiple_sources as process_ccs
from ieee_sp_ranking import html_paths as paths_ieee_sp
from usenix_ranking import pdf_paths as paths_usenix
from ccs_ranking import pdf_paths as paths_ccs


import json
import string
from collections import defaultdict

from fastapi import APIRouter, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn


router = APIRouter()
app = FastAPI()



# Enable CORS (like your previous headers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/")
def get_universities(year_start: Optional[int] = Query(None), year_end: Optional[int] = Query(None)):
    if year_start is not None and year_end is not None:
        selected_files = [
            paths_usenix[str(year)]
            for year in range(year_start, year_end + 1)
            if str(year) in paths_usenix
        ]
    else:
        selected_files = list(paths_usenix.values())

    data_usenix = process_usenix(selected_files)

    if year_start is not None and year_end is not None:
        selected_files = [
            paths_ieee_sp[str(year)]
            for year in range(year_start, year_end + 1)
            if str(year) in paths_ieee_sp
        ]
    else:
        selected_files = list(paths_ieee_sp.values())

    data_ieee_sp = process_ieee_sp(selected_files)
    
    if year_start is not None and year_end is not None:
        selected_files = [
            paths_ccs[str(year)]
            for year in range(year_start, year_end + 1)
            if str(year) in paths_ccs
        ]
    else:
        selected_files = list(paths_ccs.values())

    data_ccs = process_ccs(selected_files)
   


    data_combined = defaultdict(int)
    for d in [data_usenix, data_ieee_sp, data_ccs]:
        for k, v in d.items():
            data_combined[k] += v
    data = dict(data_combined)
    return {"data": data}
app.include_router(router)
# To run this: uvicorn yourfilename:app --reload --port 8000
if __name__ == "__main__":
    uvicorn.run("combined_ranking:app", host="0.0.0.0", port=8000, reload=True)
