import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'df' is your DataFrame with information about courses and completion status
df = pd.read_csv('final.csv')

# Count the number of completed and incompleted courses
completion_counts = df['complete'].value_counts()

# Assigning colors
colors = ["red", "green"]

# Plotting a pie chart with green for completed and red for incompleted
plt.figure(figsize=(8, 8))
plt.pie(completion_counts, labels=completion_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)

# Adding title
plt.title('Distribution of Completed and Incompleted Courses')

# Show the plot
plt.show()
