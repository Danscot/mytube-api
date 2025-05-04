from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from downloader import download_audio
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "YouTube Downloader API running"}

@app.post("/download")
async def download_youtube(url: str = Form(...)):
    try:
        file_path = download_audio(url)
        return FileResponse(file_path, media_type="audio/mpeg", filename=os.path.basename(file_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
