import os
import pandas as pd

# Define directories
ANALYSIS_DIR = "data/analysis"
REPORT_OUTPUT = "data/analysis/reports.txt"

def generate_reports():
    entity_file = os.path.join(ANALYSIS_DIR, "entity_extraction.txt")
    topic_file = os.path.join(ANALYSIS_DIR, "topic_modeling.txt")
    sentiment_file = os.path.join(ANALYSIS_DIR, "sentiment_analysis.txt")
    keyword_file = os.path.join(ANALYSIS_DIR, "keyword_extraction.txt")
    summary_file = os.path.join(ANALYSIS_DIR, "summaries.txt")

    with open(REPORT_OUTPUT, "w", encoding="utf-8") as out_f:
        for file in [entity_file, topic_file, sentiment_file, keyword_file, summary_file]:
            if os.path.exists(file):
                with open(file, "r", encoding="utf-8") as f:
                    out_f.write(f.read())
                    out_f.write("\n\n")
    print(f"Reports generated and saved as {REPORT_OUTPUT}")

if __name__ == "__main__":
    generate_reports()
