from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import yt_dlp

app = FastAPI()

# Ensure output directory exists
output_directory = 'Download__'
os.makedirs(output_directory, exist_ok=True)

# Request body model
class VideoURL(BaseModel):
    url: str

# Progress hook (optional)
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('speed', 0)
        print(f"Downloading: {percent} at {speed / 1024:.2f} KB/s")
    elif d['status'] == 'finished':
        print(f"✅ Finished downloading: {d['filename']}")

# Download function
def download_audio_from_video(video_url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'cookiefile': 'cookies.txt',  # 👈 Use your exported cookies.txt here
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Root endpoint (optional)
@app.get("/")
def root():
    return {"message": "Welcome to MyTube Downloader API 🎵"}

# Download endpoint
@app.post("/download")
def download_video(data: VideoURL):
    try:
        download_audio_from_video(data.url)
        return {"status": "success", "message": "Download completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
