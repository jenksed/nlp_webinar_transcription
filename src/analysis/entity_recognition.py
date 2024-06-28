import os
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define directories
PREPROCESSED_DIR = "data/preprocessed"
ENTITY_OUTPUT = "data/analysis/entity_extraction.txt"

# Function for entity recognition
def entity_recognition(text):
    doc = nlp(text)
    entities = {"PERSON": [], "ORG": [], "GPE": [], "DATE": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    for key in entities:
        entities[key] = list(set(entities[key]))  # Remove duplicates
    return entities

def process_all_transcripts():
    transcripts = [f for f in os.listdir(PREPROCESSED_DIR) if f.endswith(".txt")]
    all_entities = []

    for filename in transcripts:
        transcript_path = os.path.join(PREPROCESSED_DIR, filename)
        with open(transcript_path, "r", encoding="utf-8") as f:
            text = f.read()
            entities = entity_recognition(text)
            all_entities.append(f"Entities in {filename}:\n{entities}\n{'-'*80}\n")

    with open(ENTITY_OUTPUT, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(all_entities))
    print(f"Entity extraction report saved as {ENTITY_OUTPUT}")

if __name__ == "__main__":
    process_all_transcripts()
