import pandas as pd
import joblib


# ==========================================
# 1. โหลด Model
# ==========================================

model_data = joblib.load("pet_nutrition_model.pkl")

model = model_data["model"]


# ==========================================
# 2. ฟังก์ชันทำนาย
# ==========================================

def predict_nutrition(
    pet_type,
    breed,
    age_years,
    weight_kg,
    health_issue,
    activity_level,
    budget_per_kg
):

    data = pd.DataFrame([{
        "pet_type": pet_type,
        "breed": breed,
        "age_years": age_years,
        "weight_kg": weight_kg,
        "health_issue": health_issue,
        "activity_level": activity_level,
        "budget_per_kg": budget_per_kg
    }])


    # ==========================================
    # ทำนาย
    # ==========================================

    prediction = model.predict(data)[0]

    probabilities = model.predict_proba(data)[0]

    confidence = max(probabilities) * 100


    # ==========================================
    # แสดงผล
    # ==========================================

    print("\n====================================")
    print("       AI PET FOOD PREDICTION")
    print("====================================")

    print(f"Pet Type       : {pet_type}")
    print(f"Breed          : {breed}")
    print(f"Age            : {age_years} years")
    print(f"Weight         : {weight_kg} kg")
    print(f"Health Issue   : {health_issue}")
    print(f"Activity Level : {activity_level}")
    print(f"Budget         : {budget_per_kg} Baht/kg")

    print("------------------------------------")
    print("AI RESULT")
    print("------------------------------------")

    print(f"Nutrition Category : {prediction}")
    print(f"Confidence         : {confidence:.2f}%")

    print("====================================")


# ==========================================
# 3. Demo Case
# ==========================================

predict_nutrition(
    pet_type="Dog",
    breed="Golden Retriever",
    age_years=6,
    weight_kg=32,
    health_issue="Joint Problem",
    activity_level="Medium",
    budget_per_kg=200
)