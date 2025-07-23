"""
llm_utils.py
Handles interaction with OpenAI API.
"""
import json
import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

MODE = "prototype"  # or 'production'

MODEL_LOOKUP = {
    "prototype": {
        "parse_resume": "gpt-3.5-turbo",
        "get_general_feedback": "gpt-3.5-turbo",
        "get_desired_skills": "gpt-3.5-turbo",
        "get_skill_match": "gpt-3.5-turbo"
    },
    "production": {
        "parse_resume": "gpt-4-1106-preview",
        "get_general_feedback": "gpt-4-1106-preview",
        "get_desired_skills": "gpt-4-1106-preview",
        "get_skill_match": "gpt-4-1106-preview"
    }
}


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

    response = client.responses.create(
        model=MODEL_LOOKUP[MODE]["parse_resume"], input=prompt, temperature=0)

    return response.output_text


def get_general_feedback(job_pos, job_desc, parsed_resume):
    """
    Sends the parsed resume, job title, and job description to the OpenAI API 
    and retrieves general feedback about the resume’s alignment with the role.

    Args:
        job_pos (str): The job title being applied for.
        job_desc (str): The full job description text.
        parsed_resume (str): The resume content in markdown format.

    Returns:
        str: A paragraph of general feedback text.
    """

    # Construct the user message
    user_message = {
        "role":
        "user",
        "content":
        f"""
        You are a professional resume assistant. Your task is to review the following resume in the context of a specific job title and job description.

        Your goal is to provide **concise, helpful, and constructive feedback** to help the applicant improve their resume.

        **Instructions:**
        - Write 1 paragraph of general feedback about how well the resume aligns with the job.
        - Focus on tone, structure, relevance of experience, clarity, and areas for improvement.
        - Do NOT list skills or rewrite text — just offer feedback.
        - Your feedback should be specific to the provided job title and description.

        **Job Title**: {job_pos}  
        **Job Description**:  
        {job_desc}

        **Resume (Markdown format)**:  
        {parsed_resume}
        """
    }

    response = client.chat.completions.create(
        model=MODEL_LOOKUP[MODE]["get_general_feedback"],
        messages=[user_message],
        temperature=0.5)

    return response.choices[0].message.content


def get_desired_skills(job_desc):
    """
    Extracts desired hard and soft skills from a job description using the OpenAI API.

    Args:
        job_desc (str): The full job description text.

    Returns:
        dict: A dictionary with two keys:
            - "hard_skills": list of technical or domain-specific skills
            - "soft_skills": list of interpersonal or behavioral skills
    """

    # Define JSON tool schema
    tools = [{
        "type": "function",
        "function": {
            "name": "extract_skills",
            "description":
            "Extracts hard and soft skills from a job description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hard_skills": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Technical or domain-specific skills"
                    },
                    "soft_skills": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Interpersonal or behavioral skills"
                    }
                },
                "required": ["hard_skills", "soft_skills"]
            }
        }
    }]

    # Construct the user message
    user_message = {
        "role":
        "user",
        "content":
        f"""
        You are a resume analysis assistant.

        Your task is to extract a clean list of **hard skills** and **soft skills** that are desired or required based on the job description provided below.

        - A hard skill is a technical, measurable, or domain-specific skill (e.g., Python, CAD, SEO, Machine Learning, SQL).
        - A soft skill is a behavioral, interpersonal, or communication skill (e.g., teamwork, adaptability, leadership).

        Return your answer in the structure defined by the provided tool.

        Here is the job description:
        {job_desc}
        """
    }

    response = client.chat.completions.create(
        model=MODEL_LOOKUP[MODE]["get_desired_skills"],
        messages=[user_message],
        tools=tools,
        tool_choice="auto",
        temperature=0.3)

    tool_output = response.choices[0].message.tool_calls[0].function.arguments

    try:
        return json.loads(tool_output)
    except json.JSONDecodeError:
        st.error("Could not parse extracted skills as JSON. Raw output:")
        st.code(tool_output)
        raise


def get_skill_match(parsed_resume, desired_skills):
    """
    Compares the resume to the list of desired skills and checks if each is present.

    Args:
        parsed_resume (str): The resume in markdown format.
        desired_skills (dict): Dict with "hard_skills" and "soft_skills" lists.

    Returns:
        list of dicts: Each with {type, skill, present_in_resume}.
    """

    tools = [{
        "type": "function",
        "function": {
            "name": "match_skills",
            "description":
            "Checks whether each desired skill appears in the resume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hard_skills": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "skill": {
                                    "type": "string"
                                },
                                "present": {
                                    "type": "boolean"
                                }
                            },
                            "required": ["skill", "present"]
                        }
                    },
                    "soft_skills": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "skill": {
                                    "type": "string"
                                },
                                "present": {
                                    "type": "boolean"
                                }
                            },
                            "required": ["skill", "present"]
                        }
                    }
                },
                "required": ["hard_skills", "soft_skills"]
            }
        }
    }]

    # Create formatted skill lists as input
    hard_list = ", ".join(desired_skills.get("hard_skills", []))
    soft_list = ", ".join(desired_skills.get("soft_skills", []))
    print("hard list: ", hard_list)
    print("soft list: ", soft_list)

    user_message = {
        "role":
        "user",
        "content":
        f"""
        You are a resume skill matching assistant.

        Your task is to determine whether each **desired skill** is present in the applicant's resume.

        **Instructions:**
        - A skill counts as **present** if it is explicitly listed OR clearly implied through work experience, tools, or projects.
        - Use **semantic matching** — do not rely on exact word matches.
        - Think carefully about phrasing. For example:
        - If the resume says “built models using TensorFlow,” mark “TensorFlow” as **present**.
        - If “team collaboration” is described in a project, mark “Teamwork” as **present**.

        Return results using the following tool schema, where `"present": `true` or `false` for each skill.

       **Desired Hard Skills:**
        {hard_list}

        **Desired Soft Skills:**
        {soft_list}

        **Resume (in Markdown format):**
        {parsed_resume}
        """
    }

    # Send request
    response = client.chat.completions.create(
        model=MODEL_LOOKUP[MODE]["get_skill_match"],
        messages=[user_message],
        tools=tools,
        tool_choice="auto",
        temperature=0.2)

    tool_output = response.choices[0].message.tool_calls[0].function.arguments

    try:
        return json.loads(tool_output)
    except json.JSONDecodeError:
        st.error("Could not parse skill match results. Here's the raw output:")
        st.code(tool_output)
        raise
