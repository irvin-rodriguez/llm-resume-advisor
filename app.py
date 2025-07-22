"""
app.py
Main Streamlit application for the AI Resume Analyzer.
Allows user to upload resumes, input desired job title and descriptions, and recieve specific feedback.
"""

import streamlit as st 
from resume_parser import read_pdf, read_docx
from llm_utils import get_resume_feedback

st.title("AI Resume Analyzer")

job_pos = st.text_input("Write job title of the position you are applying for here:")
job_desc = st.text_area("Paste the job description here:", height=200)
uploaded_file = st.file_uploader("Upload your resume here (PDF or DOCX)", type=['pdf', 'docx'])

if uploaded_file:
    if uploaded_file.name.endswith('.pdf'):
        resume_text = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        resume_text = read_docx(uploaded_file)
    
    st.subheader("Extracted Resume Text")
    st.text_area("Your Resume Content:", resume_text, height=400)

    if (job_desc and job_pos and st.button("Get Resume Feedback")):
        feedback = get_resume_feedback(resume_text, job_pos, job_desc)
        st.subheader("Suggested Improvements:")
        st.write(feedback)