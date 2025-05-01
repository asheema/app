# api.py
"""
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib

# Create app instance
app = FastAPI()

# CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your trained model (assumed to be saved as 'mental_health_model.pkl')
# model = joblib.load("mental_health_model.pkl")
# For this example, we’ll mock predictions

class MHRequest(BaseModel):
    phq_9: list[int]
    gad_7: list[int]

@app.post("/predict")
def predict_mental_health(data: MHRequest):
    phq_score = sum(data.phq_9)
    gad_score = sum(data.gad_7)
    total_score = phq_score + gad_score

    # Custom recommendation logic (can be replaced with model.predict logic)
    if total_score <= 9:
        level = "Mild"
        recommendation = "You're doing well. Keep practicing self-care and check in with yourself often."
    elif total_score <= 19:
        level = "Moderate"
        recommendation = "You may be experiencing some mental strain. Consider talking to a counselor."
    else:
        level = "Severe"
        recommendation = "You might be going through a tough time. It's strongly recommended to seek professional help."

    return {
        "total_score": total_score,
        "level": level,
        "recommendation": recommendation
    }
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class MentalHealthInput(BaseModel):
    phq9: List[int]
    gad7: List[int]

@app.post("/predict")
def predict_score(data: MentalHealthInput):
    total_score = sum(data.phq9) + sum(data.gad7)
    if total_score <= 9:
        level = "🟢 Mild"
        recommendation = "Maintain healthy habits and monitor mood."
    elif total_score <= 19:
        level = "🟡 Moderate"
        recommendation = "Consider talking to a counselor or therapist."
    else:
        level = "🔴 Severe"
        recommendation = "Seek professional help immediately."

    return {
        "total_score": total_score,
        "level": level,
        "recommendation": recommendation
    }
