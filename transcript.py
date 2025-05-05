from youtube_transcript_api import YouTubeTranscriptApi
import os

def seconds_to_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def generate_transcript(video_id: str) -> str:
    """Generate WebVTT transcript from YouTube video"""
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    vtt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcript.vtt")
    
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, entry in enumerate(transcript, 1):
            f.write(f"{i}\n")
            start = seconds_to_timestamp(entry["start"])
            end = seconds_to_timestamp(entry["start"] + entry["duration"])
            f.write(f"{start} --> {end}\n")
            f.write(f"{entry['text']}\n\n")
            
    return vtt_path

if __name__ == "__main__":
    video_id = input("Enter YouTube video ID: ")
    transcript_path = generate_transcript(video_id)
    print(f"Transcript saved to: {transcript_path}")