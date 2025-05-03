


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn

# Define input schema
class MentalHealthInput(BaseModel):
    phq9: list[int]
    gad7: list[int]

# Load trained model
model = joblib.load("mental_health_model.pkl")  # Ensure this path matches your model file

# FastAPI app initialization
app = FastAPI(title="Mental Health Predictor API")

# Health check
@app.get("/")
def read_root():
    return {"message": "Mental Health API is running!"}

# Prediction route
@app.post("/predict")
def predict_mental_health(data: MentalHealthInput):
    if len(data.phq9) != 9 or len(data.gad7) != 7:
        raise HTTPException(status_code=400, detail="Invalid input length for PHQ-9 or GAD-7")

    features = np.array(data.phq9 + data.gad7).reshape(1, -1)
    total_score = sum(data.phq9 + data.gad7)

    prediction = model.predict(features)[0]

    if prediction == 0:
        level = "Minimal"
        recommendation = "You're doing well! Maintain a healthy routine."
    elif prediction == 1:
        level = "Mild"
        recommendation = "Consider some self-care and monitoring your feelings."
    elif prediction == 2:
        level = "Moderate"
        recommendation = "Talking to a counselor or support group may help."
    else:
        level = "Severe"
        recommendation = "We strongly recommend seeking professional help."

    return {
        "total_score": total_score,
        "level": level,
        "recommendation": recommendation
    }

# Run using: uvicorn api:app --reload
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

