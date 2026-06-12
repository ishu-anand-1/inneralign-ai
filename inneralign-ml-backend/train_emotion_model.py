import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

# =====================================================

# CONFIG

# =====================================================

FEATURE_COLUMNS = [
"Slant",
"Baseline",
"Pressure",
"LetterSpacing",
"WordSpacing",
"XHeight",
"LoopOpen",
"Speed"
]

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
MODEL_DIR,
"rf_handwriting_emotion.pkl"
)

SCALER_PATH = os.path.join(
MODEL_DIR,
"feature_scaler.pkl"
)

os.makedirs(MODEL_DIR, exist_ok=True)

# =====================================================

# LOAD DATA

# =====================================================

df = pd.read_csv("handwriting_features.csv")

print("\nDataset Shape:")
print(df.shape)

print("\nEmotion Distribution:")
print(df["EmotionLabel"].value_counts())

missing_cols = [
col for col in FEATURE_COLUMNS
if col not in df.columns
]

if missing_cols:
 raise ValueError(
f"Missing columns: {missing_cols}"
)

if "EmotionLabel" not in df.columns:
 raise ValueError(
"EmotionLabel column not found"
)

X = df[FEATURE_COLUMNS]
y = df["EmotionLabel"]


scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)


model = RandomForestClassifier(
n_estimators=200,
max_depth=8,
class_weight="balanced",
random_state=42,
n_jobs=-1
)

print("\nTraining model...")

model.fit(X_scaled, y)

print("\nFeature Importance:")

importance_pairs = sorted(
zip(
FEATURE_COLUMNS,
model.feature_importances_
),
key=lambda x: x[1],
reverse=True
)

for feature, score in importance_pairs:


 print(
    f"{feature:<15} : {score:.4f}"
)


joblib.dump(
model,
MODEL_PATH
)

joblib.dump(
scaler,
SCALER_PATH
)

print("\n✅ Model Saved")
print(MODEL_PATH)

print("\n✅ Scaler Saved")
print(SCALER_PATH)

print("\n🎉 Training Complete")
