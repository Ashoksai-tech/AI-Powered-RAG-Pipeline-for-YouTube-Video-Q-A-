import os
import json
import faiss
import numpy as np
from typing import List, Dict
import requests
import glob

def get_embedding(text: str) -> List[float]:
    """Get embeddings from Ollama mxbai-embed-large model"""
    url = "http://localhost:11434/api/embeddings"
    data = {
        "model": "mxbai-embed-large",
        "prompt": text
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["embedding"]
    else:
        raise Exception(f"Error getting embedding: {response.text}")

def load_chunks(chunks_dir: str) -> List[List[Dict]]:
    """Load all chunk files from directory"""
    chunks = []
    for chunk_file in sorted(glob.glob(os.path.join(chunks_dir, "chunk_*.json"))):
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunk_data = json.load(f)
            chunks.append(chunk_data["segments"])
    return chunks

def create_faiss_index(chunks: List[List[Dict]], base_dir: str) -> str:
    """Create FAISS index from chunks"""
    # Get first embedding to determine dimension
    first_chunk = chunks[0]
    merged_text = " ".join(segment["text"] for segment in first_chunk)
    first_embedding = get_embedding(merged_text)
    dimension = len(first_embedding)
    
    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)
    chunk_data = []
    embeddings = []
    
    # Process all chunks
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}/{len(chunks)}")
        merged_text = " ".join(segment["text"] for segment in chunk)
        embedding = get_embedding(merged_text)
        embeddings.append(embedding)
        chunk_data.append({
            "id": f"chunk_{i:03d}",
            "text": merged_text,
            "start_time": chunk[0]["start"],
            "end_time": chunk[-1]["end"],
            "segments": chunk
        })
    
    # Add embeddings to index
    embeddings_array = np.array(embeddings).astype('float32')
    index.add(embeddings_array)
    
    # Save index and metadata
    index_path = os.path.join(base_dir, "transcript.index")
    faiss.write_index(index, index_path)
    
    metadata_path = os.path.join(base_dir, "chunk_data.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunk_data, f, indent=2, ensure_ascii=False)
        
    print(f"Created FAISS index with {len(chunks)} vectors of dimension {dimension}")
    return index_path

def search_similar_chunks(query_embedding: List[float], k: int, base_dir: str) -> List[Dict]:
    """Search for k most similar chunks in FAISS index"""
    # Load index and metadata
    index = faiss.read_index(os.path.join(base_dir, "transcript.index"))
    with open(os.path.join(base_dir, "chunk_data.json"), "r") as f:
        chunk_data = json.load(f)
    
    # Convert query embedding to numpy array
    query_vector = np.array([query_embedding]).astype('float32')
    
    # Search in FAISS
    distances, indices = index.search(query_vector, k)
    
    # Get corresponding chunks
    results = []
    for i, idx in enumerate(indices[0]):
        chunk = chunk_data[idx]
        chunk['distance'] = float(distances[0][i])
        results.append(chunk)
        
    return results

def main():
    print("Loading chunks...")
    chunks = load_chunks("transcript_chunks")
    print(f"Loaded {len(chunks)} chunks")

    # Create FAISS index
    print("\nCreating FAISS index...")
    index_path = create_faiss_index(chunks, ".")

    # Search for similar chunks
    query_embedding = get_embedding("This is a query")
    similar_chunks = search_similar_chunks(query_embedding, 5, ".")
    print("\nSimilar chunks:")
    for chunk in similar_chunks:
        print(f"Chunk {chunk['id']}: {chunk['text']} (distance: {chunk['distance']})")

if __name__ == "__main__":
    main()
