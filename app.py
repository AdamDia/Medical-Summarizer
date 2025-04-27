import streamlit as st
from summarizer import summarize_text
import PyPDF2
import re
from pdfGenerator import create_pdf


# --- Page Setup ---
st.set_page_config(page_title="Medical Text Summarizer", layout="centered")
st.title("🧠 AI-Powered Medical Text Summarizer")
st.markdown("Upload a PDF medical report **or** paste one below to generate a summary using an AI model.")

# --- Initialize Session State ---
for key in ["summary", "full_text", "extracted_from_pdf"]:
    if key not in st.session_state:
        st.session_state[key] = 0 if key == "uploader_key" else None

# Special keys that must be integers
for key in ["uploader_key", "text_input_key"]:
    if key not in st.session_state:
        st.session_state[key] = 0

# --- Upload PDF (key changes force reset) ---
uploaded_file = st.file_uploader(
    "Upload a PDF medical report:",
    type=["pdf"],
    key=st.session_state.uploader_key
)
if uploaded_file:
    st.info("📎 PDF uploaded successfully!")

# --- Paste Text Option ---
text_input = st.text_area("Or paste a medical report here:", height=300,  key=f"text_input_{st.session_state.text_input_key}")

# --- PDF Extraction Helpers ---
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

def clean_extracted_text(text: str) -> str:
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

# --- Buttons (Summarize + Clear) ---
col1, col2 = st.columns(2)
with col1:
    summarize_clicked = st.button("Summarize", use_container_width=True)

with col2:
    clear_clicked = st.button("Clear", use_container_width=True)
if summarize_clicked:
        if uploaded_file:
            with st.spinner("🔍 Extracting text from PDF..."):
                raw_text = extract_text_from_pdf(uploaded_file)
                st.session_state.full_text = clean_extracted_text(raw_text)
                st.session_state.extracted_from_pdf = True
            st.success("✅ Text extracted successfully.")
        elif text_input.strip():
            st.session_state.full_text = text_input.strip()
            st.session_state.extracted_from_pdf = False
        else:
            st.warning("⚠️ Please upload a PDF or enter text to summarize.")
            st.stop()

        with st.spinner("🧠 Generating summary..."):
            st.session_state.summary = summarize_text(st.session_state.full_text)

if clear_clicked:
        for key in ["summary", "full_text", "extracted_from_pdf"]:
            st.session_state[key] = None
        st.session_state.uploader_key += 1  # force file uploader to reset
        st.session_state.text_input_key += 1
        st.rerun()

# --- Show Extracted Text Preview (PDF Only) ---
if st.session_state.full_text and st.session_state.extracted_from_pdf:
    with st.expander("🔍 View Extracted Text", expanded=False):
        st.text_area("Extracted Text", st.session_state.full_text, height=300, disabled=True)

# --- Show Summary Output ---
if st.session_state.summary:
    st.subheader("📄 Summary")
    st.success(st.session_state.summary)

    save_as_name = st.text_input(
            "Enter a filename for the downloaded summary PDF:",
            placeholder="Enter file name here",
            max_chars=50,
            key="save_as_name"
        )

    pdf_file = create_pdf(st.session_state.summary)

    download_disabled = save_as_name.strip() == ""

    st.download_button(
            label="📄 Download Summary as PDF",
            data=pdf_file,
            file_name=f"{save_as_name.strip() or 'summary'}.pdf",
            mime="application/pdf",
            disabled=download_disabled  # ✅ This line disables the button if no filename
        )

    if download_disabled:
            st.error("❌ Please enter a filename to enable downloading.")

