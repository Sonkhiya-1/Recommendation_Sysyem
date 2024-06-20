from textblob import TextBlob

class SentimentAnalysis:
    @staticmethod
    def analyze(text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return 'positive'
        elif polarity < 0:
            return 'negative'
        else:
            return 'neutral'
