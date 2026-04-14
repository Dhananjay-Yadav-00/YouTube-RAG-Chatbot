from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_channel_videos(channel_id, max_results):
    channel = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    if not channel.get("items"):
        print(f"Error: Channel ID {channel_id} not found.")
        return []

    uploads = channel["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads,
        maxResults=max_results
    ).execute()

    video_ids = [v["snippet"]["resourceId"]["videoId"] for v in videos["items"]]
    return video_ids


def get_video_details(video_ids):
    if not video_ids:
        return []

    data = []
    # YouTube API limits 'id' parameter to 50 IDs per call
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        response = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(chunk)
        ).execute()

        for v in response.get("items", []):
            data.append({
                "video_id": v["id"],
                "url": f"https://www.youtube.com/watch?v={v['id']}",
                "title": v["snippet"]["title"],
                "description": v["snippet"]["description"],
                "published": v["snippet"]["publishedAt"],
                "tags": v["snippet"].get("tags", []),
                "views": int(v["statistics"].get("viewCount", 0)),
                "likes": int(v["statistics"].get("likeCount", 0)),
                "comments": int(v["statistics"].get("commentCount", 0)),
            })
    return data
