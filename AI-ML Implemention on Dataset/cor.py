import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming 'df' is your DataFrame
df = pd.read_csv('final.csv')

# Specify the columns for which you want to compute the correlation matrix
selected_columns = ['registered', 'viewed', 'certified','chapter','incomplete','complete']

# Create a DataFrame containing only the selected columns
selected_df = df[selected_columns]

# Calculate the correlation matrix
correlation_matrix = selected_df.corr()

# Print or visualize the correlation matrix
print(correlation_matrix)
