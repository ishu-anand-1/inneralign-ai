import numpy as np
import joblib
import os

# -----------------------------------
# LOAD TRAINED MODEL (PRODUCTION SAFE)
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "rf_handwriting_emotion.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Emotion model missing at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

FEATURE_ORDER = [
    "Slant Angle",
    "Baseline Consistency",
    "Stroke Pressure",
    "Letter Spacing",
    "Word Spacing",
    "X-Height Variation",
    "Loop Openness",
    "Writing Speed Proxy"
]

def infer_emotion(features):
    feature_map = {}

    for f in features:
        val = f["value"]
        if isinstance(val, str) and "°" in val:
            val = float(val.replace("°", "")) / 120.0
        feature_map[f["name"]] = float(val)

    X = np.array([[feature_map[n] for n in FEATURE_ORDER]])

    probs = model.predict_proba(X)[0]
    idx = int(np.argmax(probs))

    label = model.classes_[idx]
    confidence = float(probs[idx])

    return {
        "label": emotion_label_map(label),
        "confidence": round(min(confidence, 0.95), 2),
        "reasons": generate_reasons(features)
    }

def emotion_label_map(label):
    return {
        "Happy": "Happy / Positive",
        "Calm": "Calm / Neutral",
        "Stressed": "Stressed",
        "Anxious": "Anxious",
        "Sad": "Sad / Low Mood"
    }.get(label, "Calm / Neutral")

def generate_reasons(features):
    reasons = []

    for f in features:
        name = f["name"]
        val = float(f["value"])

        if name == "Baseline Consistency" and val > 0.7:
            reasons.append("Stable baseline suggests emotional balance.")
        if name == "Stroke Pressure" and val > 0.7:
            reasons.append("Heavy pressure may reflect mental load.")
        if name == "Stroke Pressure" and val < 0.3:
            reasons.append("Light pressure may suggest low emotional energy.")
        if name == "Letter Spacing" and val < 0.4:
            reasons.append("Tight spacing may indicate tension.")
        if name == "Writing Speed Proxy" and val > 0.75:
            reasons.append("Fast writing speed may suggest internal pressure.")

    return list(dict.fromkeys(reasons))[:3]
