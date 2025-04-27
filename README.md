# 🧠 AI-Powered Medical Text Summarizer

A lightweight web application that summarizes long medical reports using Hugging Face NLP models, with an easy-to-use Streamlit interface.

---

## 🔧 Features
- Upload medical reports as PDF or paste text manually
- Summarize content automatically via Hugging Face Inference API
- Download the generated summary as a PDF
- Filename validation before allowing download
- Clean UI with proper error handling and input management

---

## 🚀 Installation

### Option 1: Using Conda (Recommended)

It is recommended to create an isolated environment:

```bash
# Create a new environment
conda create -n medical-summarizer python=3.10

# Activate the environment
conda activate medical-summarizer

# Install dependencies
pip install -r requirements.txt


Option 2: Using Pip Only
pip install -r requirements.txt

Running the Application
streamlit run app.py


🤖 Model
Uses Hugging Face Inference API with google/pegasus-xsum as the default summarization model.

Other supported models (easily switchable by changing API_URL inside summarizer.py):

t5-base

google/flan-t5-large

Important:

You do NOT need to download large models locally.

The app calls Hugging Face hosted models via API for efficiency.

🔑 Important Note on Hugging Face API Token
For ease of testing, a free temporary Hugging Face API token has already been included directly in the summarizer.py file.
This token allows instructors and reviewers to run the application immediately without needing to create a new token.

Note:
This token will be revoked after grading.


📂 Project Structure
├── app.py              # Streamlit frontend
├── summarizer.py       # Hugging Face API interaction
├── pdfGenerator.py     # PDF generation utility
├── requirements.txt    # Project dependencies
├── .gitignore          # Ignored files and folders
├── README.md           # Project overview

##  Demo
![PCS](https://github.com/user-attachments/assets/0406cb05-2d4b-4465-be6a-33830fe306f7)
