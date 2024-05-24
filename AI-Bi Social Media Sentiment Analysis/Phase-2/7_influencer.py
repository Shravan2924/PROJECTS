import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('ST.csv')

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

# Optionally, you can correlate influence metrics with sentiment scores if available
