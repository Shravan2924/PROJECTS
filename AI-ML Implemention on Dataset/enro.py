import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'df' is your DataFrame with information about courses and status columns
df = pd.read_csv('final.csv')

# Count the number of courses for each status
registered_counts = df['registered'].value_counts()
viewed_counts = df['viewed'].value_counts()
certified_counts = df['certified'].value_counts()

# Plotting individual bar charts for each status
plt.figure(figsize=(15, 6))

# Plotting for registered courses
plt.subplot(1, 3, 1)
sns.barplot(x=registered_counts.index, y=registered_counts.values, palette=["skyblue", "lightcoral"])
plt.title('Number of Registered Courses')
plt.xlabel('Status')
plt.ylabel('Count')

# Plotting for viewed courses
plt.subplot(1, 3, 2)
sns.barplot(x=viewed_counts.index, y=viewed_counts.values, palette=["skyblue", "lightcoral"])
plt.title('Number of Viewed Courses')
plt.xlabel('Status')
plt.ylabel('Count')

# Plotting for certified courses
plt.subplot(1, 3, 3)
sns.barplot(x=certified_counts.index, y=certified_counts.values, palette=["skyblue", "lightcoral"])
plt.title('Number of Certified Courses')
plt.xlabel('Status')
plt.ylabel('Count')

# Adjusting layout for better visualization
plt.tight_layout()

# Show the plot
plt.show()
