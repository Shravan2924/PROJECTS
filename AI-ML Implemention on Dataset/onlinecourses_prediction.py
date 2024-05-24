import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Read Data
df = pd.read_csv('onlinecourses_dataset.csv')

# Set values in the 'incomplete' column to 1 where corresponding values in the 'complete' column are 0
df['incomplete'] = df['completed'].apply(lambda x: 1 if x == 0 else 0)

# Replace the value in the "chapter" column with 12
df.loc[df['courseid'] == 1, 'chapter'] = 12
df.loc[df['courseid'] == 2, 'chapter'] = 15
df.loc[df['courseid'] == 3, 'chapter'] = 8
df.loc[df['courseid'] == 4, 'chapter'] = 7
df.loc[df['courseid'] == 5, 'chapter'] = 5
df.loc[df['courseid'] == 6, 'chapter'] = 11
df.loc[df['courseid'] == 7, 'chapter'] = 9
df.loc[df['courseid'] == 8, 'chapter'] = 13
df.loc[df['courseid'] == 9, 'chapter'] = 16
df.loc[df['courseid'] == 10, 'chapter'] = 18
df.loc[df['courseid'] == 11, 'chapter'] = 19
df.loc[df['courseid'] == 12, 'chapter'] = 6
df.loc[df['courseid'] == 13, 'chapter'] = 8
df.loc[df['courseid'] == 14, 'chapter'] = 9
df.loc[df['courseid'] == 15, 'chapter'] = 17
df.loc[df['courseid'] == 16, 'chapter'] = 16

# Replace the value in the "chapter" field if it is greater than 15
df.loc[(df["chapter"] > 1) & (df["chapter"] < 10), "difficulty"] = "4"
df.loc[(df["chapter"] > 10) & (df["chapter"] < 15), "difficulty"] = "7"
df.loc[df["chapter"] >= 15, "difficulty"] = "10"

# Replace the value in the "chapter" field if it is greater than 15
df.loc[(df["chapter"] > 1) & (df["chapter"] < 10), "difficulty_level"] = "EASY"
df.loc[(df["chapter"] > 10) & (df["chapter"] < 15), "difficulty_level"] = "MEDIUM"
df.loc[df["chapter"] >= 15, "difficulty_level"] = "HARD"

# missing values in each Column 
missing_values_per_column = df.isnull().sum()

# Print the DataFrame and the number of missing values per column
print("\nNumber of missing values per column:")
print(missing_values_per_column)

# Count the number of completed and incompleted courses
completion_counts = df['completed'].value_counts()

# Assigning colors
colors = ["red", "green"]

# Plotting a pie chart with green for completed and red for incompleted
plt.figure(figsize=(8, 8))
plt.pie(completion_counts, labels=completion_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)

# Adding title
plt.title('Distribution of Completed and Incompleted Courses')

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

# Save the modified DataFrame to a new CSV file
df.to_csv('predicted_data.csv', index=False)

