# Student Campus - AI-Powered Learning Management System

A comprehensive Django-based learning management system that integrates AI capabilities for enhanced educational experiences.

## Features

### For Teachers
- **Dashboard**: Manage subjects, students, and course materials
- **Subject Management**: Create and organize subjects with PDF notes
- **AI Quiz Generator**: Automatically generate quizzes from PDF content using Gemini AI
- **Quiz Analytics**: Track student performance with detailed analytics
- **Chat System**: Direct messaging with students, share files and notes

### For Students
- **Dashboard**: Access all subjects and learning materials
- **Magnify Learning**: AI-powered PDF chat for asking questions about course materials
- **Summarizer**: Generate AI summaries of uploaded documents
- **Quiz System**: 
  - Take quizzes with timer
  - Progress tracker (attempted/remaining questions)
  - Detailed results with answer review
- **Knowledge Bot**: Wikipedia-powered chatbot for general knowledge questions
- **Chat System**: Communicate with teachers, receive files and notes

## Technology Stack

- **Backend**: Django 5.2.8
- **Frontend**: Bootstrap 5.3.0 with Bootstrap Icons
- **AI**: Google Gemini 2.5 Flash
- **Database**: SQLite (development)
- **PDF Processing**: PyPDF2, LangChain, FAISS
- **APIs**: Wikipedia API for Knowledge Bot

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Roshan0909/LangChain-PDF-Processor.git
cd gemini
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
API_KEY="your_gemini_api_key"
WIKIPEDIA_CLIENT_ID="your_wikipedia_client_id"
WIKIPEDIA_CLIENT_SECRET="your_wikipedia_client_secret"
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Access the application at `http://localhost:8000`

## Project Structure

```
gemini/
├── authentication/          # User authentication and management
├── teachers/               # Teacher functionalities
│   ├── models.py          # Subject, Quiz, Question, ChatMessage models
│   ├── views.py           # Teacher views and logic
│   ├── quiz_generator.py  # AI quiz generation
│   └── templates/         # Teacher templates
├── students/              # Student functionalities
│   ├── models.py         # Student models
│   ├── views.py          # Student views and logic
│   ├── utils.py          # PDF processing utilities
│   └── templates/        # Student templates
├── templates/            # Shared templates
├── media/               # User uploads (PDFs, chat files)
├── faiss_index/         # Vector embeddings for PDF search
└── student_campus/      # Django project settings
```

## Key Features Explained

### AI Quiz Generation
- Upload PDF course materials
- AI automatically generates multiple-choice questions
- Customizable number of questions and duration
- Questions test key concepts from the material

### PDF Chat (Magnify Learning)
- Upload any PDF document
- Ask questions about the content
- AI retrieves relevant sections and provides answers
- Maintains chat history per document

### Knowledge Bot
- Wikipedia-powered Q&A system
- Search and display information from Wikipedia articles
- Includes source citations
- Clean chat interface

### Chat System
- Real-time messaging between teachers and students
- File sharing (images, documents)
- PDF note attachments from course materials
- Non-scrollable page with scrollable messages area

### Quiz Taking Experience
- Timed quizzes with countdown
- Real-time progress tracking (attempted/remaining)
- Progress bar showing completion percentage
- Detailed results with correct/incorrect answers
- Option to review all questions and explanations

## User Roles

### Teacher
- Create and manage subjects
- Upload PDF course materials
- Generate AI-powered quizzes
- View student performance analytics
- Chat with students
- Share files and notes

### Student
- Access all subjects and materials
- Take quizzes with timer
- Use AI PDF chat for learning
- Generate document summaries
- Ask general knowledge questions
- Chat with teachers

## Configuration

### Logging
Server request logging is configured to ERROR level only in `student_campus/settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

### Media Files
- PDFs: `media/pdfs/`
- Chat files: `media/chat_files/YYYY/MM/DD/`
- Vector embeddings: `faiss_index/`

## API Keys Required

1. **Google Gemini API**: For AI features (quiz generation, PDF chat, summarization)
   - Get from: https://makersuite.google.com/app/apikey

2. **Wikipedia API** (Optional): For Knowledge Bot
   - Client ID and Secret from Wikipedia API

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue on GitHub.
