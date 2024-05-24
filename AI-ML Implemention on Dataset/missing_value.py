import pandas as pd

#read Data
df = pd.read_csv('2.csv')


missing_values_per_column = df.isnull().sum()

# Print the DataFrame and the number of missing values per column
print("Original DataFrame:")
print(df)
print("\nNumber of missing values per column:")
print(missing_values_per_column)

