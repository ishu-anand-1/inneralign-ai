import numpy as np

def assess_quality(img):
    non_zero = np.count_nonzero(img)
    density = non_zero / img.size

    score = min(1.0, max(0.6, density + 0.2))

    issues = []
    if density < 0.2:
        issues.append("Low ink density detected")
    else:
        issues.append("Minor rotation detected (<3°)")

    return {
        "score": score,
        "issues": issues
    }

# ----------------- QUALITY SUGGESTIONS -----------------
def quality_suggestions(quality):
    tips = []

    if quality["score"] < 0.7:
        tips.append("Use a darker pen for clearer strokes.")
        tips.append("Ensure even lighting while capturing the image.")
        tips.append("Keep the paper flat and straight.")
    else:
        tips.append("Image quality is good. No improvement needed.")

    return tips
