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
    all_entities = []

    for root, _, files in os.walk(PREPROCESSED_DIR):
        for filename in files:
            if filename.endswith(".txt") and filename != "speaker_names.txt":
                transcript_path = os.path.join(root, filename)
                with open(transcript_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    entities = entity_recognition(text)
                    webinar_name = os.path.splitext(os.path.basename(filename))[0]
                    entity_output = f"Entities in {webinar_name}:\n"
                    for entity_type, entity_list in entities.items():
                        entity_output += f"{entity_type}:\n" + "\n".join(entity_list) + "\n"
                    entity_output += "-"*80 + "\n"
                    all_entities.append(entity_output)

    with open(ENTITY_OUTPUT, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(all_entities))
    print(f"Entity extraction report saved as {ENTITY_OUTPUT}")

if __name__ == "__main__":
    process_all_transcripts()
