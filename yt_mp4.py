import os
import yt_dlp


class Yt_mp4:
    def __init__(self, url: str):
        self.url = url
        self.output_dir = "Downloads"

        os.makedirs(self.output_dir, exist_ok=True)

    def download(self):
        ydl_opts = {
<<<<<<< HEAD
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'Downloads/%(title)s.%(ext)s',
             'cookiefile': 'cookies.txt',
            'quiet': True
=======
            "format": "best",
            "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
            "quiet": True,
            "cookiefile":"cookies.txt"
>>>>>>> f7d2f909e44c43845ba43e16d6c133a630e561d7
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            filename = f"{info['title']}.mp4"
            filepath = os.path.join('Downloads', filename)
            return filepath, filename
