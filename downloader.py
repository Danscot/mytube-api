from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class DownloadRequest(BaseModel):
    url: str

@app.post("/download")
def download_video(data: DownloadRequest):
    try:
        ydl_opts = {
            "format": "bestaudio/best",  # Just audio = less bot detection
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # Spoof browser
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return {
                "title": info.get("title"),
                "filename": filename,
                "status": "Downloaded successfully"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
