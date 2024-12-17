import os
import psycopg2
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        result = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port,
            sslmode="require"
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/dramas/")
async def list_dramas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, genre, country, streaming_platform, status, personal_ranking
            FROM dramas;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        dramas = [
            {
                "id": row[0],
                "name": row[1],
                "genre": row[2],
                "country": row[3],
                "streaming_platform": row[4],
                "status": row[5],
                "personal_ranking": row[6]
            }
            for row in rows
        ]
        return dramas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dramas: {e}")

@app.get("/dramas/total-watched")
async def total_watched():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM dramas 
            WHERE watched_count_this_year > 0;
        """)
        total = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating total watched dramas: {e}")
