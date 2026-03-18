"""
Productivity Score Calculator & Music Recommender
Unique features that differentiate Zidio Task Optimizer.
"""
import random


class ProductivityScorer:
    """Computes an AI Productivity Readiness Score (0–100) from mood data."""

    # Weight factors for the composite score
    WEIGHTS = {
        'current_mood': 0.45,
        'streak_bonus': 0.20,
        'trend_direction': 0.20,
        'consistency': 0.15,
    }

    MOOD_BASE_SCORES = {
        'happy': 90, 'motivated': 95, 'confident': 88,
        'calm': 70, 'tired': 35, 'stressed': 30,
        'frustrated': 25, 'anxious': 28, 'sad': 20,
        'angry': 15, 'unknown': 50,
    }

    @staticmethod
    def compute(current_emotion, recent_scores):
        """
        Compute productivity readiness (0-100).
        Args:
            current_emotion: str — latest detected emotion
            recent_scores: list of float — last N compound scores (newest last)
        """
        # 1. Current mood base
        mood_base = ProductivityScorer.MOOD_BASE_SCORES.get(current_emotion, 50)

        # 2. Positive streak bonus
        streak = 0
        for s in reversed(recent_scores):
            if s >= 0.05:
                streak += 1
            else:
                break
        streak_score = min(streak * 15, 100)  # cap at 100

        # 3. Trend direction (are scores improving?)
        if len(recent_scores) >= 2:
            recent_half = recent_scores[len(recent_scores)//2:]
            older_half = recent_scores[:len(recent_scores)//2]
            avg_recent = sum(recent_half) / len(recent_half) if recent_half else 0
            avg_older = sum(older_half) / len(older_half) if older_half else 0
            trend = (avg_recent - avg_older + 1) / 2 * 100  # normalize to 0-100
            trend = max(0, min(100, trend))
        else:
            trend = 50

        # 4. Consistency (low variance = high consistency)
        if len(recent_scores) >= 3:
            mean = sum(recent_scores) / len(recent_scores)
            variance = sum((s - mean) ** 2 for s in recent_scores) / len(recent_scores)
            consistency = max(0, 100 - variance * 200)  # scale
        else:
            consistency = 50

        w = ProductivityScorer.WEIGHTS
        composite = (
            w['current_mood'] * mood_base +
            w['streak_bonus'] * streak_score +
            w['trend_direction'] * trend +
            w['consistency'] * consistency
        )

        return round(max(0, min(100, composite)))

    @staticmethod
    def get_grade(score):
        if score >= 85:
            return {'grade': 'A+', 'label': 'Peak Performance', 'color': '#10b981'}
        elif score >= 70:
            return {'grade': 'A', 'label': 'High Readiness', 'color': '#34d399'}
        elif score >= 55:
            return {'grade': 'B', 'label': 'Moderate', 'color': '#f59e0b'}
        elif score >= 40:
            return {'grade': 'C', 'label': 'Low Energy', 'color': '#f97316'}
        else:
            return {'grade': 'D', 'label': 'Rest Recommended', 'color': '#ef4444'}


class MoodMusicRecommender:
    """Suggests playlists/activities based on detected mood."""

    PLAYLISTS = {
        'happy': {
            'genre': 'Upbeat Pop / Indie',
            'vibe': 'Keep the energy flowing',
            'tracks': [
                '🎵 "Walking on Sunshine" — Katrina & The Waves',
                '🎵 "Happy" — Pharrell Williams',
                '🎵 "Best Day of My Life" — American Authors',
                '🎵 "On Top of the World" — Imagine Dragons',
            ],
            'activity': '🎯 Perfect for brainstorming or creative sprints',
        },
        'motivated': {
            'genre': 'Epic / Workout',
            'vibe': 'Channel the drive',
            'tracks': [
                '🎵 "Lose Yourself" — Eminem',
                '🎵 "Eye of the Tiger" — Survivor',
                '🎵 "Stronger" — Kanye West',
                '🎵 "Warriors" — Imagine Dragons',
            ],
            'activity': '💪 Attack your hardest task right now',
        },
        'confident': {
            'genre': 'Power Pop / Hip-Hop',
            'vibe': 'Own the room',
            'tracks': [
                '🎵 "Confident" — Demi Lovato',
                '🎵 "Run the World" — Beyoncé',
                '🎵 "Can\'t Hold Us" — Macklemore',
                '🎵 "Unstoppable" — Sia',
            ],
            'activity': '🎤 Great time for presentations or pitches',
        },
        'calm': {
            'genre': 'Lo-fi / Ambient',
            'vibe': 'Steady focus',
            'tracks': [
                '🎵 "Weightless" — Marconi Union',
                '🎵 "Clair de Lune" — Debussy',
                '🎵 "Intro" — The xx',
                '🎵 "Sunset Lover" — Petit Biscuit',
            ],
            'activity': '📚 Ideal for deep reading or detailed work',
        },
        'stressed': {
            'genre': 'Nature Sounds / Meditation',
            'vibe': 'Decompress',
            'tracks': [
                '🎵 "Spa Music — Relaxing Piano"',
                '🎵 "Rain Sounds — 1 Hour"',
                '🎵 "Breathe Me" — Sia',
                '🎵 "Nuvole Bianche" — Ludovico Einaudi',
            ],
            'activity': '🧘 Take 5 min to breathe, then tackle one small task',
        },
        'frustrated': {
            'genre': 'Rock / Alternative',
            'vibe': 'Let it out safely',
            'tracks': [
                '🎵 "In the End" — Linkin Park',
                '🎵 "Break Stuff" — Limp Bizkit',
                '🎵 "Killing in the Name" — RATM',
                '🎵 "Smells Like Teen Spirit" — Nirvana',
            ],
            'activity': '🚶 Walk it off, then switch to a different task',
        },
        'anxious': {
            'genre': 'Acoustic / Soft Indie',
            'vibe': 'Ground yourself',
            'tracks': [
                '🎵 "Put Your Records On" — Corinne Bailey Rae',
                '🎵 "Yellow" — Coldplay',
                '🎵 "Better Together" — Jack Johnson',
                '🎵 "Here Comes the Sun" — Beatles',
            ],
            'activity': '📝 Write a quick worry list, then choose 1 action',
        },
        'sad': {
            'genre': 'Soft / Acoustic Comfort',
            'vibe': 'Be gentle with yourself',
            'tracks': [
                '🎵 "Fix You" — Coldplay',
                '🎵 "Lean on Me" — Bill Withers',
                '🎵 "You\'ve Got a Friend" — Carole King',
                '🎵 "River Flows in You" — Yiruma',
            ],
            'activity': '💬 Reach out to someone you trust for a quick chat',
        },
        'angry': {
            'genre': 'Heavy / Cathartic',
            'vibe': 'Release safely',
            'tracks': [
                '🎵 "Given Up" — Linkin Park',
                '🎵 "Bodies" — Drowning Pool',
                '🎵 "Down with the Sickness" — Disturbed',
                '🎵 "Chop Suey!" — System of a Down',
            ],
            'activity': '⏸️ Step away completely for 10 min before any decisions',
        },
        'tired': {
            'genre': 'Chill / Lo-fi Hip-Hop',
            'vibe': 'Easy does it',
            'tracks': [
                '🎵 "Lo-fi Study Beats Playlist"',
                '🎵 "Bloom" — The Paper Kites',
                '🎵 "Holocene" — Bon Iver',
                '🎵 "Electric Feel" — MGMT',
            ],
            'activity': '☕ Hydrate, snack, then do light admin tasks',
        },
    }

    @classmethod
    def recommend(cls, emotion):
        emotion = emotion.lower() if emotion else 'calm'
        return cls.PLAYLISTS.get(emotion, cls.PLAYLISTS['calm'])


class MoodStreakTracker:
    """Gamification: track consecutive positive-mood days."""

    @staticmethod
    def compute_streak(emotion_entries):
        """
        Given a list of dicts with 'date' and 'category' (newest first),
        return current positive streak count.
        """
        streak = 0
        seen_dates = set()
        for entry in emotion_entries:
            date = entry.get('date', '')
            cat = entry.get('category', '')
            if date in seen_dates:
                continue
            seen_dates.add(date)
            if cat == 'positive':
                streak += 1
            else:
                break
        return streak

    @staticmethod
    def get_streak_message(streak):
        if streak >= 7:
            return {'emoji': '🔥', 'message': f'{streak}-day streak! You\'re on fire!', 'level': 'legendary'}
        elif streak >= 5:
            return {'emoji': '⚡', 'message': f'{streak}-day streak! Incredible momentum!', 'level': 'epic'}
        elif streak >= 3:
            return {'emoji': '🌟', 'message': f'{streak}-day streak! Keep it up!', 'level': 'great'}
        elif streak >= 1:
            return {'emoji': '✨', 'message': f'{streak}-day positive streak!', 'level': 'good'}
        else:
            return {'emoji': '🌱', 'message': 'Start a new positive streak today!', 'level': 'start'}
