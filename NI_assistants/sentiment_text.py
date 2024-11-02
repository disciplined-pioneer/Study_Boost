import re
from mtranslate import translate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Функция для анализа тональности
async def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    translated_text = translate(text, 'en', 'ru')  # Перевод текста
    translated_text = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s]', '', translated_text.lower())
    result = analyzer.polarity_scores(translated_text)
    return result['compound']