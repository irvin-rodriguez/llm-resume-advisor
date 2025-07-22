"""
llm_utils.py
Handles interaction with OpenAI API for generating resume feedback.
"""

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_resume_feedback(resume_text, job_pos, job_desc):
    """
    Sends the resume text, job title, and description to OpenAI API and retrieves feedback.
    
    Args:
        resume_text (str): The extracted resume text.
        job_pos (str): The target job position.
        job_desc (str): The job description provided by the user.
    
    Returns:
        str: Feedback from the LLM about suggested resume improvements.
    """

    prompt = f"""
    You are a professional resume reviewer specializing in the position of {job_pos}.
    
    The following is a resume:
    {resume_text}

    The user is applying for this specific job:
    {job_desc}

    Please analyze the resume and suggest three specific imporvement that the user can make to better align the resume with the job description.
    """

    response = client.responses.create(
        model="gpt-3.5-turbo", 
        input=prompt, 
        temperature=0.5,
        max_output_tokens=500
    )

    return response.output_text