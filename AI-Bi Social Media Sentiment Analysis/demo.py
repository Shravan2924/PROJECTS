import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the dataset
df = pd.read_csv('ST.csv')

# Explore the data
print("Initial data exploration:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())
print("\nBasic statistics:")
print(df.describe())

# Count missing values for each column
missing_count = df.isnull().sum()

# Display the count of missing values
print("Missing values count per column:")
print(missing_count)

# Display the missing values in a DataFrame
missing_info = pd.DataFrame({
    'Column': df.columns,
    'Missing Values': missing_count,
    'Percentage Missing': (missing_count / len(df)) * 100
})

# Display the DataFrame with missing values information
print("Missing values information:")
print(missing_info)