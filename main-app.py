import os
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.responses import ORJSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
import orjson
import psycopg2
from psycopg2.pool import ThreadedConnectionPool


def read_json_file(file_path):
    with open(file_path, "rb") as file:
        data = orjson.loads(file.read())
    return data

# Database connection details
DB_CONFIG = read_json_file("db_config.json")
pool = ThreadedConnectionPool(minconn=1, maxconn=10, **DB_CONFIG)
app = FastAPI(default_response_class=ORJSONResponse)

@app.on_event("shutdown")
def close_pool():
    pool.closeall()

app.mount("/static", StaticFiles(directory="./localstatic"), name="static")

templates = Jinja2Templates(directory="./localstatic")

@app.get("/")
async def root(request: Request):
    try:
        conn = pool.getconn()
        cursor = conn.cursor()
        cursor.execute("SELECT heading_title, description, circular_image FROM data_home;")
        rows = cursor.fetchall()
        cursor.close()
        pool.putconn(conn)
        return templates.TemplateResponse("index.html", {"request": request, "data": rows})
    except Exception as e:
        return {"error": str(e)}