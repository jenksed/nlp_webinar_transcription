import os
from transformers import pipeline, AutoTokenizer

# Define directories
PREPROCESSED_DIR = "data/preprocessed"
SUMMARIES_DIR = "data/summaries"
MAX_LENGTH = 512

if not os.path.exists(SUMMARIES_DIR):
    os.makedirs(SUMMARIES_DIR)

# Initialize the summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

# Function to split text into chunks within the model's maximum sequence length
def split_text(text, max_length=MAX_LENGTH):
    sentences = text.split('.')
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        sentence_length = len(tokenizer.encode(sentence, add_special_tokens=False))
        if current_length + sentence_length <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            if current_chunk:
                yield ' '.join(current_chunk) + '.'
            current_chunk = [sentence]
            current_length = sentence_length
    if current_chunk:
        yield ' '.join(current_chunk) + '.'

def summarize_all_transcripts():
    preprocessed_files = [f for f in os.listdir(PREPROCESSED_DIR) if f.endswith(".txt")]

    for filename in preprocessed_files:
        preprocessed_path = os.path.join(PREPROCESSED_DIR, filename)
        with open(preprocessed_path, "r", encoding="utf-8") as f:
            text = f.read()

            summary_chunks = list(split_text(text, max_length=MAX_LENGTH))
            summaries = []
            for chunk in summary_chunks:
                if len(tokenizer.encode(chunk, add_special_tokens=False)) <= MAX_LENGTH:
                    summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                    summaries.append(summary)
                else:
                    print(f"Chunk too long after splitting and truncating: {chunk[:50]}...")

            summary = ' '.join(summaries)

            summary_path = os.path.join(SUMMARIES_DIR, filename)
            with open(summary_path, "w", encoding="utf-8") as out_f:
                out_f.write(summary)
            print(f"Summary saved for {filename}")

if __name__ == "__main__":
    summarize_all_transcripts()
