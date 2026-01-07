import cv2
import numpy as np

def extract_features(img):
    h, w = img.shape

    contours, _ = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    contours = [c for c in contours if cv2.contourArea(c) > 40]

    if not contours:
        return default_features()

    areas = np.array([cv2.contourArea(c) for c in contours])
    bounding_boxes = [cv2.boundingRect(c) for c in contours]

    # -----------------------------
    # FEATURE CALCULATIONS (REAL)
    # -----------------------------

    # Stroke Pressure (ink density proxy)
    stroke_pressure = np.clip(np.mean(areas) / 2000, 0, 1)

    # Baseline variation
    baseline_positions = [y for (_, y, _, _) in bounding_boxes]
    baseline_variation = np.std(baseline_positions) / h
    baseline_consistency = np.clip(1 - baseline_variation, 0, 1)

    # Letter spacing
    x_positions = [x for (x, _, _, _) in bounding_boxes]
    letter_spacing = np.clip(np.std(x_positions) / w, 0, 1)

    # Word spacing
    word_spacing = np.clip(letter_spacing * 1.5, 0, 1)

    # X-height variation
    heights = [bh for (_, _, _, bh) in bounding_boxes]
    x_height_var = np.clip(np.std(heights) / h, 0, 1)

    # Loop openness
    loop_openness = np.clip(np.mean(areas) / 2500, 0, 1)

    # Writing speed proxy
    speed_proxy = np.clip(len(contours) / 900, 0, 1)

    # Slant angle (derived, not random)
    slant_angle = 90 - np.degrees(np.arctan2(
        np.mean([bh for (_, _, _, bh) in bounding_boxes]),
        np.mean([bw for (_, _, bw, _) in bounding_boxes])
    ))
    slant_angle = np.clip(slant_angle, 60, 120)

    # -----------------------------
    # RETURN STRUCTURED FEATURES
    # -----------------------------

    return [
        feature(
            "Slant Angle",
            f"{slant_angle:.1f}°",
            "Forward-leaning writing" if slant_angle < 90 else "Upright writing",
            confidence_from_value(abs(90 - slant_angle) / 30)
        ),
        feature(
            "Baseline Consistency",
            round(baseline_consistency, 2),
            "Stable baseline" if baseline_consistency > 0.6 else "Fluctuating baseline",
            confidence_from_value(baseline_consistency)
        ),
        feature(
            "Stroke Pressure",
            round(stroke_pressure, 2),
            "Heavy pressure" if stroke_pressure > 0.6 else "Light to moderate pressure",
            confidence_from_value(stroke_pressure)
        ),
        feature(
            "Letter Spacing",
            round(letter_spacing, 2),
            "Balanced spacing" if 0.3 < letter_spacing < 0.7 else "Irregular spacing",
            confidence_from_value(1 - abs(letter_spacing - 0.5))
        ),
        feature(
            "Word Spacing",
            round(word_spacing, 2),
            "Clear word separation" if word_spacing > 0.4 else "Crowded words",
            confidence_from_value(word_spacing)
        ),
        feature(
            "X-Height Variation",
            round(x_height_var, 2),
            "Consistent letter height" if x_height_var < 0.4 else "Variable letter height",
            confidence_from_value(1 - x_height_var)
        ),
        feature(
            "Loop Openness",
            round(loop_openness, 2),
            "Open loops" if loop_openness > 0.5 else "Closed loops",
            confidence_from_value(loop_openness)
        ),
        feature(
            "Writing Speed Proxy",
            round(speed_proxy, 2),
            "Fast writing" if speed_proxy > 0.6 else "Moderate writing speed",
            confidence_from_value(speed_proxy)
        ),
    ]


def feature(name, value, interpretation, confidence):
    return {
        "name": name,
        "value": value,
        "interpretation": interpretation,
        "confidence": int(confidence * 100)
    }


def confidence_from_value(v):
    return float(np.clip(v, 0.5, 0.98))


def default_features():
    return [
        feature("Slant Angle", "90°", "Insufficient data", 50),
        feature("Baseline Consistency", 0.5, "Insufficient data", 50),
        feature("Stroke Pressure", 0.5, "Insufficient data", 50),
        feature("Letter Spacing", 0.5, "Insufficient data", 50),
        feature("Word Spacing", 0.5, "Insufficient data", 50),
        feature("X-Height Variation", 0.5, "Insufficient data", 50),
        feature("Loop Openness", 0.5, "Insufficient data", 50),
        feature("Writing Speed Proxy", 0.5, "Insufficient data", 50),
    ]
