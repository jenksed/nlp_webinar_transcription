import os
from sklearn.feature_extraction.text import TfidfVectorizer

# Define directories
PREPROCESSED_DIR = "data/preprocessed"
KEYWORD_OUTPUT = "data/analysis/keyword_extraction.txt"

# Function for keyword extraction
def keyword_extraction(texts, num_keywords=10):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=num_keywords)
    vectors = vectorizer.fit_transform(texts)
    keywords = vectorizer.get_feature_names_out()
    return keywords

def process_all_transcripts():
    transcripts = [f for f in os.listdir(PREPROCESSED_DIR) if f.endswith(".txt")]
    all_texts = []

    for filename in transcripts:
        transcript_path = os.path.join(PREPROCESSED_DIR, filename)
        with open(transcript_path, "r", encoding="utf-8") as f:
            text = f.read()
            all_texts.append(text)

    keywords = keyword_extraction(all_texts)
    with open(KEYWORD_OUTPUT, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(keywords))
    print(f"Keyword extraction report saved as {KEYWORD_OUTPUT}")

if __name__ == "__main__":
    process_all_transcripts()
