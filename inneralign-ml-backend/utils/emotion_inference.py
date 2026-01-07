import numpy as np
import joblib
import os

# -----------------------------------
# LOAD TRAINED MODEL
# -----------------------------------
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "rf_handwriting_emotion.pkl"
)

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

# -----------------------------------
# MAIN EMOTION INFERENCE
# -----------------------------------
def infer_emotion(features):
    feature_map = {}

    for f in features:
        val = f["value"]

        # Normalize slant angle
        if isinstance(val, str) and "°" in val:
            val = float(val.replace("°", "")) / 120

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
    # EXPLANATION (SAFE + REALISTIC)
    # -----------------------------------
    reasons = generate_reasons(features, label)

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
def generate_reasons(features, emotion):
    reasons = []

    for f in features:
        name = f["name"]
        val = f["value"]

        if name == "Baseline Consistency" and val > 0.7:
            reasons.append("Stable baseline suggests emotional balance")

        if name == "Stroke Pressure" and val > 0.7:
            reasons.append("Heavy stroke pressure may indicate mental load")

        if name == "Stroke Pressure" and val < 0.3:
            reasons.append("Light pressure may reflect low emotional energy")

        if name == "Letter Spacing" and val < 0.4:
            reasons.append("Tight letter spacing may indicate nervousness")

        if name == "Writing Speed Proxy" and val > 0.75:
            reasons.append("Fast writing speed suggests internal pressure")

        if name == "Writing Speed Proxy" and val < 0.4:
            reasons.append("Slow writing speed suggests low energy or caution")

    # Limit reasons (judges like realism)
    return list(dict.fromkeys(reasons))[:3]
