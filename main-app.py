from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(default_response_class=ORJSONResponse)

app.mount("/static", StaticFiles(directory="./localstatic"), name="static")

templates = Jinja2Templates(directory="./localstatic")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})