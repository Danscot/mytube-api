from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from yt_mp3 import Yt_mp3
from yt_mp4 import Yt_mp4
from search import YtSearch
import os
import unicodedata

app = FastAPI(title="Danscot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def safe_filename(title: str) -> str:
    # Normalize and remove invalid filename characters
    safe = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('ascii')
    safe = ''.join(c for c in safe if c.isalnum() or c in (' ', '-', '_')).strip()
    return safe if safe else "untitled"

@app.get("/")
def root():
    return {"message": "API system is running."}

@app.get("/youtube/mp3")
def yt_mp3(url: str):
    try:
        downloader = Yt_mp3(url)
        file_path, title = downloader.get_mp3()
        filename = f"{safe_filename(title)}.mp3"
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Video-Title": title.encode("utf-8", "ignore").decode("utf-8")
            }
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/youtube/mp4")
def yt_mp4(url: str = Query(...)):
    try:
        downloader = Yt_mp4(url)
        file_path, title = downloader.download()
        filename = f"{safe_filename(title)}.mp4"
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="video/mp4",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Video-Title": title.encode("utf-8", "ignore").decode("utf-8")
            }
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/youtube/search")
def search(query: str = Query(...)):
    try:
        searcher = YtSearch(query, api_key="AIzaSyDV11sdmCCdyyToNU-XRFMbKgAA4IEDOS0")
        results = searcher.search()
        return {"results": results}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
