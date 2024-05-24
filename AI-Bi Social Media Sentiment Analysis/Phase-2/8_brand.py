import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the dataset containing brand mentions
data = pd.read_csv('ST.csv')

# Extract the brand name mentioned by the user from the first row of the dataset
brand_name = "YourBrand"  # Replace "YourBrand" with the actual brand name

# Convert the timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Extract the year from the timestamp
data['Year'] = data['Timestamp'].dt.year

# Group the data by year and count mentions
mentions_by_year = data.groupby(['Year', 'Username']).size().reset_index(name='Mentions')

# Create a string to store the output for writing to the Notepad file
output_string = f"Brand: {brand_name}\n\n"

# Iterate over each year and append the usernames mentioning the brand to the output string
for year in mentions_by_year['Year'].unique():
    output_string += f"Year: {year}\n"
    subset = mentions_by_year[mentions_by_year['Year'] == year]
    for index, row in subset.iterrows():
        output_string += f"Username: {row['Username']}, Mentions: {row['Mentions']}\n"
    output_string += "\n"

# Write the output string to a Notepad file
output_file_path = 'brand_mentions_output.txt'
with open(output_file_path, 'w') as file:
    file.write(output_string)

# Print a message indicating the output file has been created
print(f"Output for usernames mentioning {brand_name} has been saved to brand_mentions_output.txt")

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
