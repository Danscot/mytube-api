@app.post("/download")
async def download_audio(data: dict):
    try:
        url = data.get("url")
        print(f"Received URL: {url}")

        if not url:
            raise HTTPException(status_code=400, detail="URL is required")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_song.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(info['ext'], 'mp3')

        print(f"Sending file: {filename}")

        return FileResponse(filename, media_type='audio/mpeg', filename='song.mp3')

    except Exception as e:
        print("❌ Download failed:", str(e))
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
