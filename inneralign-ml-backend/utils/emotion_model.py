import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import joblib

FEATURE_COLUMNS = [
    "Slant",
    "Baseline",
    "Pressure",
    "LetterSpacing",
    "WordSpacing",
    "XHeight",
    "LoopOpen",
    "Speed",
]

MODEL_PATH = "rf_handwriting_emotion.pkl"
SCALER_PATH = "feature_scaler.pkl"


# -------------------------------------------------
# TRAIN MODEL (RUN ONCE)
# -------------------------------------------------

def train_model(csv_path="handwriting_features.csv"):
    df = pd.read_csv(csv_path)

    X = df[FEATURE_COLUMNS]
    y = df["EmotionLabel"]

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        class_weight="balanced",
        random_state=42,
    )

    model.fit(X_scaled, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print("✅ Emotion model trained and saved")


# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# -------------------------------------------------
# PREDICT EMOTION
# -------------------------------------------------

def predict_emotion(numeric_features):
    """
    numeric_features: list of 8 normalized values (0–1)
    """

    if len(numeric_features) != 8:
        raise ValueError("Expected 8 handwriting features")

    X = scaler.transform([numeric_features])

    probabilities = model.predict_proba(X)[0]
    classes = model.classes_

    best_idx = np.argmax(probabilities)

    emotion = classes[best_idx]
    confidence = float(probabilities[best_idx])

    return {
        "emotion": emotion,
        "confidence": round(confidence, 3),
        "confidence_message": confidence_message(confidence),
    }


# -------------------------------------------------
# CONFIDENCE MESSAGE
# -------------------------------------------------

def confidence_message(confidence):
    if confidence >= 0.85:
        return "High confidence — handwriting signals are very consistent."
    elif confidence >= 0.65:
        return "Moderate confidence — results are reliable."
    else:
        return "Low confidence — image quality or writing clarity may affect accuracy."
