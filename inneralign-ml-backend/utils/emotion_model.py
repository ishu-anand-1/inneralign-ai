import numpy as np
import pandas as pd
import joblib

from functools import lru_cache, wraps
from time import perf_counter

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

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



def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start = perf_counter()

        result = func(*args, **kwargs)

        elapsed = round(
            (perf_counter() - start) * 1000,
            2
        )

        result["processing_time_ms"] = elapsed

        return result

    return wrapper



def train_model(csv_path="handwriting_features.csv"):

    df = pd.read_csv(csv_path)

    X = df[FEATURE_COLUMNS]
    y = df["EmotionLabel"]

    scaler = MinMaxScaler()

    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=15,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_scaled, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print("✅ Model trained and saved")


class ModelManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.model = joblib.load(
                MODEL_PATH
            )

            cls._instance.scaler = joblib.load(
                SCALER_PATH
            )

        return cls._instance


manager = ModelManager()



def confidence_message(confidence):

    if confidence >= 0.90:
        return (
            "Very high confidence — handwriting "
            "patterns strongly support this prediction."
        )

    elif confidence >= 0.75:
        return (
            "High confidence — prediction appears reliable."
        )

    elif confidence >= 0.60:
        return (
            "Moderate confidence — some uncertainty exists."
        )

    elif confidence >= 0.40:
        return (
            "Low confidence — multiple emotions have "
            "similar probabilities."
        )

    return (
        "Very low confidence — image quality or "
        "feature extraction may affect accuracy."
    )



@lru_cache(maxsize=1000)
def _cached_predict(feature_tuple):

    X = manager.scaler.transform(
        [list(feature_tuple)]
    )

    probabilities = manager.model.predict_proba(X)[0]

    return probabilities.tolist()


@measure_time
def predict_emotion(numeric_features):

    if len(numeric_features) != 8:
        raise ValueError(
            f"Expected 8 features, got "
            f"{len(numeric_features)}"
        )

    feature_tuple = tuple(
        round(float(x), 4)
        for x in numeric_features
    )

    probabilities = _cached_predict(
        feature_tuple
    )

    classes = manager.model.classes_

    best_idx = int(np.argmax(probabilities))

    emotion = classes[best_idx]

    confidence = float(
        probabilities[best_idx]
    )

    
    ranked = sorted(
        zip(classes, probabilities),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    top_predictions = [
        {
            "emotion": emotion_name,
            "probability": round(prob, 3)
        }
        for emotion_name, prob in ranked
    ]

    
    importances = dict(
        zip(
            FEATURE_COLUMNS,
            manager.model.feature_importances_
        )
    )

    important_features = sorted(
        importances.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    return {
        "emotion": emotion,
        "confidence": round(confidence, 3),
        "confidence_message":
            confidence_message(confidence),

        "top_predictions":
            top_predictions,

        "important_features": [
            {
                "feature": name,
                "importance": round(score, 3)
            }
            for name, score in important_features
        ]
    }