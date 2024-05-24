import pandas as pd
from sklearn.linear_model import LogisticRegression

# Assuming 'df' is your DataFrame with features and target variable
df = pd.read_csv('main.csv')

# Specify the columns for which you want to calculate feature importances
selected_columns = ['registered', 'viewed', 'certified','chapter','incomplete','complete']

# Create a subset DataFrame with selected columns

X_selected = df[selected_columns], 
y = df['complete']

# Initialize the model
model = LogisticRegression()

# Train the model
model.fit(X_selected, y)

# Get coefficients
coefficients = model.coef_[0]

# Create a DataFrame to show coefficients
coefficients_df = pd.DataFrame({'Feature': X_selected.columns, 'Coefficient': coefficients})
coefficients_df = coefficients_df.sort_values(by='Coefficient', ascending=False)

# Print or visualize coefficients
print(coefficients_df)
