# YouTube RAG Chatbot 🤖📺

A powerful AI-driven chatbot designed to provide deep analytical insights and competitive analysis for YouTube channels using **Retrieval-Augmented Generation (RAG)**. Discover competitor strategies, identify missing content gaps, and analyze viewer engagement effortlessly!

![Streamlit UI](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Language Models](https://img.shields.io/badge/LLM-Groq-F5503D?style=for-the-badge)
![Embeddings](https://img.shields.io/badge/Embeddings-HuggingFace-F9AB00?style=for-the-badge&logo=huggingface)

## ✨ Features
* **Automated Competitor Discovery:** Automatically finds top competitors in your niche by extracting topics and tags from your videos.
* **Intelligent Vector Search:** Converts YouTube statistics and video data into vector embeddings (using `SentenceTransformers`) for deep similarity analysis.
* **Lightning Fast LLM:** Utilizes the high-speed **Groq API** (`llama-3.1-8b-instant`) to instantly generate actionable insights based on your YouTube data.
* **Interactive Web Interface:** A highly responsive graphical interface powered by **Streamlit**, featuring memory caches so you don't rebuild your database every time you ask a question.
* **Data-driven Trends:** Ask the chatbot directly to compare engagement rates, comment velocities, and top-performing videos against your own catalog.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **LLM Engine:** Groq SDK (Llama 3.1)
* **Vector Database:** FAISS CPU
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2`
* **Orchestration:** LangChain
* **API Extraction:** Google YouTube Data v3 API

---

## 🚀 Getting Started

### Prerequisites
1. Python 3.9+ installed on your system.
2. A **YouTube Data V3 API Key**. (Get one from [Google Cloud Console](https://console.cloud.google.com/))
3. A **Groq API Key**. (Get one from [Groq Console](https://console.groq.com/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/youtube-rag-chatbot.git
   cd youtube-rag-chatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys:**
   Copy the `.env.example` to `.env` and fill in your API credentials.
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` and configure your credentials:*
   ```env
   YOUTUBE_API_KEY=your_youtube_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

### 💻 Running the Application

Launch the Streamlit interface using the following command:

```bash
streamlit run streamlit_app.py
```
*Wait a few seconds, and the app will open automatically in your browser at `http://localhost:8501`.*

---

## 🧠 How to Use

1. Enter your **YouTube Channel ID** in the sidebar.
2. *(Optional)* Add explicit competitor channel IDs via comma separation, or leave it blank to let the AI auto-discover competitors for you.
3. Click **"Load & Analyze"**.
4. Once data fetching and embedding completes, open the main chat window and ask questions like:
   - *"What content gaps exist between my channel and my competitors?"*
   - *"Use trend video to compare with my latest upload."*
   - *"Which competitor has the highest engagement rate and why?"*

## 🛡️ License & Contributions
Feel free to fork this repository, submit Pull Requests, or use it for your personal analytics setup!
