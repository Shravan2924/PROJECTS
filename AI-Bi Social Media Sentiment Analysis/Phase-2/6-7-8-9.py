import nltk
import pandas as pd
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import os

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

# Aggregate metrics: Total retweets, total likes, and frequency of mentions
influence_metrics = data.groupby('Username').agg({
    'Retweets': 'sum',
    'Likes': 'sum',
    'SR.No': 'count'  # Frequency of mentions
}).rename(columns={'SR.No': 'Mentions'}).reset_index()

# Rank influencers based on aggregated metrics
influence_metrics['Influence_score'] = influence_metrics['Retweets'] + influence_metrics['Likes'] + influence_metrics['Mentions']
influence_metrics.sort_values(by='Influence_score', ascending=False, inplace=True)

# Visualize influence metrics
plt.figure(figsize=(10, 6))
plt.bar(influence_metrics['Username'][:10], influence_metrics['Influence_score'][:10], color='skyblue')
plt.title('Top Influencers by Influence Score')
plt.xlabel('Username')
plt.ylabel('Influence Score')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Convert the timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Extract the year from the timestamp
data['Year'] = data['Timestamp'].dt.year

# Group the data by year and count mentions
mentions_by_year = data.groupby(['Year', 'Username']).size().reset_index(name='Mentions')

# Create a string to store the output for writing to the Notepad file
output_string = ""

# Iterate over each year and append the usernames mentioning the brand to the output string
for year in mentions_by_year['Year'].unique():
    output_string += f"Year: {year}\n"
    subset = mentions_by_year[mentions_by_year['Year'] == year]
    for index, row in subset.iterrows():
        output_string += f"Username: {row['Username']},  {row['Mentions']}\n"
    output_string += "\n"

# Write the output string to a Notepad file
output_file_path = 'brand_mentions_output.txt'
with open(output_file_path, 'w') as file:
    file.write(output_string)

# Print a message indicating the output file has been created
print("Output for usernames mentioning the brand has been saved to brand_mentions_output.txt")

# Plot the increasing number of brand mentions per year
mentions_per_year = mentions_by_year.groupby('Year')['Mentions'].sum()

plt.figure(figsize=(10, 6))
plt.plot(mentions_per_year.index, mentions_per_year.values, marker='o', linestyle='-')
plt.title('Number of Brand Mentions per Year')
plt.xlabel('Year')
plt.ylabel('Number of Mentions')
plt.grid(True)

# Show the plot
plt.show()

# Open the Notepad file
os.system(f'start notepad {output_file_path}')