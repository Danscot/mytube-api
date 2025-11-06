
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from yt_mp3 import Yt_mp3

from yt_mp4 import Yt_mp4

from search import YtSearch

import os

app = FastAPI(title="Danscot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")

def root():

    return {"message":"Api system is running."}

@app.get("/youtube/mp3")

def yt_mp3(url: str):

    downl = Yt_mp3(url)

    file = downl.get_mp3()

    if not os.path.exists(file):

        return {"error": f"File not found: {file}"}

    return FileResponse(path=file, filename=os.path.basename(file), media_type="audio/mpeg")
    
    
@app.get("/youtube/mp4")

def mp4_download(url: str = Query(...)):
    try:
        downloader = Yt_mp4(url)
        file = downloader.download()
        return FileResponse(file, filename=os.path.basename(file), media_type="video/mp4")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/youtube/search")
def search(query: str = Query(...)):
    try:
        searcher = YtSearch(query)
        results = searcher.search()
        return {"results": results}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
 
