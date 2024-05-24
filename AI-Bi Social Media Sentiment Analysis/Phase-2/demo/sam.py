import pandas as pd
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load CSV data
df = pd.read_csv('ST.csv')  # Replace 'data.csv' with your CSV file path
text_data = df['Text']

# Initialize NLTK stopwords
stop_words = set(stopwords.words('english'))

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
df['preprocessed_text'] = df['Text'].apply(preprocess_text)

# 2. Feature Extraction
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # Adjust max_features as needed
X = tfidf_vectorizer.fit_transform(df['preprocessed_text'])
y = df['Sentiment']

# 3. Model Training
naive_bayes = MultinomialNB()
naive_bayes.fit(X, y)

# Example prediction
user_text = "Good Morning"
preprocessed_user_text = preprocess_text(user_text)
text_features = tfidf_vectorizer.transform([preprocessed_user_text])
sentiment = naive_bayes.predict(text_features)[0]
print("Predicted Sentiment:", "Positive" if sentiment == 1 else "Negative")
