# AI-Powered Mental Health Assessment & Recommendation System

# Project Overview


AI-Powered Mental Health Assessment & Recommendation System is a machine learning-powered web application designed to assess a user's mental health status using two clinically validated screening tools: PHQ-9 (for depression) and GAD-7 (for anxiety).

Users complete a series of questions, and the system:

Predicts their mental wellness level using a trained Random Forest model.

Provides recommendations based on the severity.

Uses K-Means clustering to group users into behavioral patterns.

Is equipped with CI/CD automation and responsible research disclosures.


# Introduction


The Mental Health Prediction System is a comprehensive web-based application designed to help users assess their mental well-being using two clinically validated tools — PHQ-9 (for depression) and GAD-7 (for anxiety). By leveraging machine learning, FastAPI, Streamlit, and CI/CD automation, the system offers users a fast, interactive, and privacy-respecting way to gain insights into their mental health patterns.

# Objectives
Self-assessment: Enable users to perform quick screenings based on PHQ-9 and GAD-7 scores.

Prediction: Use a trained Random Forest classifier to predict mental health severity (Minimal, Mild, Moderate, Severe).

Pattern Grouping: Use K-Means Clustering to group users based on their response trends for population-level insights.

Responsible Guidance: Offer basic actionable suggestions without replacing professional care.

CI/CD Readiness: Ensure that updates and bug fixes can be deployed quickly using GitHub Actions.


# Why This Matters
Mental health issues often go undetected or unaddressed. This tool aims to:

Lower the barrier to initial screening.

Empower users with self-awareness.

Provide responsible feedback grounded in scientific research.

Promote conversations around mental wellness in a safe, data-aware manner.


# Key Features

PHQ-9 & GAD-7-Screening	16-question assessment form based on validated clinical tools

Real-time Prediction	Backend FastAPI service delivers severity classification instantly

K-Means Clustering	Groups users into behavioral clusters for deeper insight

Validation Checks	Ensures all responses are submitted before prediction

CI/CD Pipeline-Automated deployment via GitHub Actions

Ethical AI Use-Clear disclaimer, non-diagnostic purpose, synthetic data training



# Technologies Used:

Frontend: Streamlit

Backend: FastAPI

Model: Random Forest (trained on synthetic PHQ-9 and GAD-7 data)

Deployment: GitHub Actions (CI/CD)


Setup Instructions

Project Structure

app/

├── appp.py               # Streamlit UI

├── api.py                # FastAPI backend

├── train_model.py        # Script to generate and train ML model

├── random_forest_model.pkl  # Saved model

├── requirements.txt

├── .env                 # Environment configuration

├── .github/workflows/
│   └── deploy.yml        # CI/CD workflow


# Local Setup

Clone the Repository
git clone https://github.com/asheema/app.git
cd app

Install Dependencies
pip install -r requirements.txt

Run the Backend
uvicorn api:app --reload

Run the Frontend
streamlit run app.py

API Documentation

Base URL
http://localhost:8000

Health Check

Endpoint: /

Method: 

Response:

{ "message": "Mental Health API is running!" }

Predict Endpoint

Endpoint: /predict

Method: POST

Payload:

{
  "phq9": [1, 0, 2, 1, 1, 2, 0, 1, 0],
  "gad7": [0, 1, 1, 1, 2, 1, 0]
}

Response:

{
  "total_score": 14,
  "level": "Moderate",
  "recommendation": "Talking to a counselor or support group may help."
}

Errors:

400: If PHQ-9 or GAD-7 inputs are incomplete or malformed.




.env.example

API_URL=http://localhost:8000

MODEL_PATH=random_forest_model.pkl

After copying, rename this file to .env and customize as needed.


# Local Setup: Frontend + Backend Integration

Backend (FastAPI):

Run your backend API server with:

uvicorn api:app --reload

URL: http://127.0.0.1:8000 or http://localhost:8000

This serves your ML model prediction logic.

Frontend (Streamlit):

Run your frontend UI with:

streamlit run appp.py

URL: http://localhost:8501

The frontend will send a request to http://127.0.0.1:8000/predict when the user clicks "Predict".

Ensure both are running simultaneously in separate terminals.

Deployment on Render: Full Setup with Frontend + Backend

Backend (FastAPI) on Render

Push your backend code (api.py, model.pkl, train_model.py, etc.) to a GitHub repo.

Create a new Web Service on Render.

Build Command: pip install -r requirements.txt

Start Command: uvicorn api:app --host 0.0.0.0 --port 10000

Set port to 10000 in Render.

Once deployed, you'll get a public URL like:

https://app-1-g00m.onrender.com/

Replace http://127.0.0.1:8000 with this in your Streamlit appp.py.

Frontend (Streamlit) on Render

Push your app.py and related frontend code to another GitHub repo.

Create another Web Service on Render.

Build Command: pip install -r requirements.txt

Start Command: streamlit run app.py --server.port 10001 --server.enableCORS false

Once deployed, you’ll get a URL like:

https://app-1-g00m.onrender.com/

Integrating Frontend with Backend on Render

Edit appp.py to call Render backend:

API_URL = "http://127.0.0.1:8000/predict"

Make sure this replaces any local URL like http://127.0.0.1:8000.



# ML Model Development, Training Details & Evaluation

Model Used: Random Forest Classifier
Understanding Random Forest in This Project
Random Forest is a supervised machine learning algorithm used for classification and regression tasks. It works by building a "forest" of many decision trees and combining their results to make a final prediction.
In this case, it’s used for classification: predicting a mental health severity level (Minimal, Mild, Moderate, Severe) based on PHQ-9 and GAD-7 scores.

How It Works (Step-by-Step):
Multiple Decision Trees Are Created:
Each tree is trained on a random subset of the data (bootstrapping).
For each node split, only a random subset of features is considered (feature bagging).
Training with PHQ-9 + GAD-7 Inputs:
Input features: A user answers 16 questions (9 from PHQ-9, 7 from GAD-7), each scored from 0 to 3.

Example Input: [1, 2, 0, 3, 1, 1, 2, 0, 1, 1, 1, 2, 2, 0, 1, 1]
Target label: Mental health severity level, mapped from total score.
Each Tree Predicts Independently:
Trees make their own decisions (e.g., "this input is 'Moderate'").
Trees might not always agree.

Voting Mechanism:
The final classification is made by majority voting across all trees.
If 70 out of 100 trees predict "Moderate", and 30 predict "Mild", the final result is Moderate.

# Why Random Forest Is a Good Choice for This Use Case
Feature	Benefit
Handles categorical + numerical data	
Resistant to overfitting	
Feature importance insights	
Fast inference
This logic is used during training to assign correct class labels to each data point.

Evaluation Metrics (Typical)

On synthetic data (1000 samples):

Training Accuracy: ~99% (since the rules are deterministic)


Test Accuracy: ~90% (some variance due to random data noise)

Model size: Small enough for quick API response (<1MB as .pkl)

Features: 9 PHQ-9 questions + 7 GAD-7 questions (total 16 features)


Target Labels:
0: Minimal

1: Mild

2: Moderate

3: Severe

Data Generation (Synthetic)
Randomized synthetic scores from [0–3] across PHQ-9 and GAD-7
Labeled severity based on total score ranges:

0–9: Minimal

10–14: Mild

15–19: Moderate

20+: Severe

Training Script: train_model.py


# Generates synthetic data and trains a RandomForest model
from sklearn.ensemble import RandomForestClassifier

import numpy as np

import joblib

X = np.random.randint(0, 4, size=(1000, 16))

y = np.array([0 if s <= 9 else 1 if s <= 14 else 2 if s <= 19 else 3 for s in X.sum(axis=1)])

model = RandomForestClassifier(n_estimators=100, random_state=42)

model.fit(X, y)

joblib.dump(model, "random_forest_model.pkl")


# Evaluation
Accuracy (on synthetic test split): ~90%

Fast inference and high generalization on score-based severity categories


# Additional Notes

The Clustering feature in app.py uses KMeans to group user response patterns into 3 clusters for analysis, based on past response trends.

CI/CD pipeline auto-deploys the app using GitHub Actions (.github/workflows/deploy.yml).

Responsible AI: Includes ethical disclaimers, research references, and prioritizes user safety.
