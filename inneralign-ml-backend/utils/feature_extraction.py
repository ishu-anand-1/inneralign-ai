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

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contours, _ = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    min_area = max(40, (h * w) // 15000)
    contours = [c for c in contours if cv2.contourArea(c) > min_area]

    # 🚨 HARD STOP IF NO HANDWRITING
    if len(contours) < 3:
        return []   # ⛔ NO DEFAULT FEATURES

    areas = np.array([cv2.contourArea(c) for c in contours])
    boxes = [cv2.boundingRect(c) for c in contours]

    xs = np.array([x for (x, _, _, _) in boxes])
    ys = np.array([y for (_, y, _, _) in boxes])
    widths = np.array([bw for (_, _, bw, _) in boxes])
    heights = np.array([bh for (_, _, _, bh) in boxes])

    stroke_pressure = np.clip(np.mean(areas) / 2400, 0, 1)
    baseline_consistency = np.clip(1 - np.std(ys) / h, 0, 1)
    letter_spacing = np.clip(np.std(xs) / w, 0, 1)
    word_spacing = np.clip(letter_spacing * 1.3, 0, 1)
    x_height_var = np.clip(np.std(heights) / h, 0, 1)
    loop_openness = np.clip(np.mean(areas) / 2800, 0, 1)
    speed = np.clip(len(contours) / (w * h / 5000), 0, 1)

    slant_angle = 90 - np.degrees(np.arctan2(
        np.median(heights),
        np.median(widths)
    ))
    slant_angle = np.clip(slant_angle, 60, 120)
    slant_norm = np.clip((slant_angle - 60) / 60, 0, 1)

    return [
        make_feature("Slant Angle", f"{slant_angle:.1f}°", slant_norm,
                     "Forward-leaning" if slant_angle < 88 else "Upright"),
        make_feature("Baseline Consistency", baseline_consistency,
                     baseline_consistency, "Stable"),
        make_feature("Stroke Pressure", stroke_pressure,
                     stroke_pressure, "Heavy"),
        make_feature("Letter Spacing", letter_spacing,
                     letter_spacing, "Balanced"),
        make_feature("Word Spacing", word_spacing,
                     word_spacing, "Clear"),
        make_feature("X-Height Variation", x_height_var,
                     x_height_var, "Consistent"),
        make_feature("Loop Openness", loop_openness,
                     loop_openness, "Open"),
        make_feature("Writing Speed", speed,
                     speed, "Moderate"),
    ]


def make_feature(name, value, numeric, interpretation):
    confidence = np.clip(0.55 + numeric * 0.35, 0.55, 0.9)
    return {
        "name": name,
        "value": value,
        "numeric_value": round(float(numeric), 3),
        "interpretation": interpretation,
        "confidence": int(confidence * 100),
    }
