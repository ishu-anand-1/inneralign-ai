from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import time
import os

from utils.preprocess import preprocess_image
from utils.feature_extraction import extract_features
from utils.emotion_inference import infer_emotion
from utils.quality_analysis import assess_quality
from utils.explanation_engine import explain_feature_simple
from utils.confidence_engine import confidence_message
from utils.quality_feedback import quality_suggestions

app = Flask(__name__)

# 🔥 ABSOLUTE CORS FIX (WORKS ON RENDER + VERCEL)
CORS(
     app,
    resources={r"/*": {
        "origins": [
            "http://localhost:5173",
            "https://inneralign-ai.vercel.app",
            "https://inneralign-53kf3yprf-ishu-anand-1s-projects.vercel.app"
        ]
    }},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# -----------------------------------
# HEALTH CHECK
# -----------------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


# -----------------------------------
# ANALYZE HANDWRITING
# -----------------------------------
@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return jsonify({"status": "preflight ok"}), 200

    start_time = time.time()

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        file = request.files["image"]
        img = Image.open(file.stream).convert("L")
        img_np = np.array(img)

        processed = preprocess_image(img_np)
        quality = assess_quality(processed)
        features = extract_features(processed)

        for f in features:
            f["simpleExplanation"] = explain_feature_simple(f)

        emotion = infer_emotion(features)

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

        processing_time = int((time.time() - start_time) * 1000)

        return jsonify({
            "overallConfidence": overall_conf,
            "confidenceMessage": confidence_message(overall_conf / 100),

            "qualityScore": round(quality["score"] * 100, 1),
            "qualityIssues": quality.get("issues", []),
            "qualitySuggestions": quality_suggestions(quality),

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
