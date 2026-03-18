from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


class TextEmotionAnalyzer:
    """Analyzes text to detect employee emotions using VADER sentiment
    analysis combined with robust keyword/phrase detection for 10 granular
    emotion categories."""

    # Multi-word phrases checked FIRST (order matters — more specific first)
    EMOTION_PHRASES = {
        "stressed": [
            "stressed out", "under pressure", "too much work", "can't keep up",
            "burning out", "burnt out", "burned out", "work overload",
            "so much to do", "no time", "tight deadline", "running out of time",
            "losing my mind", "pulling my hair", "at my limit",
        ],
        "frustrated": [
            "can't figure", "not working", "keeps breaking", "stuck on",
            "doesn't make sense", "going nowhere", "wasting time",
            "hit a wall", "dead end", "going in circles", "so annoying",
            "fed up", "sick of", "had enough", "doesn't work",
        ],
        "anxious": [
            "freaking out", "can't stop thinking", "what if", "scared about",
            "worried about", "nervous about", "afraid of", "panic attack",
            "feel uneasy", "knot in my stomach", "on edge", "butterflies",
        ],
        "motivated": [
            "can't wait", "fired up", "let's go", "bring it on", "pumped up",
            "ready to go", "looking forward", "let's do this", "give it my all",
            "so excited", "raring to go", "on a roll",
        ],
        "tired": [
            "worn out", "no energy", "need sleep", "barely awake",
            "running on empty", "dead tired", "half asleep", "so drained",
            "need a nap", "can barely keep", "eyes closing",
        ],
        "confident": [
            "nailed it", "crushed it", "killed it", "on top of",
            "feeling strong", "i got this", "piece of cake", "smashed it",
            "knocked it out", "proud of myself", "feeling great about",
        ],
        "sad": [
            "feeling down", "not myself", "lost interest", "don't care anymore",
            "feeling empty", "miss the old", "feel like crying", "heartbroken",
            "feel alone", "nobody cares", "can't be bothered",
        ],
        "angry": [
            "pissed off", "so mad", "makes me furious", "drives me crazy",
            "want to scream", "blood boiling", "had it", "last straw",
            "absolutely unacceptable", "beyond angry",
        ],
    }

    # Single keywords as fallback
    EMOTION_KEYWORDS = {
        "stressed":    ["stress", "overwhelm", "pressure", "deadline", "overwork",
                        "burnout", "exhausted", "overloaded", "swamped", "hectic",
                        "chaos", "meltdown", "crunch"],
        "frustrated":  ["frustrat", "annoy", "irritat", "stuck", "block", "ridiculous",
                        "useless", "pointless", "impossible", "broken", "glitch", "bug"],
        "anxious":     ["anxi", "worr", "nervous", "uneasy", "uncertain", "scared",
                        "afraid", "dread", "panic", "paranoid", "restless", "tense"],
        "sad":         ["sad", "depress", "lonely", "hopeless", "miserable", "unhappy",
                        "heartbr", "grief", "sorrow", "gloomy", "upset", "devastat",
                        "disappoint", "let down", "cry"],
        "angry":       ["angry", "furious", "rage", "mad", "hate", "livid", "irate",
                        "hostile", "resentful", "bitter", "outraged"],
        "happy":       ["happy", "joy", "delight", "cheerful", "wonderful", "fantastic",
                        "amazing", "love", "great", "awesome", "excellent", "thrilled",
                        "elated", "blessed", "glad", "pleased", "ecstatic", "superb",
                        "brilliant", "terrific", "marvelous"],
        "motivated":   ["motivat", "inspir", "excit", "eager", "pump", "passionate",
                        "driven", "determined", "ambitious", "energized", "enthus",
                        "fired", "focused", "productive"],
        "calm":        ["calm", "relax", "peace", "serene", "content", "tranquil",
                        "composed", "settled", "chill", "mellow", "zen", "mindful",
                        "easy", "steady", "balanced"],
        "tired":       ["tired", "fatigue", "sleepy", "exhaust", "drained", "weary",
                        "lethargic", "sluggish", "drowsy", "yawn"],
        "confident":   ["confident", "proud", "accomplish", "achiev", "succeed",
                        "nailed", "crush", "strong", "capable", "empowered", "unstoppable"],
    }

    # Map emotions to broader categories
    EMOTION_CATEGORIES = {
        "stressed": "negative",
        "frustrated": "negative",
        "anxious": "negative",
        "sad": "negative",
        "angry": "negative",
        "tired": "negative",
        "happy": "positive",
        "motivated": "positive",
        "confident": "positive",
        "calm": "neutral",
    }

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def _detect_phrase_emotion(self, text):
        """Check for multi-word phrases first (highest accuracy)."""
        text_lower = text.lower()
        for emotion, phrases in self.EMOTION_PHRASES.items():
            for phrase in phrases:
                if phrase in text_lower:
                    return emotion
        return None

    def _detect_keyword_emotion(self, text):
        """Fallback: detect from single keywords using substring match."""
        text_lower = text.lower()
        # Split into words for more accurate matching
        words = re.findall(r'[a-z]+', text_lower)
        word_text = ' '.join(words)

        scores = {}  # emotion -> match count
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            count = 0
            for keyword in keywords:
                if keyword in word_text:
                    count += 1
            if count > 0:
                scores[emotion] = count

        if scores:
            # Return the emotion with the most keyword hits
            return max(scores, key=scores.get)
        return None

    def _check_negation(self, text, emotion):
        """Check if the detected emotion is negated (e.g., 'not happy')."""
        text_lower = text.lower()
        negation_patterns = [
            r"(?:not|don'?t|doesn'?t|isn'?t|wasn'?t|aren'?t|never|no longer|hardly|barely)\s+(?:\w+\s+){0,2}",
        ]
        keywords = self.EMOTION_KEYWORDS.get(emotion, [])
        for kw in keywords:
            for pattern in negation_patterns:
                if re.search(pattern + re.escape(kw), text_lower):
                    # Emotion is negated — flip category
                    cat = self.EMOTION_CATEGORIES.get(emotion, "neutral")
                    if cat == "positive":
                        return "sad"  # "not happy" → sad
                    elif cat == "negative":
                        return "calm"  # "not stressed" → calm
        return emotion  # no negation detected

    def get_emotion(self, text_input):
        """Analyze text and return (emotion_label, compound_score, category).

        Detection strategy (in priority order):
          1. Multi-word phrase matching (highest precision)
          2. Single keyword matching with frequency scoring
          3. Negation-aware correction
          4. VADER compound score fallback
        """
        if not text_input or not isinstance(text_input, str):
            return "unknown", 0.0, "unknown"

        text_input = text_input.strip()
        if len(text_input) < 2:
            return "unknown", 0.0, "unknown"

        vs = self.analyzer.polarity_scores(text_input)
        score = vs['compound']

        # 1. Phrase-based detection
        emotion = self._detect_phrase_emotion(text_input)

        # 2. Keyword-based detection
        if not emotion:
            emotion = self._detect_keyword_emotion(text_input)

        # 3. Negation check
        if emotion:
            emotion = self._check_negation(text_input, emotion)
            category = self.EMOTION_CATEGORIES.get(emotion, "neutral")

            # Cross-validate: if keyword says positive but VADER is very negative,
            # trust VADER for the category
            if category == "positive" and score <= -0.3:
                emotion = "sad" if score <= -0.5 else "stressed"
                category = "negative"
            elif category == "negative" and score >= 0.3:
                emotion = "happy" if score >= 0.5 else "calm"
                category = "positive" if score >= 0.5 else "neutral"

            return emotion, score, category

        # 4. VADER score fallback with fine-grained thresholds
        if score >= 0.6:
            return "happy", score, "positive"
        elif score >= 0.3:
            return "motivated", score, "positive"
        elif score >= 0.05:
            return "calm", score, "positive"
        elif score <= -0.6:
            return "sad", score, "negative"
        elif score <= -0.3:
            return "stressed", score, "negative"
        elif score <= -0.05:
            return "anxious", score, "negative"
        else:
            return "calm", score, "neutral"

    def get_sentiment_details(self, text_input):
        """Return full VADER breakdown: positive, negative, neutral, compound."""
        if not text_input or not isinstance(text_input, str):
            return {"pos": 0, "neg": 0, "neu": 0, "compound": 0}
        return self.analyzer.polarity_scores(text_input)