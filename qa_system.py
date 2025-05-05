import os
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_gemini():
    """Configure Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in .env file")
        
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    model = genai.GenerativeModel(
        model_name="gemma-3-1b-it",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    return model

def format_context(chunks: List[Dict]) -> str:
    """Format retrieved chunks into context"""
    context = "Here are the relevant transcript segments:\n\n"
    for i, chunk in enumerate(chunks, 1):
        context += f"Segment {i} [{chunk['start_time']} --> {chunk['end_time']}]:\n"
        context += f"{chunk['text']}\n\n"
    return context

def generate_prompt(query: str, context: str) -> str:
    """Generate prompt for Gemini"""
    return f"""You are a helpful AI assistant. Use the following transcript segments to answer the question. 
Only use information from the provided segments. If you cannot find the answer in the segments, say so.

{context}

Question: {query}

Answer: """

def query_gemini(prompt: str) -> str:
    """Query Gemini API"""
    model = setup_gemini()
    try:
        response = model.generate_content(prompt)
        if response.prompt_feedback.block_reason:
            raise Exception(f"Content blocked: {response.prompt_feedback.block_reason}")
        return response.text
    except Exception as e:
        raise Exception(f"Error querying Gemini API: {str(e)}")

if __name__ == "__main__":
    # Test the QA system
    test_chunks = [
        {
            "text": "This is a test segment 1",
            "start_time": "00:00:00.000",
            "end_time": "00:00:10.000"
        },
        {
            "text": "This is a test segment 2",
            "start_time": "00:00:10.000",
            "end_time": "00:00:20.000"
        }
    ]
    
    context = format_context(test_chunks)
    prompt = generate_prompt("What are the test segments?", context)
    answer = query_gemini(prompt)
    print("Answer:", answer)
