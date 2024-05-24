import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Load your dataset
data = pd.read_csv('ST.csv')

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to get sentiment score for each text
def get_sentiment_score(Text):
    sentiment = sia.polarity_scores(Text)['compound']
    return sentiment

# Apply the sentiment analysis function to each text in the dataset
data['sentiment_score'] = data['Text'].apply(get_sentiment_score)

# Write the updated dataset with sentiment scores to a new CSV file
data.to_csv('sentiment_scores_dataset.csv', index=False)

print("Sentiment scores appended to the dataset and saved to sentiment_scores_dataset.csv")
