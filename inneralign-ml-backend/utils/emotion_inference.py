import numpy as np
import joblib
import os

# -----------------------------------
# LOAD TRAINED MODEL (PRODUCTION SAFE)
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "rf_handwriting_emotion.pkl"
)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Emotion model not found at {MODEL_PATH}. "
        "Ensure rf_handwriting_emotion.pkl is committed to GitHub."
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
# MAIN EMOTION INFERENCE
# -----------------------------------
def infer_emotion(features):
    feature_map = {}

    for f in features:
        val = f["value"]

        # Normalize slant angle safely
        if isinstance(val, str) and "°" in val:
            val = float(val.replace("°", "")) / 120.0

        feature_map[f["name"]] = float(val)

    # Ensure correct order
    X = np.array([[feature_map[name] for name in FEATURE_ORDER]])

    # -----------------------------------
    # ML PREDICTION
    # -----------------------------------
    probs = model.predict_proba(X)[0]
    idx = int(np.argmax(probs))

    label = model.classes_[idx]
    confidence = float(probs[idx])

    # -----------------------------------
    # EXPLANATION (REALISTIC + ETHICAL)
    # -----------------------------------
    reasons = generate_reasons(features)

    return {
        "label": emotion_label_map(label),
        "confidence": round(min(confidence, 0.95), 2),
        "reasons": reasons
    }

# -----------------------------------
# EMOTION LABEL MAPPING
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
# REASON GENERATION (NO OVERCLAIM)
# -----------------------------------
def generate_reasons(features):
    reasons = []

    for f in features:
        name = f["name"]
        val = float(f["value"])

        if name == "Baseline Consistency" and val > 0.7:
            reasons.append(
                "Your writing baseline stays steady, often associated with emotional balance."
            )

        if name == "Stroke Pressure" and val > 0.7:
            reasons.append(
                "Firm writing pressure may reflect higher emotional or mental load."
            )

        if name == "Stroke Pressure" and val < 0.3:
            reasons.append(
                "Light pressure may suggest lower emotional energy or sensitivity."
            )

        if name == "Letter Spacing" and val < 0.4:
            reasons.append(
                "Tight letter spacing can sometimes be linked to nervousness or tension."
            )

        if name == "Writing Speed Proxy" and val > 0.75:
            reasons.append(
                "Faster writing speed may indicate internal pressure or urgency."
            )

        if name == "Writing Speed Proxy" and val < 0.4:
            reasons.append(
                "Slower writing speed may suggest carefulness or lower energy levels."
            )

    # Remove duplicates + limit output
    return list(dict.fromkeys(reasons))[:3]
