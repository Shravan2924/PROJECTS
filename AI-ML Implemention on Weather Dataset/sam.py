import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from IPython.display import display


data = pd.read_csv('weather_data.csv') 

# Split the data into training and testing sets
X = data[['temperature', 'humidity']]  # Features
y = data['weather_condition']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train decision tree
dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)

# Evaluate decision tree
y_pred_dt = dt_classifier.predict(X_test)
accuracy_dt = accuracy_score(y_test, y_pred_dt)
report_dt = classification_report(y_test, y_pred_dt)

print("Decision Tree")
print(f"Accuracy: {accuracy_dt:.2f}")
print(f"Classification Report:\n{report_dt}\n")
display(pd.DataFrame({"Accuracy": [accuracy_dt], "Classification Report": [report_dt]}))

# Train random forest
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Evaluate random forest
y_pred_rf = rf_classifier.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
report_rf = classification_report(y_test, y_pred_rf)

print("Random Forest")
print(f"Accuracy: {accuracy_rf:.2f}")
print(f"Classification Report:\n{report_rf}\n")
display(pd.DataFrame({"Accuracy": [accuracy_rf], "Classification Report": [report_rf]}))

# Train ensemble model
ensemble_clf = VotingClassifier(estimators=[
    ('dt', dt_classifier),
    ('rf', rf_classifier)], voting='soft')

ensemble_clf.fit(X_train_scaled, y_train)  # Use scaled data

y_pred_ensemble = ensemble_clf.predict(X_test_scaled)
accuracy_ensemble = accuracy_score(y_test, y_pred_ensemble)
report_ensemble = classification_report(y_test, y_pred_ensemble)

print("Ensemble Model")
print(f"Accuracy: {accuracy_ensemble:.2f}")
print(f"Classification Report:\n{report_ensemble}\n")
display(pd.DataFrame({"Accuracy": [accuracy_ensemble], "Classification Report": [report_ensemble]}))
