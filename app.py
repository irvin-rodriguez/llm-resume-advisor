"""
app.py
Main Streamlit application for the AI Resume Analyzer.
Allows user to upload resumes, input desired job title and descriptions, and recieve specific feedback.
"""

import streamlit as st
import pandas as pd
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

            st.session_state.general_feedback = get_general_feedback(
                job_pos, job_desc, st.session_state.parsed_resume)
            st.session_state.desired_skills = get_desired_skills(job_desc)
            st.session_state.skill_match = get_skill_match(
                st.session_state.parsed_resume,
                st.session_state.desired_skills)

            st.session_state.debug_outputs = {
                "parsed_resume": st.session_state.parsed_resume,
                "desired_skills": st.session_state.desired_skills,
                "skill_match": st.session_state.skill_match
            }

            st.session_state.page = "review"
            st.rerun()

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
        # score = st.session_state.resume_analysis["match_score"]
        st.plotly_chart(show_match_gauge(score=50), use_container_width=True)

        with st.expander("Debug Outputs", expanded=False):
            st.json(st.session_state.debug_outputs)

        with st.expander("General Suggestions", expanded=True):
            st.write(st.session_state.general_feedback)

        with st.expander("Hard and Soft Skill Match", expanded=True):
            st.markdown(
                "This table compares desired hard and soft skills from the job description against your resume."
            )

            skill_match = st.session_state.skill_match

            # Create DataFrames for hard and soft skills
            for skill_type, label in [("hard_skills", "Hard Skills"),
                                      ("soft_skills", "Soft Skills")]:
                skill_data = skill_match.get(skill_type, [])
                if skill_data:
                    df = pd.DataFrame(skill_data)
                    df["Present?"] = df["present"].map({True: "✅", False: "❌"})
                    df = df[["skill", "Present?"
                             ]].rename(columns={"skill": f"Desired {label}"})

                    st.markdown(f"### {label}")
                    st.table(df)
                else:
                    st.markdown(f"_No {label.lower()} detected._")

        # with st.expander("Specific Editing", expanded=False):
        #     st.markdown("Highlight or paste a sentence from your resume you'd like to improve.")
        #     to_edit = st.text_area("Paste the sentence to improve:", height=80)

        #     if st.button("Suggest Rewriting"):
        #         if not to_edit.strip():
        #             st.warning("Please paste something from your resume first.")
        #         else:
        #             print("HI")
