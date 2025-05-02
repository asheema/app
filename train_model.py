
import joblib
from sklearn.ensemble import RandomForestClassifier
from generate_data import generate_synthetic_data
import numpy as np

df = generate_synthetic_data()
X = df.apply(lambda row: row['phq_9_scores'] + row['gad_7_scores'], axis=1).tolist()
y = df['label']

model = RandomForestClassifier()
model.fit(X, y)
joblib.dump(model, 'mental_health_model.pkl')
print("Model trained and saved!")

"""
# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import joblib
from generate_data import generate_synthetic_data

def flatten_scores(X):
    return np.hstack([np.array(X['phq_9_scores'].tolist()), np.array(X['gad_7_scores'].tolist())])

def main():
    df = generate_synthetic_data()

    X = df[['phq_9_scores', 'gad_7_scores']]
    y = df['label']

    pipeline = Pipeline([
        ('flatten', FunctionTransformer(flatten_scores, validate=False)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X, y)
    joblib.dump(pipeline, 'mental_health_model.pkl')
    print("✅ Model saved as 'mental_health_model.pkl'.")

if __name__ == "__main__":
    main()
"""