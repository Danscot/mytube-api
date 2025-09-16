
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse

from ytdl import Ytdl

import os

app = FastAPI()

@app.get("/youtube")

def root():

    return {"message":"Youtube  Downloader Running"}

@app.post("/youtube/download/mp3")

def mp3_downloader(url: str):

    downl = Ytdl(url)

    file = downl.get_mp3()

    if not os.path.exists(file):
        
        return {"error": f"File not found: {file}"}

    return FileResponse(path=file, filename=os.path.basename(file), media_type="audio/mpeg")

