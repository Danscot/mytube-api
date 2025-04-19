from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import os
import uuid

app = FastAPI()

@app.post("/download")
async def download_audio(data: dict):
    try:
        url = data.get("url")
        print(f"🎯 Received URL: {url}")

        if not url:
            raise HTTPException(status_code=400, detail="URL is required")

        file_id = str(uuid.uuid4())
        base_filename = f"{file_id}.%(ext)s"
        final_mp3 = f"{file_id}.mp3"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': base_filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"✅ File ready: {final_mp3}")
        return FileResponse(final_mp3, media_type='audio/mpeg', filename='song.mp3')

    except Exception as e:
        print(f"❌ Download failed: {e}")
        raise HTTPException(status_code=500, detail=f"Download failed: {e}")

    finally:
        if os.path.exists(final_mp3):
            os.remove(final_mp3)
