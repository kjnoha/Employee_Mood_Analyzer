from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TextEmotionAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_emotion(self, text_input):
        if not text_input or not isinstance(text_input, str):
            return "unknown", 0.0

        vs = self.analyzer.polarity_scores(text_input)
        score = vs['compound']

        if score >= 0.05:
            label = "positive"
        elif score <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        return label, score