# Quiz Topics Feature

## Overview
Teachers can now optionally specify topics when generating quizzes from PDF files. This allows for more focused quizzes on specific subjects within a document.

## How It Works

### For Teachers:
1. Navigate to "Create Quiz" page
2. Select a PDF document
3. Choose the number of questions and duration
4. **NEW**: Enter specific topics in the "Specific Topics" field (optional)
   - Example: `Functions, Classes, Inheritance, Polymorphism`
   - Topics should be comma-separated
5. Click "Generate Quiz with AI"

### Behavior:
- **With Topics**: AI generates questions only about the specified topics from the PDF
- **Without Topics**: AI generates questions from the entire PDF document

## Technical Implementation

### Database Changes
- Added `topics` field to `Quiz` model (TextField, blank=True)
- Migration: `0007_quiz_topics.py`

### Code Changes
1. **teachers/models.py**
   - Added `topics` field to store comma-separated topics

2. **templates/teachers/generate_quiz.html**
   - Added textarea input for topics entry
   - Includes helpful placeholder text and instructions

3. **teachers/quiz_generator.py**
   - Updated `generate_quiz_questions()` to accept `topics` parameter
   - Modified AI prompt to focus on specific topics when provided

4. **teachers/views.py**
   - Retrieves topics from form submission
   - Passes topics to quiz generator
   - Stores topics in quiz description and model

## Example Usage

### Scenario 1: Topic-Specific Quiz
```
Document: "Python Programming - Object Oriented Programming"
Topics: "Inheritance, Polymorphism"
Result: Quiz questions focused only on inheritance and polymorphism concepts
```

### Scenario 2: Full Document Quiz
```
Document: "Python Programming - Object Oriented Programming"
Topics: (empty)
Result: Quiz questions covering all OOP topics in the document
```

## Benefits
- More targeted assessment of specific learning objectives
- Better control over quiz content
- Flexible quiz generation for comprehensive or focused testing
- Saved topics in quiz model for future reference
