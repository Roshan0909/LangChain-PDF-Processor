"""
Leaderboard utilities for calculating student rankings and generating AI suggestions
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai
from django.db.models import Count, Sum, Avg, Q
from teachers.models import QuizAttempt

load_dotenv()

def get_leaderboard_data():
    """
    Calculate comprehensive leaderboard rankings based on multiple metrics
    """
    from authentication.models import User
    
    students = User.objects.filter(role='student')
    leaderboard = []
    
    for student in students:
        # Get quiz statistics
        attempts = QuizAttempt.objects.filter(
            student=student,
            completed_at__isnull=False
        )
        
        total_quizzes = attempts.count()
        if total_quizzes == 0:
            continue  # Skip students with no quiz attempts
        
        # Calculate metrics
        total_score = sum([attempt.score for attempt in attempts])
        total_possible = sum([attempt.total_points for attempt in attempts])
        
        avg_percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
        
        # Count perfect scores
        perfect_scores = attempts.filter(score=total_possible).count()
        
        # Get recent performance (last 5 quizzes)
        recent_attempts = attempts.order_by('-completed_at')[:5]
        recent_avg = 0
        if recent_attempts.exists():
            recent_score = sum([a.score for a in recent_attempts])
            recent_possible = sum([a.total_points for a in recent_attempts])
            recent_avg = (recent_score / recent_possible * 100) if recent_possible > 0 else 0
        
        # Calculate engagement score (weighted combination)
        engagement_score = (
            avg_percentage * 0.5 +  # 50% weight on average score
            (perfect_scores / total_quizzes * 100) * 0.2 +  # 20% weight on perfect scores
            recent_avg * 0.2 +  # 20% weight on recent performance
            min(total_quizzes * 2, 10)  # 10% weight on participation (capped at 10 points)
        )
        
        leaderboard.append({
            'student': student,
            'total_quizzes': total_quizzes,
            'avg_percentage': round(avg_percentage, 2),
            'total_score': total_score,
            'total_possible': total_possible,
            'perfect_scores': perfect_scores,
            'recent_avg': round(recent_avg, 2),
            'engagement_score': round(engagement_score, 2)
        })
    
    # Sort by engagement score (highest first)
    leaderboard.sort(key=lambda x: x['engagement_score'], reverse=True)
    
    # Add rankings and badges
    for idx, entry in enumerate(leaderboard, 1):
        entry['rank'] = idx
        entry['badge'] = get_rank_badge(idx)
        entry['tier'] = get_tier(entry['engagement_score'])
    
    return leaderboard


def get_rank_badge(rank):
    """Get badge icon and color based on rank"""
    badges = {
        1: {'icon': '👑', 'name': 'Champion', 'color': '#FFD700'},
        2: {'icon': '🥈', 'name': 'Runner-up', 'color': '#C0C0C0'},
        3: {'icon': '🥉', 'name': 'Bronze Star', 'color': '#CD7F32'},
    }
    
    if rank <= 3:
        return badges[rank]
    elif rank <= 10:
        return {'icon': '⭐', 'name': 'Top 10', 'color': '#667eea'}
    else:
        return {'icon': '🎯', 'name': 'Achiever', 'color': '#764ba2'}


def get_tier(engagement_score):
    """Determine tier based on engagement score"""
    if engagement_score >= 90:
        return {'name': 'Diamond', 'color': '#00D9FF', 'icon': '💎'}
    elif engagement_score >= 75:
        return {'name': 'Platinum', 'color': '#E5E4E2', 'icon': '🌟'}
    elif engagement_score >= 60:
        return {'name': 'Gold', 'color': '#FFD700', 'icon': '⚡'}
    elif engagement_score >= 45:
        return {'name': 'Silver', 'color': '#C0C0C0', 'icon': '🔥'}
    else:
        return {'name': 'Bronze', 'color': '#CD7F32', 'icon': '📚'}


def generate_personalized_suggestion(student_data, leaderboard_position):
    """
    Use Gemini AI to generate personalized improvement suggestions
    """
    try:
        genai.configure(api_key=os.getenv('API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = f"""You are an encouraging educational AI coach helping students improve their academic performance.

Student Performance Data:
- Current Rank: #{student_data['rank']} out of {leaderboard_position['total_students']}
- Engagement Score: {student_data['engagement_score']}/100
- Average Quiz Score: {student_data['avg_percentage']}%
- Total Quizzes Completed: {student_data['total_quizzes']}
- Perfect Scores: {student_data['perfect_scores']}
- Recent Performance (last 5 quizzes): {student_data['recent_avg']}%
- Current Tier: {student_data['tier']['name']}

Generate a personalized, motivational suggestion to help this student improve. Keep it:
1. Encouraging and positive (2-3 sentences max)
2. Specific and actionable
3. Focused on one key area for improvement
4. Friendly and conversational

Format:
🎯 **[Catchy Title]**
[Encouraging message with specific actionable advice]

Example styles:
- If performing well: Celebrate success and suggest next challenge
- If average: Encourage consistency and identify growth area
- If struggling: Provide motivation and simple first steps
- If improving: Acknowledge progress and maintain momentum

DO NOT use generic advice. Make it personal based on their actual data.
Keep the total response under 100 words."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        # Fallback suggestions if AI fails
        if student_data['avg_percentage'] >= 80:
            return "🎯 **Outstanding Work!**\nYou're already excelling! Challenge yourself with tougher topics and help mentor classmates to reinforce your knowledge even further."
        elif student_data['avg_percentage'] >= 60:
            return "🎯 **You're on Track!**\nGreat progress! Focus on reviewing quiz mistakes and practicing weak areas. Consistency is key to reaching the next tier!"
        else:
            return "🎯 **Keep Building Momentum!**\nEvery expert was once a beginner. Start with smaller study sessions daily, and review material before quizzes. You've got this!"


def generate_overall_insights(leaderboard_data):
    """
    Generate AI-powered insights about the overall leaderboard trends
    """
    try:
        if not leaderboard_data:
            return "No student data available yet."
        
        genai.configure(api_key=os.getenv('API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Calculate statistics
        avg_score = sum([d['avg_percentage'] for d in leaderboard_data]) / len(leaderboard_data)
        top_performer = leaderboard_data[0] if leaderboard_data else None
        total_students = len(leaderboard_data)
        
        prompt = f"""You are an educational analytics AI providing insights about class performance.

Class Statistics:
- Total Active Students: {total_students}
- Average Class Score: {avg_score:.2f}%
- Top Performer Score: {top_performer['avg_percentage']:.2f}% (Rank #1)
- Score Range: {leaderboard_data[-1]['avg_percentage']:.2f}% to {top_performer['avg_percentage']:.2f}%

Generate a brief, insightful observation about the class performance (2-3 sentences). 
Make it encouraging but honest. Highlight positive trends and areas of strength.
Keep it under 80 words and friendly in tone.

Format: Plain text, no emojis, professional but warm."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        return "The class is showing great engagement with the learning materials. Keep up the excellent work!"
