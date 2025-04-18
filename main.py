import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import uuid

app = FastAPI()

# Create output folder if it doesn't exist
DOWNLOAD_DIR = "Download__"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Request body schema
class VideoURL(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "✅ MyTube API is up and running!"}

@app.post("/download")
def download_audio(data: VideoURL):
    video_url = data.url

    # Generate a unique filename to avoid clashes
    temp_filename = f"{uuid.uuid4()}.%(ext)s"
    output_template = os.path.join(DOWNLOAD_DIR, temp_filename)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "ignoreerrors": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9",
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get("title", "audio")
            filename = ydl.prepare_filename(info)
            mp3_file = filename.rsplit(".", 1)[0] + ".mp3"

            if os.path.exists(mp3_file):
                return FileResponse(mp3_file, media_type="audio/mpeg", filename=f"{title}.mp3")
            else:
                raise HTTPException(status_code=500, detail="Download failed or file not found")

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Download failed")
