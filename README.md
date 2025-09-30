# 🎵 FastAPI YouTube Downloader

A simple YouTube-to-MP3 downloader API built with **FastAPI** and **yt-dlp**.  
It lets you download audio from YouTube videos directly as MP3 files.

---

## 🚀 Features
- Download YouTube videos as **MP3**  
- Returns the file directly via API  
- Uses **yt-dlp** + **ffmpeg** for conversion  
- Runs inside a lightweight **Docker container**

---

## 📦 Setup (Docker)

1. Clone this repository and navigate into it:
   ```bash
   git clone https://github.com/Danscot/mytube-api.git

   cd mytube-api
```

2. Build the Docker image:

   ```bash

docker build -t mytube .


```
3. Run the container:

```bash
docker run -d -p 8000:8000 mytube

```

- The API will be available at:

http://127.0.0.1:8000/youtube

- Inorder to do request use

 POST http://127.0.0.1:8000/youtube/download/mp3?url="Youtube_video_url"

## Example

- Using curl

```bash

curl -X POST http://127.0.0.1:8000/youtube/download/mp3?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ


```
