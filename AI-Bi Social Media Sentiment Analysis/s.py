import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load your dataset
data = pd.read_csv('ST.csv')

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to classify sentiment into positive, negative, or neutral
def classify_sentiment(score):
    if score > 0.05:
        return 'Positive'
    elif score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Function to get sentiment score for each text
def get_sentiment_score(text):
    sentiment = sia.polarity_scores(text)['compound']
    return sentiment

# Apply the sentiment analysis function to each text in the dataset
data['sentiment_score'] = data['Text'].apply(get_sentiment_score)

# Classify sentiment into categories
data['sentiment'] = data['sentiment_score'].apply(classify_sentiment)

# Write the updated dataset with sentiment scores and categories to a new CSV file
data.to_csv('sentiment_analysis_results.csv', index=False)

print("Sentiment analysis results saved to sentiment_analysis_results.csv")
