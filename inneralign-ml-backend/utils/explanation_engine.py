def explain_feature(feature):
 """
  Returns a structured explanation for a handwriting feature.
 """


 name = feature.get("name", "Unknown Feature")

 try:
    value = float(
        feature.get(
            "numeric_value",
            feature.get("value", 0.5)
        )
    )
 except Exception:
    value = 0.5

 FEATURE_EXPLANATIONS = {
    "Baseline Consistency": {
        "high": {
            "title": "Stable Baseline",
            "description": "Your writing remains steady across the page."
        },
        "medium": {
            "title": "Moderately Stable Baseline",
            "description": "Your writing shows minor natural variation."
        },
        "low": {
            "title": "Variable Baseline",
            "description": "The writing baseline varies across the page."
        }
    },

    "Stroke Pressure": {
        "high": {
            "title": "Strong Pressure",
            "description": "The writing shows firm pressure and defined strokes."
        },
        "medium": {
            "title": "Balanced Pressure",
            "description": "Writing pressure appears balanced."
        },
        "low": {
            "title": "Light Pressure",
            "description": "The writing uses lighter pressure."
        }
    },

    "Letter Spacing": {
        "high": {
            "title": "Open Letter Spacing",
            "description": "Letters are spaced openly."
        },
        "medium": {
            "title": "Balanced Letter Spacing",
            "description": "Letter spacing appears balanced."
        },
        "low": {
            "title": "Compact Letter Spacing",
            "description": "Letters are positioned closely together."
        }
    },

    "Word Spacing": {
        "high": {
            "title": "Wide Word Spacing",
            "description": "Words are separated by generous spacing."
        },
        "medium": {
            "title": "Balanced Word Spacing",
            "description": "Word spacing appears natural."
        },
        "low": {
            "title": "Crowded Word Spacing",
            "description": "Words are positioned close together."
        }
    },

    "Slant Angle": {
        "high": {
            "title": "Forward Slant",
            "description": "The writing shows a noticeable forward slant."
        },
        "medium": {
            "title": "Moderate Slant",
            "description": "The writing maintains a moderate slant."
        },
        "low": {
            "title": "Upright Writing",
            "description": "The writing appears relatively upright."
        }
    },

    "X-Height Variation": {
        "high": {
            "title": "Variable Letter Height",
            "description": "Letter height varies noticeably."
        },
        "medium": {
            "title": "Moderately Consistent Height",
            "description": "Letter heights remain fairly consistent."
        },
        "low": {
            "title": "Highly Consistent Height",
            "description": "Letter heights remain highly uniform."
        }
    },

    "Loop Openness": {
        "high": {
            "title": "Open Loops",
            "description": "Letter loops appear open and clear."
        },
        "medium": {
            "title": "Moderate Loops",
            "description": "Letter loops show moderate openness."
        },
        "low": {
            "title": "Compact Loops",
            "description": "Letter loops appear compact."
        }
    },

    "Writing Speed": {
        "high": {
            "title": "Fast Writing Flow",
            "description": "Writing appears relatively quick and fluid."
        },
        "medium": {
            "title": "Moderate Writing Flow",
            "description": "Writing speed appears balanced."
        },
        "low": {
            "title": "Deliberate Writing Flow",
            "description": "Writing appears slower and more deliberate."
        }
    }
 }

 if value >= 0.75:
    level = "High"
    key = "high"
 elif value >= 0.45:
    level = "Medium"
    key = "medium"
 else:
    level = "Low"
    key = "low"

 if name not in FEATURE_EXPLANATIONS:
    return {
        "name": name,
        "score": round(value * 100, 1),
        "level": level,
        "title": "Feature Analysis",
        "description": feature.get(
            "interpretation",
            "No explanation available."
        )
    }

 explanation = FEATURE_EXPLANATIONS[name][key]

 return {
    "name": name,
    "score": round(value * 100, 1),
    "level": level,
    "title": explanation["title"],
    "description": explanation["description"]
 }



def explain_feature_simple(feature):
    result = explain_feature(feature)

    return result.get(
        "description",
        "No explanation available."
    )
def explain_feature_simple(feature):
    explanation = explain_feature(feature)

    return explanation["description"]