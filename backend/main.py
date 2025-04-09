from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from neo4j import Driver

from router import faq

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

app.include_router(faq.router)