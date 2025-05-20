import random

class SuggestionEngine:
    def __init__(self):
        self.suggestions = {
            "positive": [
                "Excellent! Channel this positive energy into a creative or challenging task.",
                "Great to hear! Consider collaborating with your team or mentoring someone."
            ],
            "neutral": [
                "A good state for focused work. Tackle your to-do list or routine tasks.",
                "Neutral mood. This might be a good time for planning or organizing."
            ],
            "negative": [
                "I'm sorry you're feeling this way. Consider taking a short break or stretching.",
                "If you're stressed, perhaps switch to a less demanding task for a while."
            ],
            "unknown": ["Mood not determined. Please provide input about how you're feeling."]
        }

    def get_suggestion(self, emotion_label):
        if emotion_label in self.suggestions:
            return random.choice(self.suggestions[emotion_label])
        return "No specific suggestion available for this mood."