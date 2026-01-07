import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)
import joblib

# --------------------------------
# LOAD DATA
# --------------------------------
df = pd.read_csv("handwriting_features.csv")

feature_cols = [
    "Slant", "Baseline", "Pressure",
    "LetterSpacing", "WordSpacing",
    "XHeight", "LoopOpen", "Speed"
]

X = df[feature_cols]
y = df["EmotionLabel"]

# --------------------------------
# TRAIN / TEST SPLIT
# --------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# --------------------------------
# TRAIN MODEL
# --------------------------------
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------
# PREDICTION
# --------------------------------
y_pred = model.predict(X_test)

# --------------------------------
# MODEL EVALUATION
# --------------------------------
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
conf_matrix = confusion_matrix(y_test, y_pred)

print("\n📊 MODEL EVALUATION RESULTS")
print("----------------------------")
print(f"Accuracy : {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall   : {recall:.2f}")

print("\nConfusion Matrix:")
print(conf_matrix)

print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred))

# --------------------------------
# SAVE MODEL
# --------------------------------
joblib.dump(model, "rf_handwriting_emotion.pkl")

print("\n✅ Model trained & saved successfully")
