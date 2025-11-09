import yt_dlp

class YtSearch:
    def __init__(self, query: str):
        self.query = query

    def search(self, limit=10):
        ydl_opts = {"quiet": True, "skip_download": True, "cookiefile": "cookies.txt"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch{limit}:{self.query}", download=False)

        videos = []
        for entry in result.get("entries", []):
            videos.append({
                "title": entry.get("title"),
                "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                "thumbnail": entry.get("thumbnail"),
                "duration": entry.get("duration"),
                "channel": entry.get("uploader"),
            })

        return videos

