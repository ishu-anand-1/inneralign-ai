from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import time

from utils.preprocess import preprocess_image
from utils.feature_extraction import extract_features
from utils.emotion_inference import infer_emotion
from utils.quality_analysis import assess_quality

# NEW EXPLAINABILITY IMPORTS
from utils.explanation_engine import explain_feature_simple
from utils.confidence_engine import confidence_message
from utils.quality_feedback import quality_suggestions

app = Flask(__name__)
CORS(app)


# -----------------------------------
# HEALTH CHECK
# -----------------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


# -----------------------------------
# ANALYZE HANDWRITING
# -----------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    start_time = time.time()

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        # -----------------------------
        # LOAD IMAGE
        # -----------------------------
        file = request.files["image"]
        img = Image.open(file.stream).convert("L")
        img_np = np.array(img)

        # -----------------------------
        # PREPROCESS IMAGE
        # -----------------------------
        processed = preprocess_image(img_np)

        # -----------------------------
        # QUALITY ANALYSIS
        # -----------------------------
        quality = assess_quality(processed)

        # -----------------------------
        # FEATURE EXTRACTION
        # -----------------------------
        features = extract_features(processed)

        # ADD SIMPLE EXPLANATIONS (HUMAN READABLE)
        for f in features:
            f["simpleExplanation"] = explain_feature_simple(f)

        # -----------------------------
        # EMOTION INFERENCE (ML MODEL)
        # -----------------------------
        emotion = infer_emotion(features)

        # -----------------------------
        # OVERALL CONFIDENCE CALCULATION
        # -----------------------------
        feature_conf_avg = sum(
            f["confidence"] for f in features
        ) / (len(features) * 100)

        overall_conf = round(
            (
                quality["score"] * 0.25 +
                emotion["confidence"] * 0.45 +
                feature_conf_avg * 0.30
            ) * 100,
            1
        )

        # CONFIDENCE MESSAGE
        confidence_text = confidence_message(overall_conf / 100)

        # QUALITY IMPROVEMENT SUGGESTIONS
        quality_tips = quality_suggestions(quality)

        processing_time = int((time.time() - start_time) * 1000)

        # -----------------------------
        # FINAL RESPONSE
        # -----------------------------
        return jsonify({
            "overallConfidence": overall_conf,
            "confidenceMessage": confidence_text,

            "qualityScore": round(quality["score"] * 100, 1),
            "qualityIssues": quality.get("issues", []),
            "qualitySuggestions": quality_tips,

            "emotion": emotion["label"],
            "emotionConfidence": round(emotion["confidence"] * 100, 1),
            "emotionReasons": emotion["reasons"],

            "features": features,
            "processingTime": processing_time
        })

    except Exception as e:
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500


# -----------------------------------
# RUN SERVER
# -----------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
