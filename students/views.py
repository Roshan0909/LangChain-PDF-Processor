from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Max
from teachers.models import Subject, PDFNote, ChatMessage
from .models import ChatHistory
from .utils import get_answer_for_pdf
from authentication.models import User
import json
import requests

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subjects = Subject.objects.all()
    return render(request, 'students/dashboard.html', {'subjects': subjects})

@login_required
def student_subject_detail(request, subject_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subject = get_object_or_404(Subject, id=subject_id)
    notes = subject.notes.all()
    
    return render(request, 'students/subject_detail.html', {'subject': subject, 'notes': notes})

@login_required
def magnify_learning(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subjects = Subject.objects.all().prefetch_related('notes')
    return render(request, 'students/magnify_learning.html', {'subjects': subjects})

@login_required
def pdf_chat(request, pdf_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    pdf_note = get_object_or_404(PDFNote, id=pdf_id)
    chat_history = ChatHistory.objects.filter(student=request.user, pdf_note=pdf_note)
    
    return render(request, 'students/pdf_chat.html', {
        'pdf_note': pdf_note,
        'chat_history': chat_history
    })

@login_required
@require_POST
def ask_question(request, pdf_id):
    if not request.user.is_student():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        pdf_note = get_object_or_404(PDFNote, id=pdf_id)
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        # Get previous chat history for context
        previous_chats = ChatHistory.objects.filter(
            student=request.user, 
            pdf_note=pdf_note
        ).order_by('-created_at')[:5]
        
        # Build chat history string
        history_text = ""
        for chat in reversed(previous_chats):
            history_text += f"Q: {chat.question}\nA: {chat.answer}\n\n"
        
        # Get PDF file path
        pdf_path = pdf_note.pdf_file.path
        
        # Get answer using the utility function
        answer = get_answer_for_pdf(pdf_path, question, history_text)
        
        # Save to chat history
        chat = ChatHistory.objects.create(
            student=request.user,
            pdf_note=pdf_note,
            question=question,
            answer=answer
        )
        
        return JsonResponse({
            'success': True,
            'answer': answer,
            'question': question,
            'timestamp': chat.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def upload_and_chat(request):
    if not request.user.is_student():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        pdf_file = request.FILES.get('pdf_file')
        
        if not pdf_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        if not pdf_file.name.endswith('.pdf'):
            return JsonResponse({'error': 'Only PDF files are allowed'}, status=400)
        
        # Check file size (200MB limit)
        if pdf_file.size > 200 * 1024 * 1024:
            return JsonResponse({'error': 'File size exceeds 200MB limit'}, status=400)
        
        # Create a temporary PDFNote for the uploaded file
        # We'll create it under a special "Personal Uploads" subject
        from teachers.models import Subject
        
        # Try to get or create a personal subject for this student
        personal_subject, created = Subject.objects.get_or_create(
            name=f"Personal Uploads - {request.user.username}",
            teacher=request.user,
            defaults={'description': 'Files uploaded for personal learning'}
        )
        
        # Create the PDFNote
        pdf_note = PDFNote.objects.create(
            subject=personal_subject,
            title=pdf_file.name.replace('.pdf', ''),
            pdf_file=pdf_file,
            uploaded_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'redirect_url': f'/student/pdf-chat/{pdf_note.id}/',
            'message': 'File uploaded successfully'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def summarizer(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    return render(request, 'students/summarizer.html')

@login_required
@require_POST
def generate_summary(request):
    if not request.user.is_student():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        from .summarizer_utils import summarize_text, extract_text_from_pdf_file, extract_text_from_docx_file
        
        text = request.POST.get('text', '').strip()
        summary_type = request.POST.get('summary_type', 'concise')
        
        # Check if file was uploaded
        if request.FILES:
            uploaded_file = request.FILES.get('file')
            
            if uploaded_file:
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension == 'pdf':
                    text = extract_text_from_pdf_file(uploaded_file)
                    if not text:
                        return JsonResponse({'error': 'Could not extract text from PDF'}, status=400)
                elif file_extension in ['docx', 'doc']:
                    text = extract_text_from_docx_file(uploaded_file)
                    if not text:
                        return JsonResponse({'error': 'Could not extract text from Word document'}, status=400)
                else:
                    return JsonResponse({'error': 'Unsupported file format. Please upload PDF or Word document.'}, status=400)
        
        if not text or len(text.strip()) < 50:
            return JsonResponse({'error': 'Text is too short. Please provide at least 50 characters.'}, status=400)
        
        # Limit text length
        if len(text) > 50000:
            text = text[:50000]
        
        # Generate summary
        summary = summarize_text(text, summary_type)
        
        return JsonResponse({
            'success': True,
            'summary': summary,
            'original_length': len(text),
            'summary_type': summary_type
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def quiz(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    from teachers.models import Quiz
    quizzes = Quiz.objects.filter(is_active=True).select_related('subject', 'pdf_note').prefetch_related('attempts', 'questions')
    
    # Attach user's attempt to each quiz
    for quiz_obj in quizzes:
        quiz_obj.user_attempt = quiz_obj.attempts.filter(student=request.user, completed_at__isnull=False).first()
    
    return render(request, 'students/quiz.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    from teachers.models import Quiz, QuizAttempt
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = quiz.questions.all()
    
    # Check if already attempted
    existing_attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz, completed_at__isnull=False).first()
    
    return render(request, 'students/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'already_attempted': existing_attempt
    })

@login_required
def quiz_report(request, attempt_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    from teachers.models import QuizAttempt
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user, completed_at__isnull=False)
    
    quiz = attempt.quiz
    questions = quiz.questions.all()
    
    # Build detailed results
    question_results = []
    for question in questions:
        question_id = str(question.id)
        student_answer = attempt.answers.get(question_id)
        is_correct = student_answer == question.correct_answer
        
        result = {
            'question': question,
            'student_answer': student_answer,
            'is_correct': is_correct
        }
        question_results.append(result)
    
    percentage = (attempt.score / quiz.questions.count() * 100) if quiz.questions.count() > 0 else 0
    
    return render(request, 'students/quiz_report.html', {
        'attempt': attempt,
        'quiz': quiz,
        'question_results': question_results,
        'percentage': round(percentage, 2)
    })

@login_required
@require_POST
def submit_quiz(request, quiz_id):
    if not request.user.is_student():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        from teachers.models import Quiz, QuizAttempt, Question
        from django.utils import timezone
        
        quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        # Calculate score and build detailed results
        score = 0
        total_questions = quiz.questions.count()
        correct_answers = {}
        question_details = []
        
        for question in quiz.questions.all():
            question_id = str(question.id)
            student_answer = answers.get(question_id)
            correct_answer = question.correct_answer
            
            is_correct = student_answer == correct_answer
            if is_correct:
                score += 1
                correct_answers[question_id] = True
            else:
                correct_answers[question_id] = False
            
            # Build question detail for report
            question_detail = {
                'id': question.id,
                'text': question.text,
                'student_answer': student_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'type': question.question_type
            }
            
            # Add options for multiple choice
            if question.question_type == 'multiple_choice':
                question_detail['options'] = question.options
            
            question_details.append(question_detail)
        
        # Save attempt
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            student=request.user,
            completed_at=timezone.now(),
            score=score,
            total_points=total_questions,
            answers=answers
        )
        
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        return JsonResponse({
            'success': True,
            'score': score,
            'total': total_questions,
            'percentage': round(percentage, 2),
            'correct_answers': correct_answers,
            'question_details': question_details
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def student_chat(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    # Get all teachers
    teachers = User.objects.filter(role='teacher').order_by('username')
    
    # Get recent conversations with last message
    conversations = []
    for teacher in teachers:
        last_message = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=teacher) | Q(sender=teacher, receiver=request.user)
        ).order_by('-created_at').first()
        
        unread_count = ChatMessage.objects.filter(
            sender=teacher, receiver=request.user, is_read=False
        ).count()
        
        conversations.append({
            'user': teacher,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    # Sort by last message time (most recent first)
    conversations.sort(key=lambda x: x['last_message'].created_at if x['last_message'] else x['user'].date_joined, reverse=True)
    
    return render(request, 'students/chat.html', {
        'conversations': conversations
    })

@login_required
def student_chat_with(request, user_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    other_user = get_object_or_404(User, id=user_id, role='teacher')
    
    # Get all messages between student and teacher
    messages_list = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).select_related('attached_note', 'attached_note__subject').order_by('created_at')
    
    # Mark messages as read
    ChatMessage.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    # Get all available notes (teacher's notes or subject notes)
    available_notes = PDFNote.objects.filter(subject__teacher=other_user).select_related('subject')
    
    return render(request, 'students/chat_conversation.html', {
        'other_user': other_user,
        'messages': messages_list,
        'available_notes': available_notes
    })

@login_required
def knowledge_bot(request):
    """General knowledge chatbot using Wikipedia API and Gemini AI"""
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    from .models import KnowledgeBotHistory
    
    # Get chat history for current student
    chat_history = KnowledgeBotHistory.objects.filter(student=request.user).order_by('created_at')
    
    return render(request, 'students/knowledge_bot.html', {'chat_history': chat_history})

@login_required
def knowledge_bot_ask(request):
    """Handle knowledge bot questions"""
    if not request.user.is_student():
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    
    try:
        from .models import KnowledgeBotHistory
        
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        
        if not question:
            return JsonResponse({'success': False, 'error': 'Question cannot be empty'}, status=400)
        
        # Get recent chat history for context
        recent_history = KnowledgeBotHistory.objects.filter(
            student=request.user
        ).order_by('-created_at')[:5]
        
        history_context = ""
        for hist in reversed(recent_history):
            history_context += f"Previous Q: {hist.question}\nPrevious A: {hist.answer[:200]}...\n\n"
        
        # Search Wikipedia for relevant information
        wiki_context = search_wikipedia(question)
        
        # Check if we got any results
        if not wiki_context.get('context'):
            # Try a simplified search with just key words
            words = question.lower().replace('what is', '').replace('who is', '').replace('where is', '').replace('when is', '').replace('how', '').replace('?', '').strip()
            wiki_context = search_wikipedia(words)
        
        # Generate answer using Gemini AI
        answer = generate_knowledge_answer(question, wiki_context, history_context)
        
        # Save to history
        history_entry = KnowledgeBotHistory.objects.create(
            student=request.user,
            question=question,
            answer=answer,
            sources=wiki_context.get('sources', [])
        )
        
        return JsonResponse({
            'success': True,
            'answer': answer,
            'sources': wiki_context.get('sources', []),
            'timestamp': history_entry.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def search_wikipedia(query):
    """Search Wikipedia for relevant information using proper API"""
    try:
        import os
        from dotenv import load_dotenv
        import google.generativeai as genai
        
        load_dotenv()
        
        # Use Gemini AI to extract the main search topic from the question
        genai.configure(api_key=os.getenv('API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        topic_prompt = f"""Extract the main topic/concept that should be searched on Wikipedia from this question.
Return ONLY the search term(s) that would find the most relevant Wikipedia article.

Examples:
"What is photosynthesis?" → "photosynthesis"
"Who was Albert Einstein?" → "Albert Einstein"
"Define mitosis" → "mitosis"
"Tell me about the pyramids" → "pyramids"
"History of the internet" → "internet history"
"Explain gravity" → "gravity"
"What is quantum physics?" → "quantum physics"

Question: "{query}"
Search term:"""
        
        try:
            topic_response = model.generate_content(topic_prompt)
            search_query = topic_response.text.strip().strip('"\'').lower()
        except:
            # Fallback to original query if AI fails
            search_query = query
        
        # Get credentials from environment
        client_id = os.getenv('WIKIPEDIA_CLIENT_ID')
        client_secret = os.getenv('WIKIPEDIA_CLIENT_SECRET')
        
        # Use Wikipedia API with proper headers
        search_url = "https://en.wikipedia.org/w/api.php"
        
        headers = {
            'User-Agent': 'StudentCampusApp/1.0 (Educational Purpose)'
        }
        
        # Search for relevant articles
        search_params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': search_query,
            'srlimit': 5,
            'srprop': 'snippet'
        }
        
        search_response = requests.get(search_url, params=search_params, headers=headers, timeout=10)
        search_data = search_response.json()
        
        context = ""
        sources = []
        
        if 'query' in search_data and 'search' in search_data['query']:
            results = search_data['query']['search']
            
            if not results:
                return {'context': '', 'sources': []}
            
            # Get the first result's full content
            first_result = results[0]
            title = first_result['title']
            page_id = first_result['pageid']
            
            # Get full page content (not just intro)
            content_params = {
                'action': 'query',
                'format': 'json',
                'pageids': page_id,
                'prop': 'extracts',
                'explaintext': True,
                'exsectionformat': 'plain'
            }
            
            content_response = requests.get(search_url, params=content_params, headers=headers, timeout=10)
            content_data = content_response.json()
            
            if 'query' in content_data and 'pages' in content_data['query']:
                page_content = content_data['query']['pages'][str(page_id)].get('extract', '')
                if page_content:
                    # Get first 3000 characters for comprehensive answer
                    context = f"{title}\n\n{page_content[:3000]}"
                    if len(page_content) > 3000:
                        context += "..."
                    
                    sources.append({
                        'title': title,
                        'url': f"https://en.wikipedia.org/?curid={page_id}"
                    })
                    
                    # Add one more related article if available
                    if len(results) > 1:
                        second_result = results[1]
                        second_title = second_result['title']
                        second_page_id = second_result['pageid']
                        
                        content_params['pageids'] = second_page_id
                        content_response = requests.get(search_url, params=content_params, headers=headers, timeout=10)
                        content_data = content_response.json()
                        
                        if 'query' in content_data and 'pages' in content_data['query']:
                            second_content = content_data['query']['pages'][str(second_page_id)].get('extract', '')
                            if second_content:
                                context += f"\n\nRelated: {second_title}\n\n{second_content[:1000]}"
                                sources.append({
                                    'title': second_title,
                                    'url': f"https://en.wikipedia.org/?curid={second_page_id}"
                                })
        
        return {'context': context, 'sources': sources}
        
    except Exception as e:
        return {'context': '', 'sources': []}

def generate_knowledge_answer(question, wiki_context, history_context=""):
    """Format answer using Gemini AI with Wikipedia content"""
    try:
        import os
        from dotenv import load_dotenv
        import google.generativeai as genai
        
        load_dotenv()
        
        context = wiki_context.get('context', '').strip()
        
        if context and len(context) > 50:
            # Use Gemini AI to format and improve the answer
            genai.configure(api_key=os.getenv('API_KEY'))
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            prompt = f"""You are a knowledgeable educational assistant providing definitions, history, and informational content from Wikipedia.

Your role is to provide:
- Definitions and explanations of terms and concepts
- Historical information and background
- Biographical information about people
- General informational content

You should NOT provide:
- Step-by-step procedures or instructions
- Causes or reasons (just define the topic)
- Process explanations or "how to" guides

Student's Question: {question}

{f"Recent Conversation Context:\n{history_context}\n" if history_context else ""}Wikipedia Information:
{context}

Instructions:
1. Provide definitions, explanations, and informational content
2. Focus on WHAT something is, WHO someone was, and HISTORICAL context
3. If asked about causes, processes, or "how to" - politely explain you provide definitions and information only
4. Use clear structure with bullet points for key facts
5. Make it educational and conversational
6. Format with proper paragraphs (double line breaks)
7. Include interesting facts and context where helpful
8. Keep answers focused on defining and explaining the topic

Format properly with clear paragraphs and structure.

Provide the answer:"""
            
            response = model.generate_content(prompt)
            answer = response.text.strip()
            
            return answer
        else:
            return ("I couldn't find relevant information on Wikipedia for your question. "
                   "Please try:\n\n"
                   "• Using simpler keywords\n"
                   "• Checking your spelling\n"
                   "• Asking about a different topic\n\n"
                   "Examples: 'photosynthesis', 'Albert Einstein', 'solar system', 'Python programming'")
        
    except Exception as e:
        # Fallback to Wikipedia content if Gemini fails
        context = wiki_context.get('context', '').strip()
        if context and len(context) > 50:
            return context
        return f"I apologize, but I encountered an error: {str(e)}"

@login_required
def leaderboard(request):
    """Display creative leaderboard with AI-powered suggestions"""
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    from .leaderboard_utils import get_leaderboard_data, generate_personalized_suggestion, generate_overall_insights
    
    # Get leaderboard data
    leaderboard_data = get_leaderboard_data()
    
    # Find current student's data
    current_student_data = None
    for entry in leaderboard_data:
        if entry['student'].id == request.user.id:
            current_student_data = entry
            break
    
    # Generate AI suggestion for current student
    ai_suggestion = None
    if current_student_data:
        ai_suggestion = generate_personalized_suggestion(
            current_student_data,
            {'total_students': len(leaderboard_data)}
        )
    
    # Generate overall insights
    overall_insights = generate_overall_insights(leaderboard_data)
    
    return render(request, 'students/leaderboard.html', {
        'leaderboard': leaderboard_data,
        'current_student_data': current_student_data,
        'ai_suggestion': ai_suggestion,
        'overall_insights': overall_insights,
        'total_students': len(leaderboard_data)
    })
