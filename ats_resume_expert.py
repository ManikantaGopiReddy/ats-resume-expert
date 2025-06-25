from dotenv import load_dotenv
import streamlit as st
import os
import io
import fitz  # PyMuPDF
import base64
import docx2txt
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, resume_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, resume_text, prompt])
    return response.text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_data = uploaded_file.read()
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return docx2txt.process(uploaded_file)

    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file type")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF, Word, or Text)...", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.success(f"{uploaded_file.name} uploaded successfully!")

submit1 = st.button("Tell me About the Resume")
submit2 = st.button("How can I Improve my Skills")
submit3 = st.button("Percentage match")
submit4 = st.button("Generate Resume Points for this Position")

# Prompts
input_prompt1 = """You are an experienced HR with Tech experience in Data Science, Full Stack, Web Development, Big Data Engineering, DevOps, and Data Analytics.
Your task is to review the provided resume against the job description. Share your evaluation on alignment, strengths, and weaknesses."""
input_prompt2 = """You are a career coach with expertise in the mentioned fields. Suggest areas for improvement in skills or knowledge based on the job description."""
input_prompt3 = """You are a skilled ATS scanner. Give a percentage match between the resume and job description, list missing keywords, and provide final thoughts."""
input_prompt4 = """Act as a resume expert. Based on the job description, generate optimized resume bullet points that align with the job's key responsibilities and required skills."""

if uploaded_file is not None:
    resume_text = extract_text_from_file(uploaded_file)

    if submit1:
        response = get_gemini_response(input_prompt1, resume_text, input_text)
        st.subheader("Evaluation of Resume")
        st.write(response)

    elif submit2:
        response = get_gemini_response(input_prompt2, resume_text, input_text)
        st.subheader("Skill Improvement Suggestions")
        st.write(response)

    elif submit3:
        response = get_gemini_response(input_prompt3, resume_text, input_text)
        st.subheader("ATS Match Results")
        st.write(response)

    elif submit4:
        response = get_gemini_response(input_prompt4, resume_text, input_text)
        st.subheader("Tailored Resume Points")
        st.write(response)
else:
    if submit1 or submit2 or submit3 or submit4:
        st.warning("Please upload a resume file.")
