import sys
import os
from pytube import YouTube
from pydub import AudioSegment

def download_audio(youtube_url, output_dir='data/audio'):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Create YouTube object
        yt = YouTube(youtube_url)

        # Get the best audio stream available
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream
        print(f"Downloading audio from {yt.title}...")
        audio_file = audio_stream.download(output_dir)

        # Convert the downloaded file to mp3
        base, ext = os.path.splitext(audio_file)
        mp3_file = f"{base}.mp3"
        AudioSegment.from_file(audio_file).export(mp3_file, format="mp3")

        # Remove the original downloaded file
        os.remove(audio_file)

        print(f"Downloaded and converted audio saved to {mp3_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_audio.py <YouTube URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]
    download_audio(youtube_url)
