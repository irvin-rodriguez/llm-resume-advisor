"""
llm_utils.py
Handles interaction with OpenAI API.
"""
import json

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def parse_resume(resume_text):
    """
    Sends the resume text to OpenAI API and parses it into markdown format.

    Args:
        resume_text (str): The extracted resume text.

    Returns:
        str: Markdown format of given resume.
    """

    prompt = f"""
    You are a professional resume parsing assistant.

    Your task is to convert the following plain text resume into structured **Markdown** format.

    **Instructions:**
    - Preserve the original **section headings** as Markdown `## Heading`.
    - Preserve the original **item titles** (e.g., job titles, degrees, skills) as `### Subheadings` if appropriate.
    - Preserve any bullet points (`- ...`) under their respective items.
    - Fix irregular spacing or line breaks, but **do NOT rewrite, paraphrase, or omit** any content.
    - Maintain the **original order** of all content.
    - Do NOT include any explanations, commentary, or metadata — return only valid markdown.

    Here is the resume:
    {resume_text}

    Return only the markdown.
    """

    response = client.responses.create(model="gpt-3.5-turbo",
                                       input=prompt,
                                       temperature=0)

    return response.output_text


# def analyze_resume(parsed_resume, job_pos, job_desc):
#     """
#     Sends the parsed resume, job title, and description to OpenAI API and retrieves full analysis of it in JSON format.

#     Args:
#         parsed_resume (str): The extracted resume in markdown format.
#         job_pos (str): The target job position.
#         job_desc (str): The job description provided by the user.

#     Returns:
#         str: Feedback from the LLM about suggested resume improvements in JSON format.
#     """

#     prompt = f"""
#     You are a professional resume reviewer specializing in the position of {job_pos}.

#     The following is a resume:
#     {parsed_resume}

#     The user is applying for this specific job:
#     {job_desc}

#     Please analyze the resume and suggest three specific improvements that the user can make to better align the resume with the job description.
#     """

#     response = client.responses.create(model="gpt-3.5-turbo",
#                                        input=prompt,
#                                        temperature=0.5,
#                                        max_output_tokens=500)

#     return response.output_text
