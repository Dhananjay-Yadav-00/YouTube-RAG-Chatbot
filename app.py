import sys
sys.stdout.reconfigure(encoding='utf-8')
from youtube.channel_videos import get_channel_videos, get_video_details
from youtube.competitor_discovery import discover_competitors
from rag.document_builder import build_documents
from rag.vector_store import create_vector_store
from chatbot.router import route_question
from chatbot.qa_engine import answer
from config import USER_VIDEO_LIMIT, COMPETITOR_VIDEO_LIMIT, COMPETITOR_AUTO_LIMIT

def main():
    user_channel = input("Enter YOUR channel ID: ")
    competitor_channels = input(
        "Enter competitor channel IDs (comma separated) OR press Enter to auto-discover: "
    )

    # User videos
    print(f"Fetching up to {USER_VIDEO_LIMIT} videos from your channel...")
    user_ids = get_channel_videos(user_channel, USER_VIDEO_LIMIT)
    user_videos = get_video_details(user_ids)

    if not user_videos:
        print("No videos found for your channel. Please check the ID.")
        return

    # Competitors
    if competitor_channels.strip():
        comp_ids = []
        channels = [ch.strip() for ch in competitor_channels.split(",") if ch.strip()]
        if channels:
            # Distribute COMPETITOR_VIDEO_LIMIT among provided channels
            per_channel = max(1, COMPETITOR_VIDEO_LIMIT // len(channels))
            print(f"Fetching up to {per_channel} videos from each of the {len(channels)} competitor channels...")
            for ch in channels:
                comp_ids += get_channel_videos(ch, per_channel)
    else:
        # Improve keyword extraction: Prioritize tags, then title
        if user_videos[0].get("tags"):
            # Use top 3 tags for broader reach
            keywords = " ".join(user_videos[0]["tags"][:3])
        else:
            keywords = user_videos[0]["title"]
            
        print(f"Auto-discovering up to {COMPETITOR_AUTO_LIMIT} competitors using keywords: '{keywords}'...")
        comp_ids = discover_competitors(keywords, COMPETITOR_AUTO_LIMIT)

    print(f"Fetching details for {len(comp_ids)} competitor videos...")
    competitor_videos = get_video_details(comp_ids)

    docs = []
    docs += build_documents(user_videos, "user")
    docs += build_documents(competitor_videos, "competitor")

    if not docs:
        print("No video data could be gathered for analysis.")
        return

    vector_db = create_vector_store(docs)

    print("\nChatbot ready! Ask questions (type 'exit' to stop)\n")

    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break

        intent = route_question(q)
        relevant_docs = vector_db.similarity_search(q, k=6)
        print("\nBot:", answer(q, relevant_docs, intent), "\n")

if __name__ == "__main__":
    main()
