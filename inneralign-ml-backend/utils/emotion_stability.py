from functools import wraps
from statistics import mean, median, stdev
from time import perf_counter

import numpy as np

# =====================================================

# PERFORMANCE DECORATOR

# =====================================================

def measure_time(func):


 @wraps(func)
 def wrapper(*args, **kwargs):

    start = perf_counter()

    result = func(*args, **kwargs)

    result["execution_ms"] = round(
        (perf_counter() - start) * 1000,
        2
    )

    return result

 return wrapper


# =====================================================

# FEATURE WEIGHTS

# =====================================================

FEATURE_WEIGHTS = {
"Baseline Consistency": 1.5,
"Slant Angle": 1.2,
"Stroke Pressure": 1.4,
"Letter Spacing": 1.3,
"Word Spacing": 1.1,
"Writing Speed": 1.0,
"Loop Openness": 1.0,
"X-Height Variation": 1.2,
}


def safe_float(value):


 try:

    if isinstance(value, str):

        value = (
            value.replace("°", "")
            .replace("%", "")
            .strip()
        )

    return float(value)

 except Exception:

    return None


def remove_outliers(values):


 if len(values) < 4:
    return values

 arr = np.array(values)

 q1 = np.percentile(arr, 25)
 q3 = np.percentile(arr, 75)

 iqr = q3 - q1

 lower = q1 - (1.5 * iqr)
 upper = q3 + (1.5 * iqr)

 filtered = arr[
    (arr >= lower)
    & (arr <= upper)
 ]

 return filtered.tolist()

def stability_label(score):


 if score >= 0.85:
    return "Very High"

 elif score >= 0.70:
    return "High"

 elif score >= 0.50:
    return "Moderate"

 elif score >= 0.30:
    return "Low"

 return "Very Low"


# =====================================================

# MAIN ANALYSIS

# =====================================================

@measure_time
def emotion_stability(features):


 weighted_values = []

 for feature in features:

    feature_name = feature.get(
        "name",
        ""
    )

    value = safe_float(
        feature.get(
            "numeric_value"
        )
    )

    if value is None:
        continue

    weight = FEATURE_WEIGHTS.get(
        feature_name,
        1.0
    )

    weighted_values.append(
        value * weight
    )

 if len(weighted_values) < 3:

    return {
        "score": 0.20,
        "confidence": 0.10,
        "label": "Low",
        "message":
            "Insufficient handwriting data "
            "for stability analysis."
    }

 cleaned = remove_outliers(
    weighted_values
 )

 if len(cleaned) < 3:
    cleaned = weighted_values

 avg = mean(cleaned)

 med = median(cleaned)

 sd = (
    stdev(cleaned)
    if len(cleaned) > 1
    else 0
 )

 cv = (
    sd / avg
    if avg != 0
    else 1
 )

 stability_score = round(
    max(
        0,
        min(
            1,
            1 - cv
        )
    ),
    3
 )

 confidence = round(
    min(
        1.0,
        len(cleaned) / 8
    ),
    3
 )

 label = stability_label(
    stability_score
 )

 if stability_score >= 0.85:

    message = (
        "Handwriting features appear highly "
        "consistent across the sample."
    )

 elif stability_score >= 0.70:

    message = (
        "Handwriting shows strong stability "
        "with only minor variation."
    )

 elif stability_score >= 0.50:

    message = (
        "Moderate variation detected "
        "between handwriting features."
    )

 elif stability_score >= 0.30:

    message = (
        "Noticeable variation detected. "
        "Interpret results cautiously."
    )

 else:

    message = (
        "Significant variability detected. "
        "Confidence in stability assessment "
        "is limited."
    )

 return {

    "score": stability_score,

    "confidence": confidence,

    "label": label,

    "mean": round(avg, 3),

    "median": round(med, 3),

    "std_dev": round(sd, 3),

    "coefficient_variation":
        round(cv, 3),

    "samples_used":
        len(cleaned),

    "message":
        message
 }

