# main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from usenix_ranking import app as usenix_app
from ieee_sp_ranking import app as ieee_sp_app
from top_ranking import app as top_app
from ccs_ranking import app as ccs_app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend.yoursite.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-APIs
app.mount("/usenix", usenix_app)
app.mount("/ieee_sp", ieee_sp_app)
app.mount("/top", top_app)
app.mount("/ccs", ccs_app)

