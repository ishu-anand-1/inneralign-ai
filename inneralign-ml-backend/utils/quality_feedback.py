def quality_suggestions(quality):
    """
    Generate image quality improvement suggestions.

    ```
    Expected Input:
    {
        "score": 0.62,
        "blur": 0.45,
        "brightness": 0.30,
        "contrast": 0.55,
        "alignment": 0.40
    }
    ```
    """

    score = quality.get("score", 0)

    tips = []

    # -----------------------------------
    # Excellent Quality
    # -----------------------------------
    if score >= 0.85:
        return [
            "Image quality is excellent. No improvements are needed."
        ]

    # -----------------------------------
    # Blur Detection
    # -----------------------------------

    blur = quality.get("blur")

    if blur is not None and blur < 0.5:
        tips.append(
            "Capture the image with a steadier camera to reduce blur."
        )

    # -----------------------------------
    # Brightness Analysis
    # -----------------------------------

    brightness = quality.get("brightness")

    if brightness is not None:

        if brightness < 0.4:
            tips.append(
                "Increase lighting to make handwriting more visible."
            )

        elif brightness > 0.9:
            tips.append(
                "Reduce glare or excessive brightness while capturing the image."
            )

    # -----------------------------------
    # Contrast Analysis
    # -----------------------------------

    contrast = quality.get("contrast")

    if contrast is not None and contrast < 0.5:
        tips.append(
            "Use a darker pen or improve contrast between paper and ink."
        )

    # -----------------------------------
    # Alignment Analysis
    # -----------------------------------

    alignment = quality.get("alignment")

    if alignment is not None and alignment < 0.5:
        tips.append(
            "Keep the paper flat and align it straight before taking the photo."
        )

    # -----------------------------------
    # Additional Suggestions
    # -----------------------------------

    if score < 0.6:

        tips.append(
            "Fill most of the frame with the handwriting sample."
        )

        tips.append(
            "Avoid shadows covering any part of the writing."
        )

        tips.append(
            "Capture the image against a clean and uncluttered background."
        )

    # -----------------------------------
    # Fallback
    # -----------------------------------
    if not tips:
        tips.append(
            "Image quality is acceptable, though minor improvements may increase analysis accuracy."
        )
    return tips

