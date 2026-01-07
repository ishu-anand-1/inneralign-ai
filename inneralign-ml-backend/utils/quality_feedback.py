def quality_suggestions(quality):
    tips = []

    if quality["score"] < 0.7:
        tips.append("Use a darker pen for clearer strokes.")
        tips.append("Ensure even lighting while capturing the image.")
        tips.append("Keep the paper flat and straight.")
    else:
        tips.append("Image quality is good. No improvement needed.")

    return tips
