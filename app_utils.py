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
                                 'range': [0, 40],
                                 'color': "red"
                             },
                             {
                                 'range': [40, 70],
                                 'color': "yellow"
                             },
                             {
                                 'range': [70, 100],
                                 'color': "green"
                             },
                         ],
                     }))

    fig.update_layout(
        width=200,  # adjust width
        height=200,  # adjust height
        margin=dict(t=50, b=10, l=10, r=10))

    return fig
