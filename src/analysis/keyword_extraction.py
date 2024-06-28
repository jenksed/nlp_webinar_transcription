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
    all_keywords = []

    for root, _, files in os.walk(PREPROCESSED_DIR):
        for filename in files:
            if filename.endswith(".txt"):
                transcript_path = os.path.join(root, filename)
                with open(transcript_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    keywords = keyword_extraction([text])
                    webinar_name = os.path.splitext(os.path.basename(filename))[0]
                    all_keywords.append(f"{webinar_name}:\n" + "\n".join(keywords) + "\n" + "-"*80 + "\n")

    with open(KEYWORD_OUTPUT, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(all_keywords))
    print(f"Keyword extraction report saved as {KEYWORD_OUTPUT}")

if __name__ == "__main__":
    process_all_transcripts()
