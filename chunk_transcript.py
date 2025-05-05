import os
import json
from typing import List, Dict

def seconds_to_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def save_chunk(chunk: List[Dict], chunk_num: int, chunks_dir: str):
    """Save a chunk to file"""
    chunk_data = {
        "segments": chunk,
        "start_time": chunk[0]["start"],
        "end_time": chunk[-1]["end"],
        "merged_text": " ".join(segment["text"] for segment in chunk),
        "segment_count": len(chunk)
    }
    
    chunk_path = os.path.join(chunks_dir, f"chunk_{chunk_num:03d}.json")
    with open(chunk_path, "w", encoding="utf-8") as f:
        json.dump(chunk_data, f, indent=2, ensure_ascii=False)
    print(f"Created chunk {chunk_num} with {len(chunk)} segments")

def chunk_transcript(vtt_path: str, chunks_dir: str, chunk_duration: int = 30) -> List[Dict]:
    """Split transcript into chunks of specified duration"""
    if not os.path.exists(chunks_dir):
        os.makedirs(chunks_dir)

    current_chunk = []
    current_chunk_duration = 0
    chunk_counter = 1
    chunks = []

    with open(vtt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.isdigit() and i + 2 < len(lines):
                timestamp_line = lines[i + 1].strip()
                text_line = lines[i + 2].strip()
                
                if " --> " in timestamp_line:
                    start_time, end_time = timestamp_line.split(" --> ")
                    current_chunk.append({
                        "timestamp": timestamp_line,
                        "text": text_line,
                        "start": start_time,
                        "end": end_time
                    })
                    
                    # Calculate duration
                    start_parts = start_time.split(":")
                    start_seconds = float(start_parts[0]) * 3600 + float(start_parts[1]) * 60 + float(start_parts[2])
                    end_parts = end_time.split(":")
                    end_seconds = float(end_parts[0]) * 3600 + float(end_parts[1]) * 60 + float(end_parts[2])
                    current_chunk_duration += (end_seconds - start_seconds)
                    
                    # Save chunk if duration exceeds threshold
                    if current_chunk_duration >= chunk_duration:
                        save_chunk(current_chunk, chunk_counter, chunks_dir)
                        chunks.append(current_chunk)
                        current_chunk = []
                        current_chunk_duration = 0
                        chunk_counter += 1
                        
            i += 4 if line.isdigit() and i + 2 < len(lines) else 1

    # Save any remaining chunk
    if current_chunk:
        save_chunk(current_chunk, chunk_counter, chunks_dir)
        chunks.append(current_chunk)

    print(f"\nTotal chunks created: {chunk_counter}")
    print(f"Chunks are saved in the '{chunks_dir}' directory")
    return chunks

if __name__ == "__main__":
    vtt_path = input("Enter path to VTT file: ")
    chunks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcript_chunks")
    chunks = chunk_transcript(vtt_path, chunks_dir)
