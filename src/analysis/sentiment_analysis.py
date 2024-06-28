import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download required NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')

# Define directories
PREPROCESSED_DIR = "data/preprocessed"
SENTIMENT_OUTPUT = "data/analysis/sentiment_analysis.txt"

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

def sentiment_analysis(text):
    sentences = nltk.sent_tokenize(text)
    sentiment_scores = {"compound": 0, "pos": 0, "neu": 0, "neg": 0}
    for sentence in sentences:
        scores = sid.polarity_scores(sentence)
        for key in sentiment_scores:
            sentiment_scores[key] += scores[key]
    for key in sentiment_scores:
        sentiment_scores[key] = sentiment_scores[key] / len(sentences)
    return sentiment_scores

def process_all_transcripts():
    transcripts = [f for f in os.listdir(PREPROCESSED_DIR) if f.endswith(".txt")]
    all_sentiments = []

    for filename in transcripts:
        transcript_path = os.path.join(PREPROCESSED_DIR, filename)
        with open(transcript_path, "r", encoding="utf-8") as f:
            text = f.read()
            sentiments = sentiment_analysis(text)
            all_sentiments.append(f"Sentiments in {filename}:\n{sentiments}\n{'-'*80}\n")

    with open(SENTIMENT_OUTPUT, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(all_sentiments))
    print(f"Sentiment analysis report saved as {SENTIMENT_OUTPUT}")

if __name__ == "__main__":
    process_all_transcripts()
