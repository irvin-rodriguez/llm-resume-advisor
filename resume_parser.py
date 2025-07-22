"""
resume_parser.py
Handles reading and extracting text from an uploaded resume (PDF or DOCX).
"""

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
