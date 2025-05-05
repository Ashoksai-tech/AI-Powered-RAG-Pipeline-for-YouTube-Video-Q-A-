import os
import logging
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Import functions from other modules
from transcript import generate_transcript
from chunk_transcript import chunk_transcript, save_chunk
from embed_chunks import get_embedding, create_faiss_index, search_similar_chunks
from qa_system import query_gemini, format_context, generate_prompt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, video_id: str):
        load_dotenv()
        self.video_id = video_id
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.chunks_dir = os.path.join(self.base_dir, "transcript_chunks")
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        if not os.path.exists(self.chunks_dir):
            os.makedirs(self.chunks_dir)

    def run_pipeline(self) -> None:
        """Run the complete pipeline"""
        try:
            # Step 1: Generate transcript
            logger.info("Generating transcript...")
            vtt_path = generate_transcript(self.video_id)
            
            # Step 2: Chunk transcript
            logger.info("Chunking transcript...")
            chunks = chunk_transcript(vtt_path, self.chunks_dir)
            
            # Steps 3 & 4: Create embeddings and index
            logger.info("Creating embeddings and FAISS index...")
            index_path = create_faiss_index(chunks, self.base_dir)
            
            logger.info("Pipeline completed successfully!")
            logger.info("You can now query the system using the query_system method")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise

    def query_system(self, query: str, k: int = 3) -> Dict:
        """Process query and generate response"""
        logger.info("Processing query...")
        try:
            # Get query embedding
            query_embedding = get_embedding(query)
            
            # Search similar chunks using FAISS
            results = search_similar_chunks(query_embedding, k, self.base_dir)
            
            # Format context and generate prompt
            context = format_context(results)
            prompt = generate_prompt(query, context)
            
            # Get response from Gemini
            answer = query_gemini(prompt)
            
            return {
                "answer": answer,
                "retrieved_chunks": results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

def main():
    # Get video ID from user
    video_id = input("Enter YouTube video ID: ").strip()
    
    # Initialize and run pipeline
    pipeline = RAGPipeline(video_id)
    pipeline.run_pipeline()
    
    print("\nRAG Pipeline is ready!")
    print("Type 'quit' to exit")
    
    # Interactive query loop
    while True:
        try:
            query = input("\nYour question: ").strip()
            
            if query.lower() == 'quit':
                break
                
            result = pipeline.query_system(query)
            
            if "error" in result:
                print(f"\nError: {result['error']}")
            else:
                print("\nAnswer:", result["answer"])
                print("\nRetrieved from segments:")
                for chunk in result["retrieved_chunks"]:
                    print(f"- [{chunk['start_time']} --> {chunk['end_time']}] (distance: {chunk['distance']:.4f})")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
