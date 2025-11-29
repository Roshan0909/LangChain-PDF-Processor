import os
from google import genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
import io

load_dotenv()
API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)

def summarize_text(text, summary_type="concise"):
    """Summarize text using Gemini AI"""
    
    if summary_type == "concise":
        prompt = f"""
        Summarize the following text in a concise, easy-to-understand manner. 
        Focus on the key points and main ideas. Make it suitable for quick learning.
        Use bullet points where appropriate.
        
        Text to summarize:
        {text}
        
        Provide a clear, concise summary:
        """
    elif summary_type == "detailed":
        prompt = f"""
        Provide a detailed summary of the following text.
        Break it down into sections with headings.
        Explain the key concepts thoroughly.
        Include important examples or details.
        
        Text to summarize:
        {text}
        
        Provide a comprehensive summary:
        """
    else:  # bullet points
        prompt = f"""
        Summarize the following text as clear, organized bullet points.
        Group related points under headings.
        Make it easy to scan and memorize.
        
        Text to summarize:
        {text}
        
        Provide bullet-point summary:
        """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def extract_text_from_pdf_file(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return None

def extract_text_from_docx_file(docx_file):
    """Extract text from uploaded Word document"""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return None
