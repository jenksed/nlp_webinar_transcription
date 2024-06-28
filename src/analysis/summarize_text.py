import os
from transformers import pipeline, AutoTokenizer

# Define directories
PREPROCESSED_DIR = "data/preprocessed"
SUMMARIES_DIR = "data/summaries"
MAX_LENGTH = 512  # Adjust as needed based on your model and average sentence length

if not os.path.exists(SUMMARIES_DIR):
    os.makedirs(SUMMARIES_DIR)

# Initialize the summarizer with more lenient settings
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
    for root, _, files in os.walk(PREPROCESSED_DIR):
        for filename in files:
            if filename.endswith(".txt") and filename != "speaker_names.txt":
                preprocessed_path = os.path.join(root, filename)
                with open(preprocessed_path, "r", encoding="utf-8") as f:
                    text = f.read()

                    # Check if the text exceeds the maximum length before tokenizing and generating summary
                    if len(tokenizer.encode(text, add_special_tokens=False)) > MAX_LENGTH:
                        print(f"Warning: Text too long for {filename}, truncating...")
                        text = tokenizer.decode(tokenizer.encode(text, add_special_tokens=False)[:MAX_LENGTH])
                        
                    # Summarize the entire text directly
                    summary = summarizer(
                        text,
                        max_length=300,
                        min_length=50,
                        do_sample=True,
                        temperature=0.5,
                    )[0]['summary_text']

                    summary_path = os.path.join(SUMMARIES_DIR, filename)
                    with open(summary_path, "w", encoding="utf-8") as out_f:
                        out_f.write(summary)
                    print(f"Summary saved for {filename}")

if __name__ == "__main__":
    summarize_all_transcripts()