import os
from gensim import corpora, models

# Define directories
PREPROCESSED_DIR = "data/preprocessed"
TOPIC_OUTPUT = "data/analysis/topic_modeling.txt"

# Function for topic modeling
def topic_modeling(texts, num_topics=2):
    texts = [text.split() for text in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    return ldamodel.print_topics(num_words=5)

def process_all_transcripts():
    transcripts = [f for f in os.listdir(PREPROCESSED_DIR) if f.endswith(".txt")]
    all_texts = []

    for filename in transcripts:
        transcript_path = os.path.join(PREPROCESSED_DIR, filename)
        with open(transcript_path, "r", encoding="utf-8") as f:
            text = f.read()
            all_texts.append(text)

    topics = topic_modeling(all_texts)
    with open(TOPIC_OUTPUT, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join([str(topic) for topic in topics]))
    print(f"Topic modeling report saved as {TOPIC_OUTPUT}")

if __name__ == "__main__":
    process_all_transcripts()
