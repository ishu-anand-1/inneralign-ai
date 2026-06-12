def confidence_message(confidence: float) -> str:
    """
    Generate human-friendly confidence interpretation.

    confidence: value between 0 and 1
    """

    if confidence >= 0.90:
        return (
            "Very high confidence — handwriting patterns are highly "
            "consistent and strongly support this prediction."
        )

    elif confidence >= 0.75:
        return (
            "High confidence — handwriting signals are consistent "
            "and the prediction appears reliable."
        )

    elif confidence >= 0.60:
        return (
            "Moderate confidence — most handwriting indicators align "
            "with this prediction, though some uncertainty remains."
        )

    elif confidence >= 0.40:
        return (
            "Low confidence — multiple emotional categories show "
            "similar probabilities. Interpret results cautiously."
        )

    elif confidence >= 0.20:
        return (
            "Very low confidence — handwriting features provide "
            "limited evidence for a clear prediction."
        )

    return (
        "Insufficient confidence — image quality, handwriting clarity, "
        "or feature extraction issues may affect accuracy."
    )