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
        "Ensure rf_handwriting_emotion.pkl is present."
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
    "Writing Speed",
]

# -----------------------------------
# HELPER: SAFE NUMERIC CONVERSION
# -----------------------------------
def safe_numeric(val):
    """
    Converts string or numeric values to float safely.
    Removes degree or percentage symbols.
    """
    if isinstance(val, str):
        val = val.replace("°", "").replace("%", "").strip()
    try:
        return float(val)
    except Exception:
        return 0.5  # fallback neutral value

# -----------------------------------
# MAIN EMOTION INFERENCE
# -----------------------------------
def infer_emotion(features):
    """
    Input:
        features: list of dicts returned by extract_features()
    Output:
        dict: label, confidence (0–1), reasons
    """

    # Map feature names → numeric values
    feature_map = {
        f["name"]: safe_numeric(f.get("numeric_value", 0.5))
        for f in features
    }

    # Build model input in correct order
    X = np.array([[feature_map.get(name, 0.5) for name in FEATURE_ORDER]])

    # Predict probabilities
    probs = model.predict_proba(X)[0]
    best_idx = int(np.argmax(probs))
    label = model.classes_[best_idx]
    confidence = float(probs[best_idx])

    return {
        "label": emotion_label_map(label),
        "confidence": round(np.clip(confidence, 0, 0.95), 3),
        "reasons": generate_reasons(features),
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
        "Sad": "Sad / Low Mood",
    }.get(label, "Calm / Neutral")

# -----------------------------------
# REASON GENERATOR
# -----------------------------------
def generate_reasons(features):
    """
    Provides up to 3 professional explanations for detected emotion.
    """

    reasons = []

    for f in features:
        name = f["name"]
        val = safe_numeric(f.get("numeric_value", 0.5))

        if name == "Baseline Consistency":
            if val > 0.7:
                reasons.append("A steady baseline indicates emotional stability.")
            elif val < 0.4:
                reasons.append("Fluctuating baseline may reflect mood variability.")

        if name == "Stroke Pressure":
            if val > 0.7:
                reasons.append("Firm pressure can reflect higher mental or emotional load.")
            elif val < 0.3:
                reasons.append("Light pressure may indicate sensitivity or low energy.")

        if name == "Letter Spacing":
            if val < 0.4:
                reasons.append("Tight letter spacing may indicate internal tension or stress.")

        if name == "Writing Speed":
            if val > 0.65:
                reasons.append("Fast writing may indicate urgency or heightened mental activity.")
            elif val < 0.4:
                reasons.append("Slow writing may reflect carefulness or lower energy.")

    # Deduplicate and limit to top 3 reasons
    return list(dict.fromkeys(reasons))[:3]
