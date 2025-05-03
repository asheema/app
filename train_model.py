
    

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Generate synthetic data (1000 samples)
np.random.seed(42)
data = []

for _ in range(1000):
    phq9 = np.random.randint(0, 4, 9).tolist()
    gad7 = np.random.randint(0, 4, 7).tolist()
    total_score = sum(phq9) + sum(gad7)

    # Labeling based on total_score thresholds
    if total_score < 10:
        label = 0  # Mild
    elif 10 <= total_score < 15:
        label = 1  # Moderate
    elif 15 <= total_score < 20:
        label = 2  # Moderately Severe
    else:
        label = 3  # Severe

    data.append(phq9 + gad7 + [label])

# Create DataFrame
columns = [f"q{i+1}" for i in range(16)] + ["label"]
df = pd.DataFrame(data, columns=columns)

# Train/test split
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "random_forest_model.pkl")
print("Model saved as 'random_forest_model.pkl'")
