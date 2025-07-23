"""
app.py
Main Streamlit application for the AI Resume Analyzer.
Allows user to upload resumes, input desired job title and descriptions, and recieve specific feedback.
"""

import streamlit as st
from app_utils import read_pdf, show_match_gauge
from llm_utils import *

# ----- Page Settings -----
st.set_page_config(layout="wide")

# ------ Initialize Session State ------
if "page" not in st.session_state:
    st.session_state.page = "form"

if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = None

# ------ Page 1: Submission Form ------
if st.session_state.page == "form":
    st.title("AI Resume Analyzer")

    job_pos = st.text_input(
        "Write job title of the position you are applying for here:")
    job_desc = st.text_area("Paste the job description here:", height=200)
    uploaded_file = st.file_uploader("Upload your resume here (PDF)",
                                     type=['pdf'])

    if job_pos and job_desc and uploaded_file:
        if st.button("Confirm Submission"):
            resume_text = read_pdf(uploaded_file)

            # Store everything in session state
            st.session_state.resume_text = resume_text
            st.session_state.job_position = job_pos
            st.session_state.job_description = job_desc
            st.session_state.parsed_resume = parse_resume(resume_text)
            st.session_state.resume_analysis = analyze_resume(
                job_pos, job_desc, st.session_state.parsed_resume)

            st.session_state.page = "review"

# ----- Page 2: Review Submission -----
elif st.session_state.page == "review":
    back_col, _, _ = st.columns([1, 6, 1])
    with back_col:
        if st.button("Go Back"):
            st.session_state.page = "form"

    col1, col2 = st.columns(2, border=True)

    with col1:
        st.title("Your Resume")
        st.markdown(st.session_state.parsed_resume)
        # st.code(st.session_state.parsed_resume, language="markdown")

    with col2:
        st.title("AI Resume Assistant")

        # Match Gauge
        st.plotly_chart(show_match_gauge(score=50), use_container_width=True)

        with st.expander("General Suggestions", expanded=True):
            if st.button("Generate Suggestions"):
                print("General Suggestions Here")

        with st.expander("Hard and Soft Skill Match", expanded=False):
            if st.button("Analyze Skills"):
                print("Analyzed Skills Here")

        with st.expander("Specific Editing", expanded=False):
            user_input = st.text_area(
                "What part of the resume do you want to rewrite?")
            if st.button("Start Editing Chat"):
                print("Chat Here")

    # # Button to get AI feedback
    # if st.button("Get Resume Feedback"):
    #     feedback = get_general_feedback(
    #         parsed_resume=st.session_state.parsed_resume,
    #         job_pos=st.session_state.job_position,
    #         job_desc=st.session_state.job_description)
    #     st.subheader("Suggested Improvements:")
    #     st.write(feedback)
