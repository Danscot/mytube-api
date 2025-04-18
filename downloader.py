from fastapi.responses import FileResponse

@app.post("/download")
def download_video(data: VideoURL):
    try:
        # Download video
        download_audio_from_video(data.url)

        # Find the last downloaded .mp3 file
        files = sorted(
            [f for f in os.listdir(output_directory) if f.endswith(".mp3")],
            key=lambda x: os.path.getmtime(os.path.join(output_directory, x)),
            reverse=True
        )

        if not files:
            raise Exception("No MP3 file found after download.")

        last_file = os.path.join(output_directory, files[0])
        return FileResponse(last_file, media_type="audio/mpeg", filename=files[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
