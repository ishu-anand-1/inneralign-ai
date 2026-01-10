import cv2
import numpy as np

FEATURE_NAMES = [
    "Slant Angle",
    "Baseline Consistency",
    "Stroke Pressure",
    "Letter Spacing",
    "Word Spacing",
    "X-Height Variation",
    "Loop Openness",
    "Writing Speed Proxy",
]


def extract_features(img):
    h, w = img.shape

    contours, _ = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = [c for c in contours if cv2.contourArea(c) > 40]

    if not contours:
        return default_features()

    areas = np.array([cv2.contourArea(c) for c in contours])
    boxes = [cv2.boundingRect(c) for c in contours]

    # ---------------- NUMERIC FEATURES ----------------
    stroke_pressure = np.clip(np.mean(areas) / 2000, 0, 1)

    baseline_var = np.std([y for (_, y, _, _) in boxes]) / h
    baseline_consistency = np.clip(1 - baseline_var, 0, 1)

    letter_spacing = np.clip(np.std([x for (x, _, _, _) in boxes]) / w, 0, 1)
    word_spacing = np.clip(letter_spacing * 1.5, 0, 1)

    x_height_var = np.clip(np.std([bh for (_, _, _, bh) in boxes]) / h, 0, 1)
    loop_openness = np.clip(np.mean(areas) / 2500, 0, 1)
    speed_proxy = np.clip(len(contours) / 900, 0, 1)

    slant_angle = 90 - np.degrees(
        np.arctan2(
            np.mean([bh for (_, _, _, bh) in boxes]),
            np.mean([bw for (_, _, bw, _) in boxes]),
        )
    )
    slant_angle = np.clip(slant_angle, 60, 120)

    # ---------------- RETURN FEATURES ----------------
    return [
        feature(
            "Slant Angle",
            display=f"{slant_angle:.1f}°",
            numeric=round((slant_angle - 60) / 60, 3),  # normalized 0–1
            interpretation="Forward-leaning writing"
            if slant_angle < 90
            else "Upright writing",
        ),
        feature(
            "Baseline Consistency",
            display=round(baseline_consistency, 2),
            numeric=baseline_consistency,
            interpretation="Stable baseline"
            if baseline_consistency > 0.6
            else "Fluctuating baseline",
        ),
        feature(
            "Stroke Pressure",
            display=round(stroke_pressure, 2),
            numeric=stroke_pressure,
            interpretation="Heavy pressure"
            if stroke_pressure > 0.6
            else "Light to moderate pressure",
        ),
        feature(
            "Letter Spacing",
            display=round(letter_spacing, 2),
            numeric=letter_spacing,
            interpretation="Balanced spacing"
            if 0.3 < letter_spacing < 0.7
            else "Irregular spacing",
        ),
        feature(
            "Word Spacing",
            display=round(word_spacing, 2),
            numeric=word_spacing,
            interpretation="Clear word separation"
            if word_spacing > 0.4
            else "Crowded words",
        ),
        feature(
            "X-Height Variation",
            display=round(x_height_var, 2),
            numeric=x_height_var,
            interpretation="Consistent letter height"
            if x_height_var < 0.4
            else "Variable letter height",
        ),
        feature(
            "Loop Openness",
            display=round(loop_openness, 2),
            numeric=loop_openness,
            interpretation="Open loops"
            if loop_openness > 0.5
            else "Closed loops",
        ),
        feature(
            "Writing Speed Proxy",
            display=round(speed_proxy, 2),
            numeric=speed_proxy,
            interpretation="Fast writing"
            if speed_proxy > 0.6
            else "Moderate writing speed",
        ),
    ]


# ---------------- HELPERS ----------------

def feature(name, display, numeric, interpretation):
    confidence = confidence_from_value(numeric)
    return {
        "name": name,
        "value": display,            # UI-safe
        "numeric_value": round(float(numeric), 3),  # ML-safe
        "interpretation": interpretation,
        "confidence": int(confidence * 100),
    }


def confidence_from_value(v):
    return float(np.clip(v, 0.5, 0.98))


def default_features():
    return [
        {
            "name": name,
            "value": "N/A",
            "numeric_value": 0.5,
            "interpretation": "Insufficient data",
            "confidence": 50,
        }
        for name in FEATURE_NAMES
    ]
