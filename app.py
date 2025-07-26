import streamlit as st
from utils import analyze_file, chat_about_uploaded_file
import os

st.set_page_config(page_title="Analyzer Agent", layout="centered")
st.title("📊 Analyzer Agent")

st.sidebar.title("Choose Analyzer")
analyzer_type = st.sidebar.radio("Select what you want to analyze", ("Poster", "Resume", "Article"))

uploaded_file = st.file_uploader(
    "Upload a file (PDF, DOCX, TXT, JPG, PNG)",
    type=["pdf", "docx", "txt", "jpg", "jpeg", "png"]
)

if uploaded_file:
    file_text = uploaded_file.read()
    file_path = f"temp_{uploaded_file.name}"

    # Save uploaded file temporarily
    with open(file_path, "wb") as f:
        f.write(file_text)

    with st.spinner("Analyzing..."):
        result = analyze_file(file_path, analyzer_type)
        st.success("✅ Analysis complete!")
        st.write(result)

    st.divider()
    st.subheader("💬 Ask Questions About This File")
    question = st.text_input("Ask a question about the uploaded file")

    if question:
        with st.spinner("Thinking..."):
            answer = chat_about_uploaded_file(file_path, analyzer_type, question)
            st.write(answer)

    # Clean up temp file
    os.remove(file_path)
