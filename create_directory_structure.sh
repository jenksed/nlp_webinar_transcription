#!/bin/bash

# Set up directories
echo "Creating project directories..."
mkdir -p data/raw_transcripts
mkdir -p data/preprocessed
mkdir -p data/summaries
mkdir -p data/analysis
mkdir -p data/audio
mkdir -p src/preprocessing
mkdir -p src/analysis
mkdir -p src/report_generation
mkdir -p src/utils
mkdir -p config
mkdir -p tests
mkdir -p docs
mkdir -p notebooks

# Create README and guide files
echo "Creating documentation files..."
touch docs/README.md
touch docs/user_guide.md
touch docs/developer_guide.md

# Create Python script files
echo "Creating Python script files..."
touch src/preprocessing/preprocess_text.py
touch src/preprocessing/transcribe_mp3.py
touch src/analysis/entity_recognition.py
touch src/analysis/topic_modeling.py
touch src/analysis/sentiment_analysis.py
touch src/analysis/keyword_extraction.py
touch src/analysis/summarize_text.py
touch src/report_generation/generate_reports.py
touch src/report_generation/create_webinar_report.py
touch src/utils/file_utils.py
touch src/utils/logging_utils.py
touch config/config.py

# Create test files
echo "Creating test files..."
touch tests/test_preprocessing.py
touch tests/test_analysis.py
touch tests/test_reporting.py

# Create requirements.txt
echo "Creating requirements.txt..."
cat <<EOT >> requirements.txt
spacy
nltk
gensim
transformers
pandas
numpy
scikit-learn
whisper
pydub
pytest
coverage
pre-commit
EOT

# Initialize Git repository
echo "Initializing Git repository..."
git init

# Create virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Deactivate virtual environment
deactivate

# Final message
echo "Project setup complete. To start working, activate the virtual environment using 'source venv/bin/activate'."
