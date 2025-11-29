import os
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv
import json
import re

load_dotenv()
API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)

def extract_text_from_pdf(pdf_path, max_pages=20):
    """Extract text from PDF (limit to first max_pages for speed)"""
    try:
        pdf_reader = PdfReader(pdf_path)
        text = ""
        num_pages = min(len(pdf_reader.pages), max_pages)
        
        for i in range(num_pages):
            page_text = pdf_reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
        
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def generate_quiz_questions(pdf_text, num_questions=10):
    """Generate MCQ questions from PDF text using Gemini AI"""
    
    prompt = f"""
    Based on the following text, generate {num_questions} multiple choice questions (MCQs) that test understanding of the key concepts.
    
    For each question:
    1. Create a clear, specific question
    2. Provide exactly 4 options (A, B, C, D)
    3. Mark the correct answer
    4. Make sure questions test important concepts, not trivial details
    
    Format your response as a JSON array with this exact structure:
    [
        {{
            "question": "Question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Brief explanation of why this is correct"
        }}
    ]
    
    Important: 
    - correct_answer should be the index (0-3) of the correct option
    - Make questions challenging but fair
    - Ensure all options are plausible
    - Return ONLY the JSON array, no other text
    
    TEXT TO ANALYZE:
    {pdf_text[:15000]}
    
    Generate the {num_questions} MCQ questions now in JSON format:
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        response_text = response.text.strip()
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        
        # Parse JSON
        questions = json.loads(response_text)
        
        # Validate and clean questions
        validated_questions = []
        for q in questions:
            if all(key in q for key in ['question', 'options', 'correct_answer']):
                if len(q['options']) == 4 and 0 <= q['correct_answer'] <= 3:
                    validated_questions.append(q)
        
        return validated_questions[:num_questions]
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

def generate_quiz_from_pdf(pdf_path, num_questions=10):
    """Main function to generate quiz from PDF"""
    
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    if not pdf_text or len(pdf_text) < 100:
        return None, "Could not extract sufficient text from PDF"
    
    # Generate questions using AI
    questions = generate_quiz_questions(pdf_text, num_questions)
    
    if not questions:
        return None, "Could not generate questions from PDF content"
    
    return questions, None
