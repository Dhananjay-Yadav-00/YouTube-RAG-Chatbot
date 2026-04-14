import streamlit as st
import sys
import os

# Important for running properly with non-utf8 defaults on Windows
sys.stdout.reconfigure(encoding='utf-8')

from youtube.channel_videos import get_channel_videos, get_video_details
from youtube.competitor_discovery import discover_competitors
from rag.document_builder import build_documents
from rag.vector_store import create_vector_store
from chatbot.router import route_question
from chatbot.qa_engine import answer
from config import USER_VIDEO_LIMIT, COMPETITOR_VIDEO_LIMIT, COMPETITOR_AUTO_LIMIT

# Streamlit Page Config
st.set_page_config(page_title="YouTube Competitor RAG Chatbot", page_icon="🤖", layout="wide")

st.title("YouTube Competitor Analysis Chatbot 🤖")
st.markdown("Analyze your channel against top competitors. Ask questions about content gaps, engagement, and video ideas!")

# Initialize Session State
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for Setup
with st.sidebar:
    st.header("Setup")
    user_channel = st.text_input("Enter YOUR Channel ID:", placeholder="e.g., UCCWi3hpnq...")
    competitor_channels = st.text_input("Competitor Channels (Optional, comma-separated):", help="Leave empty to auto-discover competitors.")
    
    if st.button("Load & Analyze"):
        if not user_channel:
            st.error("Please provide your Channel ID.")
        else:
            with st.status("Fetching Data...", expanded=True) as status:
                try:
                    # User videos
                    st.write("Fetching user videos...")
                    user_ids = get_channel_videos(user_channel, USER_VIDEO_LIMIT)
                    if not user_ids:
                        status.update(label="Failed to fetch user videos.", state="error")
                        st.stop()
                        
                    user_videos = get_video_details(user_ids)
                    
                    # Competitor videos
                    if competitor_channels.strip():
                        comp_ids = []
                        channels = [ch.strip() for ch in competitor_channels.split(",") if ch.strip()]
                        if channels:
                            per_channel = max(1, COMPETITOR_VIDEO_LIMIT // len(channels))
                            st.write(f"Fetching from {len(channels)} provided competitors...")
                            for ch in channels:
                                comp_ids += get_channel_videos(ch, per_channel)
                    else:
                        st.write("Auto-discovering competitors...")
                        if user_videos and user_videos[0].get("tags"):
                            keywords = " ".join(user_videos[0]["tags"][:3])
                        else:
                            keywords = user_videos[0]["title"]
                        comp_ids = discover_competitors(keywords, COMPETITOR_AUTO_LIMIT)

                    st.write(f"Fetching details for {len(comp_ids)} competitor videos...")
                    competitor_videos = get_video_details(comp_ids)

                    # Building Docs & DB
                    st.write("Building vector database...")
                    docs = []
                    docs += build_documents(user_videos, "user")
                    docs += build_documents(competitor_videos, "competitor")

                    if not docs:
                        status.update(label="No video data gathered.", state="error")
                        st.stop()
                    
                    st.session_state.vector_db = create_vector_store(docs)
                    status.update(label="Data loaded and Ready!", state="complete", expanded=False)
                    st.success("Chatbot is ready. You can now chat in the main window.")
                except Exception as e:
                    status.update(label=f"An error occurred: {str(e)}", state="error")

# Main Interface: Chat
if st.session_state.vector_db:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask a question about your content vs competitors..."):
        # Add and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    intent = route_question(prompt)
                    relevant_docs = st.session_state.vector_db.similarity_search(prompt, k=6)
                    response = answer(prompt, relevant_docs, intent)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {e}")
else:
    st.info("👈 Please load your Channel Data from the sidebar to begin chatting.")
