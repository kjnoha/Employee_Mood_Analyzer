"""
Zidio Task Optimizer — Web Application
A mood-driven task optimization dashboard for teams.
"""
import os
import sys
import json

# Ensure src is on the path
project_root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir_path = os.path.join(project_root_dir, "src")
if src_dir_path not in sys.path:
    sys.path.insert(0, src_dir_path)

from flask import Flask, render_template, request, jsonify

from src.emotion_analyzer import TextEmotionAnalyzer
from src.suggestion_engine import SuggestionEngine
from src.data_logger import DataLogger
from src.extras import ProductivityScorer, MoodMusicRecommender, MoodStreakTracker


# ── NLTK bootstrap ──────────────────────────────────────────────────────
def _ensure_nltk():
    try:
        from nltk.downloader import Downloader
        if not Downloader().is_installed('vader_lexicon'):
            import nltk
            nltk.download('vader_lexicon', quiet=True)
    except Exception:
        pass

_ensure_nltk()


# ── Flask app ───────────────────────────────────────────────────────────
app = Flask(__name__,
            template_folder=os.path.join(project_root_dir, 'templates'),
            static_folder=os.path.join(project_root_dir, 'static'))

analyzer = TextEmotionAnalyzer()
suggester = SuggestionEngine()
logger = DataLogger()


# ── Emotion metadata (colours & icons for the UI) ──────────────────────
EMOTION_META = {
    "happy":      {"color": "#10b981", "icon": "😊"},
    "motivated":  {"color": "#f59e0b", "icon": "🔥"},
    "confident":  {"color": "#8b5cf6", "icon": "💪"},
    "calm":       {"color": "#06b6d4", "icon": "😌"},
    "stressed":   {"color": "#ef4444", "icon": "😰"},
    "frustrated": {"color": "#f97316", "icon": "😤"},
    "anxious":    {"color": "#a855f7", "icon": "😟"},
    "sad":        {"color": "#3b82f6", "icon": "😢"},
    "angry":      {"color": "#dc2626", "icon": "😡"},
    "tired":      {"color": "#6b7280", "icon": "😴"},
    "unknown":    {"color": "#9ca3af", "icon": "❓"},
    "positive":   {"color": "#10b981", "icon": "😊"},
    "negative":   {"color": "#ef4444", "icon": "😢"},
    "neutral":    {"color": "#06b6d4", "icon": "😌"},
}


def _get_team_mood_category():
    """Determine the dominant mood category across all entries."""
    dist = logger.get_emotion_distribution()
    if not dist:
        return "mixed"
    from src.emotion_analyzer import TextEmotionAnalyzer as TEA
    cat_counts = {"positive": 0, "negative": 0, "neutral": 0}
    for em, count in dist.items():
        cat = TEA.EMOTION_CATEGORIES.get(em, "neutral")
        cat_counts[cat] = cat_counts.get(cat, 0) + count
    dominant = max(cat_counts, key=cat_counts.get)
    return dominant


def _build_entry(row):
    """Build a display-ready dict from a DataFrame row."""
    emotion = row.get('detected_emotion', 'unknown')
    meta = EMOTION_META.get(emotion, EMOTION_META['unknown'])
    return {
        'timestamp': row['timestamp'],
        'employee_id': row['employee_id'],
        'text_input': row['text_input'],
        'emotion': emotion,
        'category': row.get('emotion_category', 'neutral'),
        'score': round(row['emotion_score'], 2),
        'suggestion': row['suggestion_given'],
        'icon': meta['icon'],
        'color': meta['color'],
    }


# ── Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    team_stats = logger.get_team_stats()
    employee_ids = logger.get_all_employee_ids()
    recent_logs = logger.get_logs(limit=15)
    recent_entries = [_build_entry(row) for _, row in recent_logs.iterrows()]
    recent_entries.reverse()  # newest first

    # Productivity score (team-wide)
    all_logs = logger.get_logs()
    all_scores = all_logs['emotion_score'].tolist() if not all_logs.empty else []
    dominant_emotion = team_stats.get('most_common_emotion', 'calm')
    prod_score = ProductivityScorer.compute(dominant_emotion, all_scores[-10:])
    prod_grade = ProductivityScorer.get_grade(prod_score)

    # Streak
    streak_entries = []
    for _, row in recent_logs.iterrows():
        streak_entries.append({
            'date': str(row['timestamp'])[:10],
            'category': row.get('emotion_category', 'neutral'),
        })
    streak_entries.reverse()
    streak_count = MoodStreakTracker.compute_streak(streak_entries)
    streak_info = MoodStreakTracker.get_streak_message(streak_count)

    team_mood_cat = _get_team_mood_category()

    return render_template('dashboard.html',
                           team_stats=team_stats,
                           employee_ids=employee_ids,
                           recent_entries=recent_entries,
                           emotion_meta=EMOTION_META,
                           prod_score=prod_score,
                           prod_grade=prod_grade,
                           streak_info=streak_info,
                           team_mood_category=team_mood_cat)


@app.route('/analyze', methods=['POST'])
def analyze():
    employee_id = request.form.get('employee_id', '').strip()
    text_input = request.form.get('text_input', '').strip()

    if not employee_id or not text_input:
        return jsonify({'error': 'Employee ID and mood text are required.'}), 400

    emotion, score, category = analyzer.get_emotion(text_input)
    suggestion = suggester.get_suggestion(emotion)
    task_priority = suggester.get_task_priority(emotion)
    all_suggestions = suggester.get_all_suggestions(emotion)
    sentiment_details = analyzer.get_sentiment_details(text_input)

    logger.log_entry(employee_id, text_input, emotion, score, suggestion, category)

    meta = EMOTION_META.get(emotion, EMOTION_META['unknown'])

    # Productivity score for this employee
    emp_logs = logger.get_logs(employee_id=employee_id)
    emp_scores = emp_logs['emotion_score'].tolist() if not emp_logs.empty else [score]
    prod_score = ProductivityScorer.compute(emotion, emp_scores[-10:])
    prod_grade = ProductivityScorer.get_grade(prod_score)

    # Music recommendation
    music = MoodMusicRecommender.recommend(emotion)

    # Streak for this employee
    streak_entries = []
    for _, row in emp_logs.iterrows():
        streak_entries.append({
            'date': str(row['timestamp'])[:10],
            'category': row.get('emotion_category', 'neutral'),
        })
    streak_entries.reverse()
    streak_count = MoodStreakTracker.compute_streak(streak_entries)
    streak_info = MoodStreakTracker.get_streak_message(streak_count)

    return jsonify({
        'success': True,
        'result': {
            'emotion': emotion,
            'score': round(score, 4),
            'category': category,
            'suggestion': suggestion,
            'all_suggestions': all_suggestions,
            'task_priority': task_priority,
            'sentiment_details': {
                'positive': round(sentiment_details['pos'] * 100, 1),
                'negative': round(sentiment_details['neg'] * 100, 1),
                'neutral': round(sentiment_details['neu'] * 100, 1),
            },
            'icon': meta['icon'],
            'color': meta['color'],
            'productivity': {
                'score': prod_score,
                'grade': prod_grade['grade'],
                'label': prod_grade['label'],
                'grade_color': prod_grade['color'],
            },
            'music': music,
            'streak': streak_info,
        }
    })


@app.route('/api/trends')
def api_trends():
    employee_id = request.args.get('employee_id', None)
    days = int(request.args.get('days', 30))
    trends = logger.get_mood_trends(employee_id=employee_id, days=days)
    return jsonify(trends)


@app.route('/api/distribution')
def api_distribution():
    employee_id = request.args.get('employee_id', None)
    dist = logger.get_emotion_distribution(employee_id=employee_id)
    labels = list(dist.keys())
    values = list(dist.values())
    colors = [EMOTION_META.get(e, EMOTION_META['unknown'])['color'] for e in labels]
    icons = [EMOTION_META.get(e, EMOTION_META['unknown'])['icon'] for e in labels]
    return jsonify({'labels': labels, 'values': values, 'colors': colors, 'icons': icons})


@app.route('/api/logs')
def api_logs():
    employee_id = request.args.get('employee_id', None)
    logs_df = logger.get_logs(employee_id=employee_id if employee_id else None)
    entries = [_build_entry(row) for _, row in logs_df.iterrows()]
    entries.reverse()
    return jsonify(entries)


@app.route('/api/employees')
def api_employees():
    return jsonify(logger.get_all_employee_ids())


# ── Run ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
