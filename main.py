
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse

from downl import downl

app = FastAPI()

@app.get("/youtube")

def root():

    return {"message":"Youtube  Downloader Running"}

@app.post("/youtube/download/{url}")

def downloader(url:str):

    downl = Downl()

    file = downl.get_mp3(url)

    return FileResponse(file_path)




