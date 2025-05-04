from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import httpx
import os
import uuid

app = FastAPI()

# New server URL (Server 2)
NEW_SERVER_URL = "https://mytube-api-1.onrender.com"

@app.get("/")
def root():
    return {"message": "YouTube Downloader Proxy API running"}

@app.post("/download")
async def download_video(data: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{NEW_SERVER_URL}/download",
                data={"url": data["url"]},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

        if response.status_code == 200:
            temp_filename = f"/tmp/{uuid.uuid4()}.mp3"
            with open(temp_filename, "wb") as f:
                f.write(response.content)

            return FileResponse(temp_filename, media_type="audio/mpeg", filename="downloaded_song.mp3")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to download: {response.text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy failed: {str(e)}")

