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
        
        # Add unique context based on actual performance changes
        performance_trend = "improving" if student_data['recent_avg'] > student_data['avg_percentage'] else "steady"
        if student_data['recent_avg'] < student_data['avg_percentage'] - 5:
            performance_trend = "declining"
        
        prompt = f"""You are an encouraging educational AI coach. Generate ONE SHORT personalized tip (maximum 15 words).

Student: Rank #{student_data['rank']}/{leaderboard_position['total_students']}
Score: {student_data['avg_percentage']}% average, {student_data['recent_avg']}% recent ({performance_trend})
Completed: {student_data['total_quizzes']} quizzes, {student_data['perfect_scores']} perfect
Tier: {student_data['tier']['name']}

Create a VERY SHORT (10-15 words), specific, actionable tip based on their performance trend.

Examples:
- Top performer + improving: "Keep crushing it! Try teaching others to master concepts."
- Mid-rank + steady: "Review wrong answers after each quiz to boost scores."
- Lower rank: "Start with 15-min daily reviews before attempting quizzes."
- Declining: "Take a break, then review basics before next quiz."

NO emojis, NO formatting, NO titles. Just one practical sentence (max 15 words)."""
        
        response = model.generate_content(prompt)
        suggestion = response.text.strip().replace('**', '').replace('🎯', '').replace('*', '')
        # Remove any line breaks and extra spaces
        suggestion = ' '.join(suggestion.split())
        # Truncate if too long
        words = suggestion.split()
        if len(words) > 15:
            suggestion = ' '.join(words[:15]) + '...'
        return suggestion
        
    except Exception as e:
        print(f"AI suggestion error: {e}")
        # Smart fallback based on actual data
        if student_data['avg_percentage'] >= 85:
            return "Excellent work! Try helping classmates to deepen your understanding."
        elif student_data['avg_percentage'] >= 70:
            return "Good progress! Review quiz mistakes to reach the next level."
        elif student_data['recent_avg'] > student_data['avg_percentage']:
            return "You're improving! Keep this momentum with daily practice sessions."
        elif student_data['total_quizzes'] < 3:
            return "Take more quizzes to build confidence and improve scores."
        else:
            return "Focus on mastering one topic at a time for better results."


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
