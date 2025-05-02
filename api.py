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
    """
"""
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load the trained RandomForest model
model = joblib.load('mental_health_model.pkl')

# Define the request body for prediction
class PredictionRequest(BaseModel):
    phq9: list
    gad7: list

app = FastAPI()

@app.post("/predict")
def predict(request: PredictionRequest):
    # Flatten and combine the features (do this explicitly)
    features = np.hstack([np.array(request.phq9).flatten(), np.array(request.gad7).flatten()])

    # Make prediction
    prediction = model.predict([features])
    total_score = sum(request.phq9) + sum(request.gad7)
    
    # Determine the mental health level based on prediction
    level_dict = {0: 'None', 1: 'Mild', 2: 'Moderate', 3: 'Severe', 4: 'Very Severe'}
    level = level_dict.get(prediction[0], 'Unknown')

    # Recommendation based on the score
    if level == 'None':
        recommendation = 'You are doing well. Keep it up!'
    elif level == 'Mild':
        recommendation = 'Consider managing stress and monitoring your mood.'
    elif level == 'Moderate':
        recommendation = 'You may benefit from seeking professional help.'
    elif level == 'Severe':
        recommendation = 'It’s highly recommended to consult a healthcare provider.'
    else:
        recommendation = 'Please seek immediate professional help.'

    return {
        'total_score': total_score,
        'level': level,
        'recommendation': recommendation
    }
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np
import uvicorn

# Define the input schema using Pydantic
class InputData(BaseModel):
    phq9: List[int]
    gad7: List[int]

# Initialize FastAPI app
app = FastAPI(title="Mental Health Prediction API")

# Load the trained model
try:
    model = joblib.load("random_forest_model.pkl")  # Ensure this file is in the same directory
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Define the prediction endpoint
@app.post("/predict")
def predict(input_data: InputData):
    if len(input_data.phq9) != 9 or len(input_data.gad7) != 7:
        raise HTTPException(status_code=400, detail="PHQ-9 must have 9 items and GAD-7 must have 7.")

    input_features = np.array(input_data.phq9 + input_data.gad7).reshape(1, -1)

    try:
        prediction = model.predict(input_features)[0]
        total_score = sum(input_data.phq9) + sum(input_data.gad7)

        # Interpret prediction class
        level_mapping = {
            0: "Mild",
            1: "Moderate",
            2: "Moderately Severe",
            3: "Severe"
        }
        level = level_mapping.get(prediction, "Unknown")

        recommendation = {
            "Mild": "Maintain healthy habits and check in with yourself regularly.",
            "Moderate": "Consider talking to a counselor or therapist.",
            "Moderately Severe": "Seek professional help soon.",
            "Severe": "Immediate help is recommended from a licensed mental health provider."
        }.get(level, "Consult a mental health professional.")

        return {
            "level": level,
            "recommendation": recommendation,
            "total_score": total_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

# Run the API (optional for local testing)
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
