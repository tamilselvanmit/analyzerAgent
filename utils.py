import os
import fitz  # PyMuPDF
import docx2txt
import easyocr
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# OCR Reader
reader = easyocr.Reader(['en'], gpu=False)

# Extract text from image using EasyOCR
def extract_text_from_image(file_path):
    result = reader.readtext(file_path, detail=0)
    return "\n".join(result)

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def get_file_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    elif file_path.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file_path)
    else:
        return "❌ Unsupported file format."

# Setup Groq LLM
def get_groq_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-8b-8192"
    )

# Main analyzer
def analyze_file(file_path, analyzer_type):
    llm = get_groq_llm()
    text = get_file_text(file_path)

    if analyzer_type == "Poster":
        prompt = f"""You are an event poster analyzer.

Analyze the following content and extract these details in structured format:
- 📌 Title
- 📅 Date
- ⏰ Time
- 📍 Venue
- 📝 Description
- 🧑‍💼 Organizers
- 📞 Contact Info
- 🧾 Additional Notes

Poster Content:
{text}
"""
    elif analyzer_type == "Resume":
        role = "Web Developer"
        prompt = f"""You are a resume screening expert.

Analyze the following resume and provide:
1. Suitability for the {role} role
2. Resume suits the role
3. Justification
4. Suggested Improvements

Resume:
{text}
"""
    else:  # Article
        prompt = f"""Analyze the following article content and extract:
- Title
- Author
- Publication Date
- Summary
- Keywords

Article Content:
{text}
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# Q&A on uploaded file
def chat_about_uploaded_file(file_path, analyzer_type, user_question):
    llm = get_groq_llm()
    text = get_file_text(file_path)

    prompt = f"""Context:
{text}

Question: {user_question}
Answer:"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
