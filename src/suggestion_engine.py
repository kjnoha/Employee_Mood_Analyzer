import random


class SuggestionEngine:
    """Provides mood-based task optimization suggestions with granular
    emotion support and task priority recommendations."""

    def __init__(self):
        self.suggestions = {
            # Granular emotions
            "happy": [
                "You're in a great mood! Tackle that challenging feature or creative task you've been putting off.",
                "Channel this positive energy into a brainstorming session or team collaboration.",
                "Perfect time to mentor a colleague or lead a team discussion.",
                "Use this momentum for code reviews or architectural decisions.",
            ],
            "motivated": [
                "Strike while the iron is hot — tackle your highest-priority task now!",
                "Your drive is high. Take on a complex problem that needs deep focus.",
                "Great energy! Consider starting that side project or learning a new skill.",
                "Channel this motivation into creating documentation or writing tests.",
            ],
            "confident": [
                "Feeling strong! Present your ideas in a meeting or pitch to leadership.",
                "Great time to take ownership of a critical task or deadline.",
                "Use this confidence to have that difficult conversation you've been avoiding.",
            ],
            "calm": [
                "A balanced state — perfect for focused, detail-oriented work.",
                "Good time for planning, organizing your backlog, or writing documentation.",
                "Neutral mood suits routine tasks, code reviews, or bug triage.",
                "Consider catching up on emails, Slack messages, or admin work.",
            ],
            "stressed": [
                "Take a 5-minute breather. Step away, stretch, or do some deep breathing.",
                "Break your current task into smaller, more manageable pieces.",
                "Consider delegating non-critical work and focusing on one thing at a time.",
                "Write down everything on your plate — just listing it out can reduce overwhelm.",
            ],
            "frustrated": [
                "Step away from the problem for 10 minutes — fresh eyes often find the solution.",
                "Try rubber duck debugging: explain the problem out loud or to a colleague.",
                "Switch to a different task temporarily, then come back with a clear head.",
                "Document what's blocking you and ask for help — no shame in that!",
            ],
            "anxious": [
                "Ground yourself: name 5 things you can see, 4 you can touch, 3 you hear.",
                "Focus on what you CAN control. Make a list of your next 3 small actions.",
                "Talk to your manager or a trusted colleague about what's worrying you.",
                "Try a low-stakes, achievable task to build momentum and ease anxiety.",
            ],
            "sad": [
                "Be gentle with yourself. It's okay to have off days.",
                "Connect with a supportive colleague or friend, even just for a quick chat.",
                "Try a task that gives you a sense of accomplishment, however small.",
                "Consider reaching out to your team lead or HR if you need support.",
            ],
            "angry": [
                "Pause before acting. Take a walk or step outside for a few minutes.",
                "Write down what triggered your frustration — it can help process the emotion.",
                "Avoid sending messages or making decisions until you've cooled down.",
                "Channel the energy into physical activity or a competitive task.",
            ],
            "tired": [
                "Listen to your body. If possible, take a 15-minute power nap or rest.",
                "Switch to less demanding tasks — organize files, reply to emails, or plan.",
                "Hydrate, have a healthy snack, and take a short walk.",
                "Avoid starting new complex tasks; finish existing small ones instead.",
            ],
            "unknown": [
                "I couldn't quite read your mood. Try describing how you're feeling in more detail.",
            ],
        }

        self.task_priorities = {
            "happy": {"priority": "high", "focus": "creative & challenging", "time_blocks": "90 min deep work"},
            "motivated": {"priority": "high", "focus": "complex & strategic", "time_blocks": "90 min deep work"},
            "confident": {"priority": "high", "focus": "leadership & presentations", "time_blocks": "60 min focused"},
            "calm": {"priority": "medium", "focus": "routine & planning", "time_blocks": "45 min blocks"},
            "stressed": {"priority": "low", "focus": "break tasks into small pieces", "time_blocks": "25 min pomodoro"},
            "frustrated": {"priority": "low", "focus": "switch context, then return", "time_blocks": "25 min pomodoro"},
            "anxious": {"priority": "low", "focus": "small achievable wins", "time_blocks": "15 min sprints"},
            "sad": {"priority": "low", "focus": "gentle, low-pressure tasks", "time_blocks": "20 min with breaks"},
            "angry": {"priority": "low", "focus": "physical or mechanical tasks", "time_blocks": "15 min then pause"},
            "tired": {"priority": "low", "focus": "admin & light tasks", "time_blocks": "25 min then break"},
            "unknown": {"priority": "medium", "focus": "general tasks", "time_blocks": "30 min blocks"},
        }

    def get_suggestion(self, emotion_label):
        """Return a random suggestion for the given emotion."""
        emotion_label = emotion_label.lower() if emotion_label else "unknown"
        if emotion_label in self.suggestions:
            return random.choice(self.suggestions[emotion_label])
        return "No specific suggestion available for this mood. Focus on what feels manageable."

    def get_task_priority(self, emotion_label):
        """Return task priority recommendation for the given emotion."""
        emotion_label = emotion_label.lower() if emotion_label else "unknown"
        return self.task_priorities.get(emotion_label, self.task_priorities["unknown"])

    def get_all_suggestions(self, emotion_label):
        """Return all suggestions for an emotion (for display in UI)."""
        emotion_label = emotion_label.lower() if emotion_label else "unknown"
        return self.suggestions.get(emotion_label, self.suggestions["unknown"])