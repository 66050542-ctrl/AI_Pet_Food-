import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. โหลด Dataset
# ==========================================

df = pd.read_csv("pet_food_dataset.csv")

print("====================================")
print("AI PET FOOD - MODEL TRAINING")
print("====================================")

print("จำนวนข้อมูล:", len(df))
print("\nตัวอย่างข้อมูล:")
print(df.head())


# ==========================================
# 2. กำหนด Features และ Target
# ==========================================

features = [
    "pet_type",
    "breed",
    "age_years",
    "weight_kg",
    "health_issue",
    "activity_level",
    "budget_per_kg"
]

target = "nutrition_category"

X = df[features].copy()
y = df[target]


# ==========================================
# 3. แบ่งข้อมูล Train / Test
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:", len(X_train))
print("Testing data:", len(X_test))


# ==========================================
# 4. แยกประเภทข้อมูล
# ==========================================

categorical_features = [
    "pet_type",
    "breed",
    "health_issue",
    "activity_level"
]

numeric_features = [
    "age_years",
    "weight_kg",
    "budget_per_kg"
]


# ==========================================
# 5. One-Hot Encoding
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# ==========================================
# 6. สร้าง Random Forest
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42
)


# ==========================================
# 7. สร้าง Pipeline
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==========================================
# 8. Train Model
# ==========================================

print("\nกำลัง Train Model...")

pipeline.fit(X_train, y_train)


# ==========================================
# 9. ทำนาย
# ==========================================

y_pred = pipeline.predict(X_test)


# ==========================================
# 10. Accuracy
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n====================================")
print("MODEL PERFORMANCE")
print("====================================")

print("Accuracy:", accuracy)
print("Accuracy (%):", round(accuracy * 100, 2), "%")


# ==========================================
# 11. Classification Report
# ==========================================

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# ==========================================
# 12. บันทึก Model
# ==========================================

model_data = {
    "model": pipeline,
    "features": features,
    "target": target
}

joblib.dump(
    model_data,
    "pet_nutrition_model.pkl"
)


print("\n====================================")
print("SUCCESS!")
print("====================================")

print("สร้างไฟล์ pet_nutrition_model.pkl เรียบร้อยแล้ว")