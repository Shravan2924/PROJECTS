import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'df' is your DataFrame with information about courses
df = pd.read_csv('final.csv')
# You might have a column like 'course_category' or 'difficulty_level'

# Count the number of courses in each category
course_counts = df['courseid'].value_counts()

# Plotting a bar chart
user_counts_per_course = df.groupby('courseid')['userid'].nunique()

# Plotting a bar chart
plt.figure(figsize=(12, 6))
sns.barplot(x=user_counts_per_course.index, y=user_counts_per_course.values, palette="viridis")

# Adding labels and title
plt.xlabel('Course ID')
plt.ylabel('Number of Unique User IDs')
plt.title('Number of Unique User IDs per Course')


# Show the plot
plt.show()
