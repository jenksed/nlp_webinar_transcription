import os
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline

# Ensure NLTK data is downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Hugging Face NER pipeline
ner_pipeline = pipeline("ner", grouped_entities=True)

# Paths to transcripts
TRANSCRIPTS_DIR = "data/raw_transcripts"
PREPROCESSED_DIR = "data/preprocessed"
SPEAKER_NAMES_FILE = "data/preprocessed/speaker_names.txt"

if not os.path.exists(PREPROCESSED_DIR):
    os.makedirs(PREPROCESSED_DIR)

# List of common non-human entities to filter out
NON_HUMAN_ENTITIES = ["GVHD", "Thermo Fisher Scientific", "PVMC", "QC", "PDX", "Lab Roots", "Thermo Fisher", "Chemistry"]

# Function to preprocess text
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    return ' '.join([word for word in words if word.isalnum() and word not in stop_words])

# Function to extract speaker names using Hugging Face NER
def extract_speaker_names(text):
    ner_results = ner_pipeline(text)
    speaker_names = [result['word'] for result in ner_results if result['entity_group'] == "PER"]
    speaker_names = list(set(speaker_names))  # Remove duplicates
    speaker_names = [name for name in speaker_names if name not in NON_HUMAN_ENTITIES]
    return speaker_names

# Function to extract webinar name from filename
def extract_webinar_name(filename):
    webinar_name = os.path.splitext(os.path.basename(filename))[0]
    return webinar_name

def preprocess_all_transcripts():
    all_speaker_names = []

    for root, _, files in os.walk(TRANSCRIPTS_DIR):
        for filename in files:
            if filename.endswith(".txt"):
                transcript_path = os.path.join(root, filename)
                with open(transcript_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    preprocessed_text = preprocess_text(text)
                    webinar_name = extract_webinar_name(filename)
                    speaker_names = extract_speaker_names(text)
                    all_speaker_names.append(f"{webinar_name}\n" + "\n".join(speaker_names) + "\n")

                    # Save the preprocessed text in the corresponding subdirectory
                    relative_path = os.path.relpath(transcript_path, TRANSCRIPTS_DIR)
                    preprocessed_path = os.path.join(PREPROCESSED_DIR, relative_path)
                    os.makedirs(os.path.dirname(preprocessed_path), exist_ok=True)
                    with open(preprocessed_path, "w", encoding="utf-8") as out_f:
                        out_f.write(preprocessed_text)
                    print(f"Preprocessed {filename}")

    # Save speaker names to a file
    with open(SPEAKER_NAMES_FILE, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(all_speaker_names))
    print(f"Extracted speaker names saved to {SPEAKER_NAMES_FILE}")

if __name__ == "__main__":
    preprocess_all_transcripts()
