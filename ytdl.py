import os

import yt_dlp


class Ytdl:

    def __init__(self, url:str):

        self.url = url

        self.ouput_dir = "Downloads"

        os.makedirs(self.ouput_dir, exist_ok=True)

    def progress_hook(self, d):

        if d['status'] == 'downloading':

            percent = d.get('_percent_str', 'N/A')

            speed = d.get('speed', 0)

            print(f"Downloading: {percent} at {speed / 1024:.2f} KB/s")

        elif d['status'] == 'finished':

            print(f"✅ Finished downloading: {d['filename']}")

    def mp3_downl(self):


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