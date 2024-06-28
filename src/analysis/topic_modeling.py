import os
from gensim import corpora, models
from gensim.models import CoherenceModel

# Define directories
PREPROCESSED_DIR = "data/preprocessed"
TOPIC_OUTPUT = "data/analysis/topic_modeling.txt"

# Function for topic modeling (with coherence calculation)
def topic_modeling(texts, dictionary, corpus, num_topics=2):
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    # Calculate coherence score (optional)
    coherence_model_lda = CoherenceModel(model=ldamodel, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()

    return ldamodel.print_topics(num_words=5), coherence_lda


def process_all_transcripts():
    all_texts = []

    for root, _, files in os.walk(PREPROCESSED_DIR):
        for filename in files:
            if filename.endswith(".txt") and filename != "speaker_names.txt":
                transcript_path = os.path.join(root, filename)
                with open(transcript_path, "r", encoding="utf-8") as f:
                    text = f.read().split()  # Split text into words for gensim
                    all_texts.append(text)  # Only append the text itself

    # Create dictionary and corpus outside the loop
    dictionary = corpora.Dictionary(all_texts)
    corpus = [dictionary.doc2bow(text) for text in all_texts]

    all_topics = []
    for i, text in enumerate(all_texts):
        topics, coherence = topic_modeling([text], dictionary, corpus)
        webinar_name = os.path.splitext(files[i])[0] # Get webinar name from the file list

        topics_output = f"Topics in {webinar_name} (Coherence: {coherence:.3f}):\n"  # Display coherence
        for topic in topics:
            topics_output += f"{topic}\n"
        topics_output += "-"*80 + "\n"
        all_topics.append(topics_output)

    with open(TOPIC_OUTPUT, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(all_topics))
    print(f"Topic modeling report saved as {TOPIC_OUTPUT}")


if __name__ == "__main__":
    process_all_transcripts()
