import pandas as pd

# Assuming data is a dictionary with keys 'complete', representing the column
data = {'complete': [1, 0, 1, 0, 1]}

# Read the CSV
df = pd.read_csv('main.csv')

# Set values in the 'incomplete' column to 1 where corresponding values in the 'complete' column are 0
df['incomplete'] = df['complete'].apply(lambda x: 1 if x == 0 else 0)

# Save the modified DataFrame to a new CSV file
df.to_csv('output_file.csv', index=False)

# Print the DataFrame after the update
print("DataFrame after setting 'incomplete' values to 1 where 'complete' is 0:")
print(df)
