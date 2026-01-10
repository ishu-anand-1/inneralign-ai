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
    "Writing Speed",
]

def extract_features(img):
    h, w = img.shape[:2]

    # Convert to grayscale if needed
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding for language-agnostic binarization
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Detect contours
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dynamic noise filtering based on image size
    min_area = max(40, (h * w) // 15000)
    contours = [c for c in contours if cv2.contourArea(c) > min_area]

    if not contours:
        return default_features()

    areas = np.array([cv2.contourArea(c) for c in contours])
    boxes = [cv2.boundingRect(c) for c in contours]

    xs = np.array([x for (x, _, _, _) in boxes])
    ys = np.array([y for (_, y, _, _) in boxes])
    widths = np.array([bw for (_, _, bw, _) in boxes])
    heights = np.array([bh for (_, _, _, bh) in boxes])

    # ---------------- NUMERIC FEATURES (0–1) ----------------

    stroke_pressure = np.clip(np.mean(areas) / 2400, 0, 1)
    baseline_consistency = np.clip(1 - np.std(ys) / h, 0, 1)
    letter_spacing = np.clip(np.std(xs) / w, 0, 1)
    word_spacing = np.clip(letter_spacing * 1.3, 0, 1)
    x_height_var = np.clip(np.std(heights) / h, 0, 1)
    loop_openness = np.clip(np.mean(areas) / 2800, 0, 1)
    speed = np.clip(len(contours) / (w * h / 5000), 0, 1)

    # Median-based slant angle (more robust to noise)
    slant_angle = 90 - np.degrees(np.arctan2(np.median(heights), np.median(widths)))
    slant_angle = np.clip(slant_angle, 60, 120)
    slant_norm = np.clip((slant_angle - 60) / 60, 0, 1)

    # ---------------- RETURN FEATURES ----------------
    return [
        make_feature("Slant Angle", f"{slant_angle:.1f}°", slant_norm,
                     "Forward-leaning" if slant_angle < 88 else "Upright"),
        make_feature("Baseline Consistency", round(baseline_consistency, 2),
                     baseline_consistency, "Stable" if baseline_consistency > 0.6 else "Fluctuating"),
        make_feature("Stroke Pressure", round(stroke_pressure, 2), stroke_pressure,
                     "Heavy" if stroke_pressure > 0.6 else "Moderate"),
        make_feature("Letter Spacing", round(letter_spacing, 2), letter_spacing,
                     "Balanced" if 0.3 < letter_spacing < 0.7 else "Irregular"),
        make_feature("Word Spacing", round(word_spacing, 2), word_spacing,
                     "Clear" if word_spacing > 0.4 else "Crowded"),
        make_feature("X-Height Variation", round(x_height_var, 2), x_height_var,
                     "Consistent" if x_height_var < 0.4 else "Variable"),
        make_feature("Loop Openness", round(loop_openness, 2), loop_openness,
                     "Open" if loop_openness > 0.5 else "Closed"),
        make_feature("Writing Speed", round(speed, 2), speed,
                     "Fast" if speed > 0.6 else "Moderate"),
    ]


# ---------------- HELPERS ----------------

def make_feature(name, display, numeric, interpretation):
    """
    Create a structured feature dict with confidence.
    """
    confidence = confidence_from_value(numeric)
    return {
        "name": name,
        "value": display,
        "numeric_value": round(float(numeric), 3),
        "interpretation": interpretation,
        "confidence": int(confidence * 100),
    }


def confidence_from_value(v):
    """
    Returns confidence based on numeric value, prevents overconfidence on noisy images.
    """
    return float(np.clip(0.55 + v * 0.4, 0.55, 0.95))


def default_features():
    """
    Fallback features for empty/noisy images.
    """
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
