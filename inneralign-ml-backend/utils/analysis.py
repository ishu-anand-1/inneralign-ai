from utils.preprocess import preprocess_image
from utils.feature_extraction import extract_features
from utils.emotion_inference import infer_emotion
from utils.quality_analysis import assess_quality
import numpy as np

def run_full_analysis(img):
    processed = preprocess_image(img)

    quality = assess_quality(processed)
    features = extract_features(processed)
    emotion = infer_emotion(features)

    overall_conf = round(
        (quality["score"] * 0.3 + emotion["confidence"] * 0.7) * 100, 1
    )

    return {
        "overallConfidence": overall_conf,
        "qualityScore": round(quality["score"] * 100, 1),
        "emotion": emotion["label"],
        "emotionConfidence": round(emotion["confidence"] * 100, 1),
        "emotionReasons": emotion["reasons"],
        "features": features
    }
