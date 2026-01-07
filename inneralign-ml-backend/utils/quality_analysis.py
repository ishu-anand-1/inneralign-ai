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
