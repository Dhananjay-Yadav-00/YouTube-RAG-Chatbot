from googleapiclient.discovery import build
from datetime import datetime, timedelta
from config import YOUTUBE_API_KEY, DAYS_LOOKBACK

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def discover_competitors(keywords, max_results):
    published_after = (datetime.utcnow() - timedelta(days=DAYS_LOOKBACK)).isoformat("T") + "Z"

    search = youtube.search().list(
        q=keywords,
        part="snippet",
        type="video",
        order="viewCount",
        publishedAfter=published_after,
        maxResults=max_results
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search.get("items", [])]

    # If not enough videos found, broaden search by removing time limit
    if len(video_ids) < max_results:
        print(f"Warning: Only found {len(video_ids)} videos recent videos. Expanding search...")
        remaining = max_results - len(video_ids)
        search_broad = youtube.search().list(
            q=keywords,
            part="snippet",
            type="video",
            order="viewCount",
            maxResults=remaining
        ).execute()
        
        new_ids = [item["id"]["videoId"] for item in search_broad.get("items", [])]
        # Avoid duplicates
        for vid in new_ids:
            if vid not in video_ids:
                video_ids.append(vid)
                
    return video_ids[:max_results]
