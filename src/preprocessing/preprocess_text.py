import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure NLTK data is downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Paths to transcripts
TRANSCRIPTS_DIR = "data/raw_transcripts"
PREPROCESSED_DIR = "data/preprocessed"

if not os.path.exists(PREPROCESSED_DIR):
    os.makedirs(PREPROCESSED_DIR)

# Function to preprocess text
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    return ' '.join([word for word in words if word.isalnum() and word not in stop_words])

def preprocess_all_transcripts():
    transcripts = [f for f in os.listdir(TRANSCRIPTS_DIR) if f.endswith(".txt")]

    for filename in transcripts:
        transcript_path = os.path.join(TRANSCRIPTS_DIR, filename)
        with open(transcript_path, "r", encoding="utf-8") as f:
            text = f.read()
            preprocessed_text = preprocess_text(text)

            preprocessed_path = os.path.join(PREPROCESSED_DIR, filename)
            with open(preprocessed_path, "w", encoding="utf-8") as out_f:
                out_f.write(preprocessed_text)
            print(f"Preprocessed {filename}")

if __name__ == "__main__":
    preprocess_all_transcripts()
