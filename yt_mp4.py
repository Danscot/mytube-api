import os
import yt_dlp


class Yt_mp4:
    def __init__(self, url: str):
        self.url = url
        self.output_dir = "Downloads"

        os.makedirs(self.output_dir, exist_ok=True)

    def download(self):
        ydl_opts = {
            "format": "best",
            "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
            "quiet": True,
            "cookiefile":"cookies.txt"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            return ydl.prepare_filename(info)

