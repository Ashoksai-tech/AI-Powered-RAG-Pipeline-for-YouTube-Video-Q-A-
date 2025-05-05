# 🎥 AI-Powered RAG Pipeline for YouTube Video Q&A

This project is an end-to-end **Retrieval-Augmented Generation (RAG)** system that enables users to ask questions about YouTube videos and receive intelligent, context-aware answers powered by **Google's Gemini AI**.

---

## 🚀 Features

- ✅ Automatic YouTube **transcript extraction**
- ✂️ Smart **chunking** with timestamp preservation
- 🧠 **Semantic embeddings** using FAISS for similarity search
- 💬 **AI-powered answers** from Google's Gemini model
- 🔍 Displays **relevant video segments** (with timestamps)
- 🖥️ Modern **React frontend** for easy interaction
- 🔗 FastAPI-based **REST backend** with full pipeline orchestration

---

## 🛠️ System Architecture

### 🔹 Backend – Python & FastAPI
- `rag_pipeline.py`: Orchestrates the pipeline from video input to querying.
- `transcript.py`: Extracts video transcripts in VTT format.
- `chunk_transcript.py`: Chunks transcript text with time references.
- `embed_chunks.py`: Embeds chunks using FAISS for vector search.
- `qa_system.py`: Formats prompts and queries Gemini AI.
- `api.py`: REST API endpoints for video processing and QA.

### 🔹 Frontend – React
- `src/App.js`: Video input, question form, and response display.
- `src/App.css`: Clean, responsive user interface with loading/error states.

---

## 📈 Workflow

### 📹 Video Processing Pipeline
```

YouTube Video ID
→ Transcript Extraction
→ Chunking with Timestamps
→ Embedding with FAISS
→ Vector Index Creation

```

### ❓ Query Pipeline
```

User Question
→ Embedding Generation
→ Semantic Search via FAISS
→ Relevant Chunk Retrieval
→ Gemini AI Query
→ Contextual Answer

````

---

## 🧪 How to Use

### 🔧 Backend Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file with:
    ```
    GEMINI_API_KEY=your_gemini_api_key
    ```

3. Run the API server:
    ```bash
    python api.py
    # Available at http://localhost:8000
    ```

### 🎨 Frontend Setup

1. Navigate to frontend directory:
    ```bash
    cd frontend
    ```

2. Install dependencies and run:
    ```bash
    npm install
    npm start
    # Available at http://localhost:3000
    ```

### 🌐 Usage

- Enter a YouTube video ID in the frontend.
- Click **Process Video** to generate transcript and embeddings.
- Enter a question and receive an AI-generated answer along with timestamped context.

---

## 🧰 Tech Stack

- **Backend**: Python, FastAPI, FAISS, Gemini API, YouTube Transcript API
- **Frontend**: React, Axios, CSS
- **AI Model**: Gemini Pro (via Google Generative AI API)

---

## 📂 Project Structure

````

📦 root/
┣ 📜 rag\_pipeline.py
┣ 📜 transcript.py
┣ 📜 chunk\_transcript.py
┣ 📜 embed\_chunks.py
┣ 📜 qa\_system.py
┣ 📜 api.py
┣ 📁 frontend/
┃ ┣ 📜 App.js
┃ ┣ 📜 App.css
┃ ┗ 📜 index.js
┗ 📄 README.md
 
