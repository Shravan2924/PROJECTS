import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

# Load your dataset
df = pd.read_csv('ST.csv')

# Text preprocessing function
def preprocess_text(text):
    text = re.sub(r'http\S+', '', str(text))  # Remove URLs
    text = re.sub(r'@\w+|\#', '', str(text))   # Remove mentions and hashtags
    text = text.encode('ascii', 'ignore').decode('ascii')  # Remove emojis
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]  # Remove stopwords
    cleaned_text = ' '.join(tokens)  # Join tokens
    return cleaned_text

# Apply text preprocessing
df['cleaned_text'] = df['text'].apply(preprocess_text)

# Sentiment analysis using VADER
sid = SentimentIntensityAnalyzer()
df['sentiment_score'] = df['text'].apply(lambda x: sid.polarity_scores(str(x))['compound'])

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['cleaned_text'])

# Latent Dirichlet Allocation (LDA) for topic modeling
lda_model = LatentDirichletAllocation(n_components=2, random_state=42)
lda_matrix = lda_model.fit_transform(tfidf_matrix)

# Add sentiment score and LDA topic features to dataframe
df['topic_1_prob'] = lda_matrix[:, 0]
df['topic_2_prob'] = lda_matrix[:, 1]

# Display the dataframe with engineered features
print(df)
