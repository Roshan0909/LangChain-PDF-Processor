"""
Reports module for teachers - Generate and filter quiz reports with PDF export
"""
from django.db.models import Q, Count, Avg, Max, Min
from teachers.models import Quiz, QuizAttempt, Question
from django.utils import timezone
from datetime import timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import json


class QuizReportFilter:
    """Handle filtering of quiz reports based on various criteria"""
    
    def __init__(self, teacher):
        self.teacher = teacher
        self.filters = {}
    
    def set_quiz_filter(self, quiz_id):
        """Filter by specific quiz"""
        self.filters['quiz_id'] = quiz_id
        return self
    
    def set_subject_filter(self, subject_id):
        """Filter by subject"""
        self.filters['subject_id'] = subject_id
        return self
    
    def set_date_range_filter(self, start_date, end_date):
        """Filter by date range"""
        self.filters['start_date'] = start_date
        self.filters['end_date'] = end_date
        return self
    
    def set_score_range_filter(self, min_score, max_score):
        """Filter by score range"""
        self.filters['min_score'] = min_score
        self.filters['max_score'] = max_score
        return self
    
    def set_student_filter(self, student_id):
        """Filter by specific student"""
        self.filters['student_id'] = student_id
        return self
    
    def set_completion_filter(self, completed_only=True):
        """Filter by completion status"""
        self.filters['completed_only'] = completed_only
        return self
    
    def set_difficulty_filter(self, difficulty):
        """Filter by quiz difficulty"""
        self.filters['difficulty'] = difficulty
        return self
    
    def set_search_filter(self, search_text):
        """Search in quiz title or student name"""
        self.filters['search'] = search_text
        return self
    
    def get_attempts(self):
        """Get filtered quiz attempts"""
        query = QuizAttempt.objects.filter(quiz__created_by=self.teacher).select_related(
            'quiz', 'student'
        ).prefetch_related('quiz__questions')
        
        # Apply filters
        if 'quiz_id' in self.filters:
            query = query.filter(quiz_id=self.filters['quiz_id'])
        
        if 'subject_id' in self.filters:
            query = query.filter(quiz__subject_id=self.filters['subject_id'])
        
        if 'student_id' in self.filters:
            query = query.filter(student_id=self.filters['student_id'])
        
        if 'completed_only' in self.filters and self.filters['completed_only']:
            query = query.filter(completed_at__isnull=False)
        
        if 'difficulty' in self.filters:
            query = query.filter(quiz__difficulty=self.filters['difficulty'])
        
        if 'start_date' in self.filters and self.filters['start_date']:
            query = query.filter(completed_at__gte=self.filters['start_date'])
        
        if 'end_date' in self.filters and self.filters['end_date']:
            end_date = self.filters['end_date']
            # Include entire day
            end_date_end = end_date.replace(hour=23, minute=59, second=59)
            query = query.filter(completed_at__lte=end_date_end)
        
        if 'min_score' in self.filters and self.filters['min_score'] is not None:
            query = query.filter(score__gte=self.filters['min_score'])
        
        if 'max_score' in self.filters and self.filters['max_score'] is not None:
            query = query.filter(score__lte=self.filters['max_score'])
        
        if 'search' in self.filters and self.filters['search']:
            search_text = self.filters['search']
            query = query.filter(
                Q(quiz__title__icontains=search_text) |
                Q(student__username__icontains=search_text) |
                Q(student__first_name__icontains=search_text) |
                Q(student__last_name__icontains=search_text)
            )
        
        return query.order_by('-completed_at')
    
    def get_statistics(self):
        """Get aggregate statistics for filtered data"""
        attempts = self.get_attempts()
        completed_attempts = attempts.filter(completed_at__isnull=False)
        
        stats = {
            'total_attempts': attempts.count(),
            'completed_attempts': completed_attempts.count(),
            'avg_score': None,
            'max_score': None,
            'min_score': None,
            'avg_percentage': None,
            'unique_students': attempts.values('student').distinct().count(),
            'total_quizzes': attempts.values('quiz').distinct().count(),
        }
        
        if completed_attempts.exists():
            agg = completed_attempts.aggregate(
                avg_score=Avg('score'),
                max_score=Max('score'),
                min_score=Min('score'),
                avg_total=Avg('total_points')
            )
            stats['avg_score'] = round(agg['avg_score'], 2) if agg['avg_score'] else 0
            stats['max_score'] = agg['max_score']
            stats['min_score'] = agg['min_score']
            
            if agg['avg_total'] and agg['avg_total'] > 0:
                stats['avg_percentage'] = round((agg['avg_score'] / agg['avg_total']) * 100, 2)
        
        return stats


class QuizReportGenerator:
    """Generate detailed PDF reports from filtered quiz data"""
    
    def __init__(self, filter_obj):
        self.filter_obj = filter_obj
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom ReportLab styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT
        ))
    
    def generate_pdf(self, filename=None):
        """Generate PDF report"""
        if filename is None:
            filename = f"quiz_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.7*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
        elements = []
        
        # Title
        title = Paragraph("📊 Quiz Performance Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.15*inch))
        
        # Generate timestamp
        timestamp = Paragraph(
            f"<b>Report Generated:</b> {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        )
        elements.append(timestamp)
        elements.append(Spacer(1, 0.25*inch))
        
        # Statistics Section
        stats = self.filter_obj.get_statistics()
        elements.extend(self._build_statistics_section(stats))
        elements.append(Spacer(1, 0.25*inch))
        
        # Detailed Attempts Table
        elements.extend(self._build_attempts_table())
        
        # Build PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        return pdf_buffer, filename
    
    def _build_statistics_section(self, stats):
        """Build statistics summary section"""
        elements = []
        
        elements.append(Paragraph("📈 Summary Statistics", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.15*inch))
        
        stats_data = [
            ['<b>Metric</b>', '<b>Value</b>'],
            ['Total Attempts', str(stats['total_attempts'])],
            ['Completed Attempts', str(stats['completed_attempts'])],
            ['Unique Students', str(stats['unique_students'])],
            ['Total Quizzes', str(stats['total_quizzes'])],
            ['Average Score', f"{stats['avg_score']} pts"],
            ['Average Percentage', f"{stats['avg_percentage']}%" if stats['avg_percentage'] else 'N/A'],
            ['Highest Score', str(stats['max_score']) if stats['max_score'] else 'N/A'],
            ['Lowest Score', str(stats['min_score']) if stats['min_score'] else 'N/A'],
        ]
        
        stats_table = Table(stats_data, colWidths=[3.5*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 14),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9ff')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9ff')]),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(stats_table)
        return elements
    
    def _build_attempts_table(self):
        """Build detailed attempts table with proper formatting"""
        elements = []
        
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("📋 Detailed Attempt Records", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.15*inch))
        
        attempts = self.filter_obj.get_attempts()
        
        # Create table data using Paragraph objects for proper rendering
        header = [
            Paragraph('<b>Quiz Title</b>', self.styles['Normal']),
            Paragraph('<b>Student Name</b>', self.styles['Normal']),
            Paragraph('<b>Score</b>', self.styles['Normal']),
            Paragraph('<b>Percentage</b>', self.styles['Normal']),
            Paragraph('<b>Completed Date</b>', self.styles['Normal']),
        ]
        
        table_data = [header]
        
        for attempt in attempts:
            percentage = round((attempt.score / attempt.total_points * 100), 2) if attempt.total_points else 0
            
            # Get student name - fallback to username if first/last names are empty
            student_name = attempt.student.get_full_name().strip() if attempt.student.get_full_name() else attempt.student.username
            if not student_name or student_name.isspace():
                student_name = attempt.student.username
            
            row = [
                Paragraph(str(attempt.quiz.title)[:30], self.styles['Normal']),
                Paragraph(str(student_name)[:35], self.styles['Normal']),
                Paragraph(str(f"{attempt.score}/{attempt.total_points}"), self.styles['Normal']),
                Paragraph(str(f"{percentage}%"), self.styles['Normal']),
                Paragraph(str(attempt.completed_at.strftime('%d-%m-%Y')) if attempt.completed_at else 'N/A', self.styles['Normal']),
            ]
            table_data.append(row)
        
        if len(table_data) > 1:
            attempts_table = Table(table_data, colWidths=[1.5*inch, 2.2*inch, 0.9*inch, 1*inch, 1.4*inch])
            attempts_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(attempts_table)
            
            # Add summary at bottom
            elements.append(Spacer(1, 0.15*inch))
            summary_text = f"<i>Total Records: <b>{attempts.count()}</b></i>"
            elements.append(Paragraph(summary_text, self.styles['Normal']))
        else:
            elements.append(Paragraph("<i>No data available for the selected filters.</i>", self.styles['Normal']))
        
        return elements


class QuizAnalytics:
    """Analyze quiz performance and generate insights"""
    
    @staticmethod
    def get_performance_by_question(quiz_id):
        """Get performance metrics for each question in a quiz"""
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.questions.all()
        
        performance_data = []
        
        for question in questions:
            attempts = QuizAttempt.objects.filter(
                quiz=quiz,
                completed_at__isnull=False
            )
            
            correct_count = 0
            for attempt in attempts:
                student_answer = attempt.answers.get(str(question.id))
                if student_answer == question.correct_answer:
                    correct_count += 1
            
            total_attempts = attempts.count()
            success_rate = (correct_count / total_attempts * 100) if total_attempts > 0 else 0
            
            performance_data.append({
                'question_id': question.id,
                'question_text': question.text[:50],
                'correct_answers': correct_count,
                'total_attempts': total_attempts,
                'success_rate': round(success_rate, 2),
                'difficulty': 'Easy' if success_rate > 80 else 'Medium' if success_rate > 50 else 'Hard'
            })
        
        return performance_data
    
    @staticmethod
    def get_student_progress(student_id, quiz_ids=None):
        """Get student progress across quizzes"""
        query = QuizAttempt.objects.filter(
            student_id=student_id,
            completed_at__isnull=False
        ).select_related('quiz').order_by('completed_at')
        
        if quiz_ids:
            query = query.filter(quiz_id__in=quiz_ids)
        
        progress_data = []
        for attempt in query:
            percentage = (attempt.score / attempt.total_points * 100) if attempt.total_points else 0
            progress_data.append({
                'quiz_title': attempt.quiz.title,
                'score': attempt.score,
                'total': attempt.total_points,
                'percentage': round(percentage, 2),
                'completed_at': attempt.completed_at,
                'time_taken_minutes': int((attempt.completed_at - attempt.started_at).total_seconds() / 60)
            })
        
        return progress_data
