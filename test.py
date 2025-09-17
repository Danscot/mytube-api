import os
import yt_dlp

# Directory to save downloaded files
output_directory = 'Download__'

os.makedirs(output_directory, exist_ok=True)

# Progress hook function (optional but helpful)
def progress_hook(d):

    if d['status'] == 'downloading':

        percent = d.get('_percent_str', 'N/A')

        speed = d.get('speed', 0)

        print(f"Downloading: {percent} at {speed / 1024:.2f} KB/s")

    elif d['status'] == 'finished':

        print(f"✅ Finished downloading: {d['filename']}")

# Main function to download audio
def download_audio_from_video(video_url):

    ydl_opts = {

        'format': 'bestaudio/best',

        'postprocessors': [{

            'key': 'FFmpegExtractAudio',

            'preferredcodec': 'mp3',

            'preferredquality': '192',

        }],

        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),

        'progress_hooks': [progress_hook],

        'cookiefile': 'cookies.txt',  # 👈 Use your exported cookies.txt here

        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        ydl.download([video_url])

if __name__ == "__main__":

    # Replace this with any video URL for testing

    test_url = 'https://www.youtube.com/watch?v=JGu9PkpU3o8'
    
    download_audio_from_video(test_url)
