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
from utils.quality_feedback import quality_suggestions
from utils.explanation_engine import explain_feature
from utils.confidence_engine import confidence_message

app = Flask(__name__)

# ----------------- CORS CONFIG -----------------
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

# ----------------- HEALTH CHECK -----------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


# ----------------- HANDWRITING ANALYSIS -----------------
@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return jsonify({"status": "preflight ok"}), 200

    start_time = time.time()

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        # ----------------- LOAD IMAGE -----------------
        file = request.files["image"]
        img = Image.open(file.stream).convert("L")
        img_np = np.array(img)

        # ----------------- PREPROCESS IMAGE -----------------
        processed = preprocess_image(img_np)

        # ----------------- ASSESS QUALITY -----------------
        quality = assess_quality(processed)
        quality_tips = quality_suggestions(quality)

        # ⛔ ⛔ ⛔ BLANK IMAGE HARD STOP (WRITE HERE) ⛔ ⛔ ⛔
        if quality.get("is_blank", False):
            return jsonify({
                "overallConfidence": 8.0,
                "confidenceMessage": "No handwriting detected. Please upload a written page.",

                "qualityScore": 5.0,
                "qualityIssues": quality.get("issues", []),
                "qualitySuggestions": quality_tips,

                "emotion": "No Data",
                "emotionConfidence": 0.0,
                "emotionReasons": [
                    "The uploaded image does not contain handwriting."
                ],

                "features": [],
                "processingTime": int((time.time() - start_time) * 1000)
            }), 200
        # ⛔ ⛔ ⛔ END BLANK STOP ⛔ ⛔ ⛔

        # ----------------- EXTRACT FEATURES -----------------
        features = extract_features(processed)
        for f in features:
          explanation = explain_feature(f)

          f["simpleExplanation"] = explanation["description"]
          f["analysis"] = explanation

        # ----------------- PREDICT EMOTION -----------------
        emotion = infer_emotion(features)

        # ----------------- OVERALL CONFIDENCE -----------------
        feature_conf_avg = (
            sum(f["confidence"] for f in features) / (len(features) * 100)
            if features else 0
        )

        overall_conf = round(
            (quality["score"] * 0.25 +
             emotion["confidence"] * 0.45 +
             feature_conf_avg * 0.30) * 100,
            1
        )

        processing_time = int((time.time() - start_time) * 1000)

        # ----------------- RESPONSE -----------------
        return jsonify({
            "overallConfidence": overall_conf,
            "confidenceMessage": confidence_message(overall_conf / 100),

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

# ----------------- RUN SERVER -----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 