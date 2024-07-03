class SentimentAnalysis:
    @staticmethod
    def analyze(text):
        positive_words = [
            'good', 'great', 'excellent', 'fantastic', 'wonderful', 
            'amazing', 'awesome', 'love', 'tasty', 'delicious', 'flavorful'
        ]
        negative_words = [
            'bad', 'terrible', 'awful', 'poor', 'worst', 'disappointing', 
            'hate', 'horrible', 'not tasty', 'bland', 'not good', 'bad taste', 
            'not worthy', 'not great', 'poor taste', 'not recommend', 'worse', 'subpar',
            'not delicious', 'unappetizing', 'inedible'
        ]

        sentiments = {
            'positive': [],
            'negative': []
        }

        text = text.lower()
        for word in positive_words:
            if word in text:
                sentiments['positive'].append(word)
        for word in negative_words:
            if word in text:
                sentiments['negative'].append(word)

        if len(sentiments['positive']) > len(sentiments['negative']):
            return 'positive', list(set(sentiments['positive']))
        elif len(sentiments['negative']) > len(sentiments['positive']):
            return 'negative', list(set(sentiments['negative']))
        else:
            return 'neutral', []
