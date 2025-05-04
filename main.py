from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import yt_dlp

app = FastAPI()

#curl -X POST https://mytube-api-3s7w.onrender.com/download   -H "Content-Type: application/json"   -d '{"url": "https://www.youtube.com/watch?v=XTB_s1E6BRA"}'   --output laugh.mp3


output_directory = 'Download__'
os.makedirs(output_directory, exist_ok=True)

class VideoURL(BaseModel):
    url: str

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('speed') or 0
        elapsed = d.get('elapsed') or 0
        eta = d.get('eta') or 0
        print(f"Downloading: {percent} at {speed / 1024:.2f} KB/s, Elapsed: {elapsed:.2f}s, ETA: {eta:.2f}s")
    elif d['status'] == 'finished':
        print(f"✅ Finished downloading: {d['filename']}")

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
        'cookiefile': 'cookies.txt',
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

@app.get("/")
def root():
    return {"message": "Welcome to MyTube Downloader API 🎵"}

@app.post("/download")
def download_video(data: VideoURL):
    try:
        download_audio_from_video(data.url)
        return {"status": "success", "message": "Download completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
        
        
