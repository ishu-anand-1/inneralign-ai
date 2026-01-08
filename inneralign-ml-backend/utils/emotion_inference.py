import numpy as np
import joblib
import os

# -----------------------------------
# LOAD TRAINED MODEL
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_handwriting_emotion.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Emotion model not found at {MODEL_PATH}. "
        "Ensure rf_handwriting_emotion.pkl is committed."
    )

model = joblib.load(MODEL_PATH)

# -----------------------------------
# FEATURE ORDER (MUST MATCH TRAINING)
# -----------------------------------
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

# -----------------------------------
# SAFE NUMERIC CONVERTER
# -----------------------------------
def clean_numeric(value):
    if isinstance(value, str):
        value = value.replace("°", "").replace("%", "").strip()
    return float(value)

# -----------------------------------
# MAIN EMOTION INFERENCE
# -----------------------------------
def infer_emotion(features):
    feature_map = {}

    for f in features:
        name = f["name"]
        val = clean_numeric(f["value"])

        # Normalize slant angle only
        if name == "Slant Angle":
            val = val / 120.0

        feature_map[name] = val

    # Ensure all features exist (fail-safe)
    X = np.array([[
        feature_map.get(name, 0.5)  # neutral fallback
        for name in FEATURE_ORDER
    ]])

    # -----------------------------------
    # MODEL PREDICTION
    # -----------------------------------
    probs = model.predict_proba(X)[0]
    idx = int(np.argmax(probs))

    confidence = float(probs[idx])

    return {
        "label": emotion_label_map(model.classes_[idx]),
        "confidence": min(confidence, 0.95),  # 🔒 always 0–1
        "reasons": generate_reasons(features)
    }

# -----------------------------------
# LABEL MAP
# -----------------------------------
def emotion_label_map(label):
    return {
        "Happy": "Happy / Positive",
        "Calm": "Calm / Neutral",
        "Stressed": "Stressed",
        "Anxious": "Anxious",
        "Sad": "Sad / Low Mood"
    }.get(label, "Calm / Neutral")

# -----------------------------------
# REASON GENERATOR (ETHICAL & SAFE)
# -----------------------------------
def generate_reasons(features):
    reasons = []

    for f in features:
        name = f["name"]
        val = clean_numeric(f["value"])

        if name == "Baseline Consistency" and val > 0.7:
            reasons.append(
                "Your writing baseline stays steady, often linked to emotional balance."
            )

        if name == "Stroke Pressure" and val > 0.7:
            reasons.append(
                "Firm writing pressure may reflect higher mental or emotional load."
            )

        if name == "Stroke Pressure" and val < 0.3:
            reasons.append(
                "Light pressure may suggest lower emotional energy or sensitivity."
            )

        if name == "Letter Spacing" and val < 0.4:
            reasons.append(
                "Tight letter spacing can sometimes indicate tension or nervousness."
            )

        if name == "Writing Speed Proxy" and val > 0.75:
            reasons.append(
                "Faster writing speed may indicate internal urgency or pressure."
            )

        if name == "Writing Speed Proxy" and val < 0.4:
            reasons.append(
                "Slower writing speed may reflect carefulness or lower energy."
            )

    return list(dict.fromkeys(reasons))[:3]
