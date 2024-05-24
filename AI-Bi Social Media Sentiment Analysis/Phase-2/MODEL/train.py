import pandas as pd
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load CSV data
df = pd.read_csv('ST.csv')  # Replace 'data.csv' with your CSV file path
text_data = df['text']

# Initialize NLTK stopwords
stop_words = set(stopwords.words('english'))

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# 1. Preprocessing
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())
    # Remove punctuation and stopwords
    tokens = [word for word in tokens if word not in string.punctuation and word not in stop_words]
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

# Preprocess text data
df['preprocessed_text'] = df['text'].apply(preprocess_text)

# 2. Sentiment Analysis using VADER
def get_sentiment_label(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df['sentiment_score'] = df['text'].apply(lambda text: sia.polarity_scores(text)['compound'])
df['sentiment_label'] = df['sentiment_score'].apply(get_sentiment_label)

# Save the updated DataFrame to a new CSV file
df.to_csv('data_with_sentiment.csv', index=False)

print("CSV file with sentiment labels saved successfully.")
