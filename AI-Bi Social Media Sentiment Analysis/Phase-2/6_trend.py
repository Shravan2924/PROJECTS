import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Load your dataset
data = pd.read_csv('ST.csv')

# Convert the timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d-%m-%Y %H:%M')

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
data['Sentiment_score'] = data['Text'].apply(get_sentiment_score)

# Classify sentiment into categories
data['Sentiment'] = data['Sentiment_score'].apply(classify_sentiment)

# Define the time window for trend analysis (e.g., daily, weekly)
time_window = 'D'  # 'D' for daily, 'W' for weekly, 'M' for monthly, etc.

# Aggregate sentiment scores within each time window
data.set_index('Timestamp', inplace=True)
sentiment_trend = data['Sentiment_score'].resample(time_window).mean().fillna(0)

# Separate positive and negative sentiment scores
positive_sentiment = sentiment_trend[sentiment_trend > 0]
negative_sentiment = sentiment_trend[sentiment_trend < 0]

# Plot the trend in sentiment scores over time
plt.figure(figsize=(10, 6))
plt.plot(sentiment_trend.index, sentiment_trend.values, color='gray', label='Overall Sentiment')
plt.scatter(positive_sentiment.index, positive_sentiment.values, color='green', label='Positive Sentiment')
plt.scatter(negative_sentiment.index, negative_sentiment.values, color='red', label='Negative Sentiment')
plt.title('Sentiment Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Average Sentiment Score')
plt.legend()
plt.grid(True)
plt.savefig('sentiment_trend.png')  # Save the plot as an image
plt.show()

# Write the updated dataset with sentiment scores and categories to a new CSV file
data.reset_index(inplace=True)
data.to_csv('sentiment_analysis_results.csv', index=False)

print("Sentiment analysis results saved to sentiment_analysis_results.csv")
print("Sentiment trend plot saved to sentiment_trend.png")
