def confidence_message(confidence):
    if confidence > 0.85:
        return "High confidence — handwriting signals are very consistent."
    elif confidence > 0.65:
        return "Moderate confidence — results are reasonably reliable."
    else:
        return "Low confidence — image quality may affect accuracy."
