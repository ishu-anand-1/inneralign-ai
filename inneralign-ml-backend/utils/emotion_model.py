import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Dummy training data (replace later with real dataset)
X_train = np.array([
    [0.2, 0.3, 0.4, 0.5, 0.2, 0.3, 0.4],  # calm
    [0.6, 0.8, 0.1, 0.2, 0.5, 0.6, 0.7],  # stressed
    [0.3, 0.4, 0.5, 0.6, 0.3, 0.4, 0.3],  # happy
])

y_train = ["Calm", "Stressed", "Happy"]

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

def predict_emotion(feature_vector):
    probs = model.predict_proba([feature_vector])[0]
    label = model.classes_[np.argmax(probs)]
    confidence = float(np.max(probs))

    return label, confidence
