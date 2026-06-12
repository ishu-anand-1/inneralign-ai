from time import perf_counter

from utils.preprocess import preprocess_image
from utils.feature_extraction import extract_features
from utils.emotion_inference import infer_emotion
from utils.quality_analysis import assess_quality
from utils.emotion_stability import emotion_stability


def run_full_analysis(img):
    """
    Main orchestration pipeline for InnerAlign AI
    """

    start_time = perf_counter()

    try:

        # ----------------------------------------
        # Step 1: Preprocess Image
        # ----------------------------------------
        processed = preprocess_image(img)

        # ----------------------------------------
        # Step 2: Quality Assessment
        # ----------------------------------------
        quality = assess_quality(processed)

        # ----------------------------------------
        # Step 3: Feature Extraction
        # ----------------------------------------
        features = extract_features(processed)

        # ----------------------------------------
        # Step 4: Emotion Prediction
        # ----------------------------------------
        emotion = infer_emotion(features)

        # ----------------------------------------
        # Step 5: Stability Analysis
        # ----------------------------------------
        stability = emotion_stability(features)

        # ----------------------------------------
        # Step 6: Dynamic Confidence Weighting
        # ----------------------------------------

        quality_score = float(quality["score"])
        emotion_conf = float(emotion["confidence"])
        stability_score = float(stability["score"])

        if quality_score < 0.5:
            quality_weight = 0.50
            emotion_weight = 0.30
            stability_weight = 0.20
        else:
            quality_weight = 0.25
            emotion_weight = 0.55
            stability_weight = 0.20

        overall_conf = round(
            (
                quality_score * quality_weight
                + emotion_conf * emotion_weight
                + stability_score * stability_weight
            )
            * 100,
            1,
        )

        # ----------------------------------------
        # Step 7: Risk Flags
        # ----------------------------------------

        flags = []

        if quality_score < 0.50:
            flags.append(
                "Low image quality may reduce analysis accuracy."
            )

        if emotion_conf < 0.50:
            flags.append(
                "Emotion prediction confidence is low."
            )

        if stability_score < 0.40:
            flags.append(
                "Handwriting features show high variability."
            )

        # ----------------------------------------
        # Step 8: Confidence Category
        # ----------------------------------------

        if overall_conf >= 80:
            confidence_level = "High"
        elif overall_conf >= 60:
            confidence_level = "Moderate"
        else:
            confidence_level = "Low"

        # ----------------------------------------
        # Step 9: Processing Time
        # ----------------------------------------

        processing_time = round(
            (perf_counter() - start_time) * 1000,
            2
        )

        # ----------------------------------------
        # Final Response
        # ----------------------------------------

        return {
            "success": True,

            "overallConfidence": overall_conf,
            "confidenceLevel": confidence_level,

            "qualityScore": round(
                quality_score * 100,
                1
            ),

            "emotion": emotion["label"],

            "emotionConfidence": round(
                emotion_conf * 100,
                1
            ),

            "emotionReasons": emotion.get(
                "reasons",
                []
            ),

            "stabilityScore": round(
                stability_score * 100,
                1
            ),

            "stabilityLabel": stability["label"],

            "stabilityMessage": stability["message"],

            "features": features,

            "flags": flags,

            "processingTimeMs": processing_time,
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "overallConfidence": 0,
        }