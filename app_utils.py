import plotly.graph_objects as go
from pdfminer.high_level import extract_text
import docx


def read_pdf(file):
    """
    Extracts text from a PDF file.
    
    Args:
        file (UploadedFile): The uploaded PDF file object.
    
    Returns:
        str: Extracted text content from the PDF.
    """
    return extract_text(file)


def read_docx(file):
    """
    Extracts text from a DOCX file.
    
    Args:
        file (UploadedFile): The uploaded DOCX file object.
    
    Returns:
        str: Extracted text content from the DOCX.
    """
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def show_match_gauge(score: int):
    """
    Generates a gauge chart to visualize how well the resume matches the job description.

    Args:
        score (int): The match score between 0 and 100.
        
    Returns:
        fig (go.Figure): A formatted Plotly gauge indicator ready to be displayed.
    """
    fig = go.Figure(
        go.Indicator(mode="gauge+number",
                     value=score,
                     number={'suffix': "%"},
                     title={'text': "Match Score"},
                     gauge={
                         'axis': {
                             'range': [0, 100]
                         },
                         'bar': {
                             'color': "darkgrey"
                         },
                         'steps': [
                             {
                                 'range': [0, 50],
                                 'color': "red"
                             },
                             {
                                 'range': [50, 75],
                                 'color': "yellow"
                             },
                             {
                                 'range': [75, 100],
                                 'color': "green"
                             },
                         ],
                     }))

    fig.update_layout(
        width=200,  # adjust width
        height=200,  # adjust height
        margin=dict(t=50, b=10, l=10, r=10))

    return fig

def compute_match_score(skill_match):
    """
    Compute the percentage of skills marked as present from skill_match.

    Args:
        skill_match (dict): A dictionary with keys hard/soft skills and whether they are present in the resume.

    Returns:
        int: Match score as an integer (0–100)
    """
    all_skills = skill_match.get("hard_skills", []) + skill_match.get("soft_skills", [])
    num_total = len(all_skills)
    if num_total == 0:
        return 0
    num_present = sum(skill.get("present", False) for skill in all_skills)
    return int((num_present / num_total) * 100)