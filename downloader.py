import yt_dlp
import os
import uuid

def download_audio(url):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.%(ext)s"
    output_path = os.path.join(output_dir, filename)
    final_path = ""

    yt_dlp_options = {
    "format": "bestaudio/best",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        base = ydl.prepare_filename(info)
        final_path = os.path.splitext(base)[0] + ".mp3"

    if os.path.exists(final_path):
        return final_path
    else:
        raise Exception(f"Download failed or file not found: {final_path}")

