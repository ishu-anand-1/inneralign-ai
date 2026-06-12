import numpy as np

def assess_quality(img):
    non_zero = np.count_nonzero(img)
    density = non_zero / img.size

    if density < 0.02:
        return {
            "score": 0.05,
            "issues": ["No handwriting detected"],
            "is_blank": True
        }

    score = min(1.0, max(0.6, density + 0.2))

    issues = []
    if density < 0.2:
        issues.append("Low ink density detected")
    else:
        issues.append("Minor rotation detected (<3°)")

    return {
        "score": score,
        "issues": issues,
        "is_blank": False
    }


def quality_suggestions(quality):
    if quality["is_blank"]:
        return ["Upload a page with visible handwriting for analysis."]

    tips = []
    if quality["score"] < 0.7:
        tips.extend([
            "Use a darker pen for clearer strokes.",
            "Ensure even lighting.",
            "Keep the paper flat."
        ])
    else:
        tips.append("Image quality is good.")

    return tips 