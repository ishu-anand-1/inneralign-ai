import os
import joblib
import numpy as np
from functools import lru_cache

# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "rf_handwriting_emotion.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "feature_scaler.pkl"
)

# =====================================================
# LOAD MODEL + SCALER
# =====================================================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(
        f"Scaler not found: {SCALER_PATH}"
    )

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# =====================================================
# FEATURE ORDER
# =====================================================

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

# =====================================================
# SAFE FLOAT
# =====================================================

def safe_numeric(value):

    if isinstance(value, str):
        value = (
            value.replace("°", "")
            .replace("%", "")
            .strip()
        )

    try:
        return float(value)

    except Exception:
        return 0.5

# =====================================================
# CONFIDENCE MESSAGE
# =====================================================

def confidence_message(confidence):

    if confidence >= 0.85:
        return (
            "High confidence — handwriting patterns "
            "strongly support this prediction."
        )

    elif confidence >= 0.65:
        return (
            "Moderate confidence — results appear "
            "reasonably reliable."
        )

    elif confidence >= 0.40:
        return (
            "Low confidence — multiple emotional "
            "categories show similar probabilities."
        )

    return (
        "Very low confidence — image quality or "
        "feature extraction may affect accuracy."
    )

# =====================================================
# CACHE PREDICTIONS
# =====================================================

@lru_cache(maxsize=500)
def cached_predict(feature_tuple):

    X = scaler.transform([list(feature_tuple)])

    probabilities = model.predict_proba(X)[0]

    return probabilities.tolist()

# =====================================================
# MAIN INFERENCE
# =====================================================

def infer_emotion(features):

    feature_map = {
        f["name"]: safe_numeric(
            f.get("numeric_value", 0.5)
        )
        for f in features
    }

    ordered_features = [
        feature_map.get(name, 0.5)
        for name in FEATURE_ORDER
    ]

    probabilities = cached_predict(
        tuple(
            round(x, 4)
            for x in ordered_features
        )
    )

    classes = model.classes_

    best_idx = int(np.argmax(probabilities))

    emotion = classes[best_idx]

    confidence = float(
        probabilities[best_idx]
    )

    # Top 3 predictions
    ranked = sorted(
        zip(classes, probabilities),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    top_predictions = [
        {
            "emotion":
                emotion_label_map(label),
            "probability":
                round(prob, 3)
        }
        for label, prob in ranked
    ]

    # Feature importance
    important_features = []

    if hasattr(model, "feature_importances_"):

        importance_pairs = list(
            zip(
                FEATURE_ORDER,
                model.feature_importances_
            )
        )

        importance_pairs.sort(
            key=lambda x: x[1],
            reverse=True
        )

        important_features = [
            {
                "feature": feature,
                "importance": round(score, 3)
            }
            for feature, score
            in importance_pairs[:3]
        ]

    return {
        "label":
            emotion_label_map(emotion),

        "confidence":
            round(confidence, 3),

        "confidenceMessage":
            confidence_message(confidence),

        "topPredictions":
            top_predictions,

        "importantFeatures":
            important_features,

        "reasons":
            generate_reasons(features)
    }

# =====================================================
# LABEL MAP
# =====================================================

def emotion_label_map(label):

    mapping = {
        "Happy": "Happy / Positive",
        "Calm": "Calm / Neutral",
        "Stressed": "Stressed",
        "Anxious": "Anxious",
        "Sad": "Sad / Low Mood"
    }

    return mapping.get(
        label,
        "Calm / Neutral"
    )

# =====================================================
# REASON GENERATOR
# =====================================================

def generate_reasons(features):

    reasons = []

    for feature in features:

        name = feature["name"]

        value = safe_numeric(
            feature.get(
                "numeric_value",
                0.5
            )
        )

        if (
            name == "Baseline Consistency"
            and value > 0.75
        ):
            reasons.append(
                "A steady baseline suggests consistent writing patterns."
            )

        elif (
            name == "Baseline Consistency"
            and value < 0.4
        ):
            reasons.append(
                "Variations in baseline may indicate inconsistent writing flow."
            )

        if (
            name == "Stroke Pressure"
            and value > 0.75
        ):
            reasons.append(
                "Firm writing pressure indicates strong pen contact."
            )

        elif (
            name == "Stroke Pressure"
            and value < 0.30
        ):
            reasons.append(
                "Light pressure indicates softer writing intensity."
            )

        if (
            name == "Letter Spacing"
            and value < 0.40
        ):
            reasons.append(
                "Tighter letter spacing was detected."
            )

        if (
            name == "Writing Speed"
            and value > 0.70
        ):
            reasons.append(
                "Writing appears relatively fast and fluid."
            )

        elif (
            name == "Writing Speed"
            and value < 0.35
        ):
            reasons.append(
                "Writing speed appears slower and more deliberate."
            )

    return list(dict.fromkeys(reasons))[:3]