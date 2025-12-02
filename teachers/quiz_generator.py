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

def generate_quiz_questions(pdf_text, num_questions=10, topics=None):
    """Generate MCQ questions from PDF text using Gemini AI"""
    
    # Build the prompt with topics if provided
    if topics and topics.strip():
        topic_instruction = f"\n\nIMPORTANT: Generate questions ONLY about the following topics: {topics}\nFocus exclusively on these topics and ignore other content in the text."
    else:
        topic_instruction = ""
    
    prompt = f"""You are a quiz generator. Based on the following text, generate exactly {num_questions} multiple choice questions.{topic_instruction}

TEXT:
{pdf_text[:15000]}

Generate {num_questions} multiple choice questions in this EXACT JSON format (no other text):
[
  {{
    "question": "What is...",
    "options": ["Answer 1", "Answer 2", "Answer 3", "Answer 4"],
    "correct_answer": 0
  }}
]

Rules:
- Each question must have exactly 4 options
- correct_answer is the index (0, 1, 2, or 3) of the correct option
- Questions should test key concepts from the text
- Return ONLY valid JSON, nothing else"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.7,
                "response_mime_type": "application/json"
            }
        )
        
        response_text = response.text.strip()
        
        # Try to extract JSON if wrapped in markdown
        if "```" in response_text:
            # Find JSON content between code blocks
            lines = response_text.split('\n')
            json_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block or (line.strip().startswith('[') or line.strip().startswith('{')):
                    json_lines.append(line)
            
            response_text = '\n'.join(json_lines).strip()
        
        # Remove any remaining markdown
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        questions = json.loads(response_text)
        
        if not isinstance(questions, list):
            print(f"Response is not a list: {type(questions)}")
            return []
        
        # Validate and clean questions
        validated_questions = []
        for q in questions:
            if isinstance(q, dict) and all(key in q for key in ['question', 'options', 'correct_answer']):
                if isinstance(q['options'], list) and len(q['options']) == 4:
                    if isinstance(q['correct_answer'], int) and 0 <= q['correct_answer'] <= 3:
                        validated_questions.append(q)
        
        if len(validated_questions) == 0:
            print(f"No valid questions found. Raw response: {response_text[:500]}")
        
        return validated_questions[:num_questions]
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text[:500]}")
        return []
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

def generate_quiz_from_pdf(pdf_path, num_questions=10, topics=None):
    """Main function to generate quiz from PDF"""
    
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    if not pdf_text or len(pdf_text) < 100:
        return None, "Could not extract sufficient text from PDF"
    
    # Generate questions using AI
    questions = generate_quiz_questions(pdf_text, num_questions, topics)
    
    if not questions:
        return None, "Could not generate questions from PDF content"
    
    return questions, None
