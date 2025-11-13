import requests


class YtSearch:
    def __init__(self, query: str, api_key: str = None):
        self.query = query
        # Get API key from parameter or environment variable
        self.api_key = api_key 
        if not self.api_key:
            raise ValueError("YouTube API key is required. Set YOUTUBE_API_KEY or pass it directly.")

    def search(self, limit=10):
<<<<<<< HEAD
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": self.query,
            "type": "video",
            "maxResults": limit,
            "key": self.api_key,
        }
=======
        ydl_opts = {"quiet": True, "skip_download": True, "cookiefile": "cookies.txt"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch{limit}:{self.query}", download=False)
>>>>>>> f7d2f909e44c43845ba43e16d6c133a630e561d7

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.text}")

        data = response.json()
        videos = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            videos.append({
                "title": snippet["title"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": snippet["thumbnails"]["high"]["url"],
                "channel": snippet["channelTitle"],
                "description": snippet.get("description", ""),
            })

        return videos

