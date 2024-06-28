import os
import whisper
from tqdm import tqdm

# Define the paths
AUDIO_DIR = "data/audio"
TRANSCRIPTS_DIR = "data/raw_transcripts"

# Create the transcripts directory if it doesn't exist
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

# Load the Whisper model
model = whisper.load_model("base")

def transcribe_audio(audio_file):
    audio_path = audio_file
    transcript_path = os.path.join(TRANSCRIPTS_DIR, os.path.splitext(os.path.relpath(audio_file, AUDIO_DIR))[0] + ".txt")
    os.makedirs(os.path.dirname(transcript_path), exist_ok=True)

    # Check if the transcript already exists
    if os.path.exists(transcript_path):
        print(f"[SKIP] Transcript already exists for {audio_file}")
        return

    print(f"[INFO] Starting transcription for {audio_file}...")
    try:
        result = model.transcribe(audio_path)

        # Write transcript to text file
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"[SUCCESS] Completed transcription for {audio_file}")

    except Exception as e:
        print(f"[ERROR] Failed to transcribe {audio_file}: {e}")

def find_audio_files(directory):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                audio_files.append(os.path.join(root, file))
    return audio_files

def main():
    print("Scanning for new audio files...")
    audio_files = find_audio_files(AUDIO_DIR)

    if not audio_files:
        print("No audio files found.")
        return

    for audio_file in tqdm(audio_files):
        transcribe_audio(audio_file)

if __name__ == "__main__":
    main()
