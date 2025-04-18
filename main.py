import os
import yt_dlp
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

DOWNLOAD_DIR = "Download__"
COOKIE_FILE = "cookies.txt"  # If using cookies

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

def get_ydl_opts(output_path):
    return {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': COOKIE_FILE if os.path.exists(COOKIE_FILE) else None,
        'quiet': True,
        'no_warnings': True,
    }

@app.get("/")
def root():
    return {"status": "OK", "message": "YouTube Audio Downloader API"}

@app.post("/download")
async def download_audio(request: DownloadRequest):
    url = request.url
    try:
        # Temporary output path with title placeholder
        output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        ydl_opts = get_ydl_opts(output_path)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title")
            if not title:
                return JSONResponse(status_code=500, content={"detail": "Failed to extract title"})

            mp3_path = os.path.join(DOWNLOAD_DIR, f"{title}.mp3")
            if os.path.exists(mp3_path):
                return FileResponse(mp3_path, media_type="audio/mpeg", filename=f"{title}.mp3")
            else:
                return JSONResponse(status_code=500, content={"detail": "Download completed, but file not found."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Download failed: {str(e)}"})
