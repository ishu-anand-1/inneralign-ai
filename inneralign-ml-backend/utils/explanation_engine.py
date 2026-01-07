def explain_feature_simple(feature):
    name = feature["name"]
    value = feature["value"]

    explanations = {
        "Baseline Consistency": {
            "high": "Your writing stays steady across the page, suggesting emotional balance.",
            "medium": "Your writing shows minor variation, which is common.",
            "low": "Your writing fluctuates, possibly reflecting emotional shifts."
        },
        "Stroke Pressure": {
            "high": "You press firmly while writing, often linked to strong emotions.",
            "medium": "Your writing pressure appears balanced.",
            "low": "You write lightly, which may suggest low energy or sensitivity."
        },
        "Letter Spacing": {
            "high": "Your writing feels open and relaxed.",
            "medium": "Your spacing is balanced and readable.",
            "low": "Tight spacing may indicate tension or nervousness."
        }
    }

    if name not in explanations:
        return feature["interpretation"]

    if value > 0.7:
        return explanations[name]["high"]
    elif value > 0.4:
        return explanations[name]["medium"]
    else:
        return explanations[name]["low"]
