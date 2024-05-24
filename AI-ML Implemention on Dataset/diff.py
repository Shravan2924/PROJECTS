import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'df' is your DataFrame with information about courses and difficulty levels
df = pd.read_csv('final.csv')

# Count the number of courses for each difficulty level
difficulty_counts = df['difficulty'].value_counts()

# Plotting a bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x=difficulty_counts.index, y=difficulty_counts.values, palette="viridis")

# Adding labels and title
plt.xlabel('Difficulty Level')
plt.ylabel('Number of Courses')
plt.title('Difficulty Level Distribution of All Subjects')

# Show the plot
plt.show()
