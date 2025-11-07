import os

import yt_dlp


class Yt_mp3:

    def __init__(self, url: str):

        self.url = url

        self.output_dir = "Downloads"

        os.makedirs(self.output_dir, exist_ok=True)

    def progress_hook(self, d):

        if d['status'] == 'downloading':

            percent = d.get('_percent_str', 'N/A')

            speed = d.get('speed', 0)

            print(f"Downloading: {percent} at {speed / 1024:.2f} KB/s")

        elif d['status'] == 'finished':

            print(f"✅ Finished downloading: {d['filename']}")

    def get_mp3(self):

        ydl_opts = {

            'format': 'bestaudio/best',

            'postprocessors': [{

                'key': 'FFmpegExtractAudio',

                'preferredcodec': 'mp3',

                'preferredquality': '192',

            }],

            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),

            #'progress_hooks': [self.progress_hook],

            'cookiefile': 'cookies.txt',

            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(self.url, download=True)

            filename = ydl.prepare_filename(info)

            return os.path.splitext(filename)[0] + ".mp3"
