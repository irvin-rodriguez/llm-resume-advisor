# AI Resume Analyzer

**Goal**: This project was built to learn how to integrate and engineer with the OpenAI API, explore prompt design for multi-step tasks, and structure a lightweight application that showcases real-world use of language models.

## Overview

The AI Resume Analyzer is a two-page Streamlit app that allows users to upload a resume and paste a job description. It uses OpenAI's GPT models to:

- Parse the raw resume into structured markdown
- Extract desired hard and soft skills from a job posting
- Determine which of those skills are present in the resume (using semantic reasoning)
- Provide general feedback on how well the resume aligns with the job
- Display results in a clean, interactive dashboard

## Key Features

- **LLM Integration**: Multiple OpenAI GPT-4 endpoints are used for parsing, reasoning, and skill matching.
- **Prompt Engineering**: Each task is wrapped in a carefully structured prompt designed for a specific function—e.g., parsing markdown, identifying implied skills, generating qualitative feedback.
- **Function Calling**: The app leverages OpenAI's function-calling tools to extract and return structured data from unstructured job descriptions.
- **Interactive UI**: Utilizes Streamlit to proide an interface where users can upload their resumes and recieve feedback seamlessly.
- **Match Score Visualization**: A Plotly gauge chart gives an at-a-glance measure of how well the resume fits the job description.

## Skills Practiced

This project was designed to strengthen competencies in:

- Calling the OpenAI API via the `openai` Python
- Designing chain-of-thought prompts for LLM-assisted analysis
- Building modular, testable prompt pipelines
- Using JSON schema tools with function-calling to structure LLM outputs
- Deploying interactive applications using Streamlit

## How It Works

1. **User uploads resume** → Extracted with `pdfminer` or `docx`.
2. **Job description is parsed** → GPT extracts hard and soft skills into JSON via function-calling.
3. **Resume is parsed into Markdown** → Clean structure, no rewriting.
4. **Skill matching** → GPT semantically compares each skill to the resume.
5. **Feedback generated** → GPT gives critiques tailored to the job.
6. **Results displayed** → Skill match table, match score gauge, feedback text.

## Why This Project

This was a learning exercise to build fluency with LLM tools in a real-world workflow. The project simulates an end-to-end AI assistant that reads human language, reasons about it, and returns helpful structured feedback.

