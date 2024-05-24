import pandas as pd

# Read the CSV, assuming your data uses the column name 'courseid'
df = pd.read_csv('main.csv')

# Replace the value in the "chapter" column with 12
df.loc[df['Chapter'] == 1, 'Chapter'] = 12
df.loc[df['courseid'] == 2, 'Chapter'] = 15
df.loc[df['courseid'] == 3, 'Chapter'] = 8
df.loc[df['courseid'] == 4, 'Chapter'] = 7
df.loc[df['courseid'] == 5, 'Chapter'] = 5
df.loc[df['courseid'] == 6, 'Chapter'] = 11
df.loc[df['courseid'] == 7, 'Chapter'] = 9
df.loc[df['courseid'] == 8, 'Chapter'] = 13
df.loc[df['courseid'] == 9, 'Chapter'] = 16
df.loc[df['courseid'] == 10, 'Chapter'] = 18
df.loc[df['courseid'] == 11, 'Chapter'] = 19
df.loc[df['courseid'] == 12, 'Chapter'] = 6
df.loc[df['courseid'] == 13, 'Chapter'] = 8
df.loc[df['courseid'] == 14, 'Chapter'] = 9
df.loc[df['courseid'] == 15, 'Chapter'] = 17
df.loc[df['courseid'] == 16, 'Chapter'] = 16

# Print the updated dataset
df.to_csv('2.csv', index=False)