from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from rag_pipeline import RAGPipeline
import uvicorn

app = FastAPI(title="RAG Pipeline API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active pipelines in memory (in production, use a proper database)
active_pipelines = {}

class VideoRequest(BaseModel):
    video_id: str

class QueryRequest(BaseModel):
    video_id: str
    query: str

class QueryResponse(BaseModel):
    answer: str
    retrieved_chunks: List[Dict]
    timestamp: str

@app.post("/process-video")
async def process_video(request: VideoRequest):
    try:
        # Initialize and run pipeline
        pipeline = RAGPipeline(request.video_id)
        pipeline.run_pipeline()
        
        # Store pipeline instance
        active_pipelines[request.video_id] = pipeline
        
        return {"message": "Video processed successfully", "video_id": request.video_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_video(request: QueryRequest):
    try:
        pipeline = active_pipelines.get(request.video_id)
        if not pipeline:
            raise HTTPException(status_code=404, detail="Video not processed. Please process the video first.")
        
        result = pipeline.query_system(request.query)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
