import pandas as pd
import joblib


# ==========================================
# 1. โหลด Model
# ==========================================

model_data = joblib.load("pet_nutrition_model.pkl")
model = model_data["model"]


# ==========================================
# 2. โหลดฐานข้อมูลอาหาร
# ==========================================

food_df = pd.read_csv("food_database.csv")


# ==========================================
# 3. ฟังก์ชันแนะนำอาหาร
# ==========================================

def recommend_food(
    pet_type,
    breed,
    age_years,
    weight_kg,
    health_issue,
    activity_level,
    budget_per_kg
):

    pet_data = pd.DataFrame([{
        "pet_type": pet_type,
        "breed": breed,
        "age_years": age_years,
        "weight_kg": weight_kg,
        "health_issue": health_issue,
        "activity_level": activity_level,
        "budget_per_kg": budget_per_kg
    }])


    # ======================================
    # ML Prediction
    # ======================================

    prediction = model.predict(pet_data)[0]

    probabilities = model.predict_proba(pet_data)[0]

    confidence = max(probabilities) * 100


    # ======================================
    # แสดงข้อมูล
    # ======================================

    print("\n========================================")
    print("       AI PET FOOD RECOMMENDATION")
    print("========================================")

    print(f"Pet Type       : {pet_type}")
    print(f"Breed          : {breed}")
    print(f"Age            : {age_years} years")
    print(f"Weight         : {weight_kg} kg")
    print(f"Health Issue   : {health_issue}")
    print(f"Activity Level : {activity_level}")
    print(f"Budget         : {budget_per_kg} Baht/kg")


    # ======================================
    # ผล ML
    # ======================================

    print("\n----------------------------------------")
    print("AI NUTRITION ANALYSIS")
    print("----------------------------------------")

    print(f"Nutrition Category : {prediction}")
    print(f"Confidence         : {confidence:.2f}%")


    # ======================================
    # เตรียมฐานข้อมูล
    # ======================================

    food_df["pet_type"] = (
        food_df["pet_type"]
        .astype(str)
        .str.strip()
    )

    food_df["nutrition_category"] = (
        food_df["nutrition_category"]
        .astype(str)
        .str.strip()
    )

    food_df["price_per_kg"] = pd.to_numeric(
        food_df["price_per_kg"],
        errors="coerce"
    )


    # ======================================
    # กรองอาหาร
    # ======================================

    result = food_df[
        (food_df["pet_type"].str.lower()
         == str(pet_type).strip().lower())
        &
        (food_df["nutrition_category"].str.lower()
         == str(prediction).strip().lower())
        &
        (food_df["price_per_kg"]
         <= budget_per_kg)
    ].copy()


    print("\n----------------------------------------")
    print("FOOD DATABASE CHECK")
    print("----------------------------------------")

    print(f"Pet Type          : {pet_type}")
    print(f"Prediction        : {prediction}")
    print(f"Budget            : {budget_per_kg} Baht/kg")
    print(f"จำนวนอาหารที่พบ   : {len(result)}")


    # ======================================
    # Recommendation Score
    # ======================================

    if len(result) > 0:

        result["score"] = 70

        result["budget_score"] = (
            (budget_per_kg - result["price_per_kg"])
            / budget_per_kg
        ) * 15

        result["grade_score"] = (
            result["grade"]
            .map({
                "Standard": 5,
                "Premium": 10,
                "Holistic": 15
            })
            .fillna(0)
        )

        result["protein_score"] = (
            result["protein_percent"]
            .apply(
                lambda x: 5 if x >= 25 else 3
            )
        )

        result["score"] = (
            result["score"]
            + result["budget_score"]
            + result["grade_score"]
            + result["protein_score"]
        )

        result["score"] = result["score"].clip(
            upper=100
        )

        result = result.sort_values(
            by="score",
            ascending=False
        )


    # ======================================
    # Smart Recommendation
    # ======================================

    print("\n========================================")
    print("       SMART RECOMMENDATION")
    print("========================================")

    recommended_foods = []


    if len(result) == 0:

        print("\nไม่พบอาหารที่ตรงกับเงื่อนไข")

        same_category = food_df[
            food_df["nutrition_category"].str.lower()
            == str(prediction).strip().lower()
        ]

        print(
            f"\nจำนวนอาหารในหมวด {prediction}: "
            f"{len(same_category)}"
        )

        if len(same_category) > 0:

            print("\nอาหารในหมวดนี้:")

            for row in same_category.head(10).itertuples():

                print(
                    f"- {row.brand} - {row.formula}"
                    f" | {row.price_per_kg} บาท/kg"
                    f" | {row.pet_type}"
                )


    else:

        top3 = result.head(3)

        for index, row in enumerate(
            top3.itertuples(),
            start=1
        ):

            food_name = (
                f"{row.brand} - {row.formula}"
            )

            recommended_foods.append(
                food_name
            )

            print(f"\nอันดับ {index}")

            print(f"Brand   : {row.brand}")
            print(f"Formula : {row.formula}")
            print(
                f"Price   : "
                f"{row.price_per_kg} Baht/kg"
            )
            print(f"Grade   : {row.grade}")
            print(
                f"Protein : "
                f"{row.protein_percent}%"
            )
            print(
                f"Fat     : "
                f"{row.fat_percent}%"
            )
            print(
                f"Score   : "
                f"{row.score:.2f}/100"
            )

            print("เหตุผล:")
            print(
                "✓ ตรงกับประเภทโภชนาการที่ ML ทำนาย"
            )
            print("✓ อยู่ในงบประมาณ")


    # ======================================
    # Feeding Guide
    # ======================================

    print("\n========================================")
    print("          FEEDING GUIDE")
    print("========================================")

    feeding_min = weight_kg * 10
    feeding_max = weight_kg * 11

    print(
        f"น้ำหนักสัตว์ : "
        f"{weight_kg} kg"
    )

    print(
        f"ปริมาณอาหารโดยประมาณ : "
        f"{feeding_min:.0f}-"
        f"{feeding_max:.0f} g/day"
    )


    # ======================================
    # AI Advice
    # ======================================

    print("\n========================================")
    print("             AI ADVICE")
    print("========================================")

    if prediction == "Joint Care":

        print(
            "✓ ควรพิจารณาอาหารในกลุ่ม Joint Care"
        )

    elif prediction == "Weight Control":

        print(
            "✓ ควรพิจารณาอาหารในกลุ่ม Weight Control"
        )

    elif prediction == "Sensitive Skin":

        print(
            "✓ ควรพิจารณาอาหารในกลุ่ม Sensitive Skin"
        )

    elif prediction == "Senior Formula":

        print(
            "✓ ควรพิจารณาอาหารในกลุ่ม Senior Formula"
        )

    else:

        print(
            "✓ ควรเลือกอาหารให้เหมาะกับวัยและกิจกรรม"
        )


    # ======================================
    # ส่งข้อมูลกลับ API / Tool
    # ======================================

    return {
        "prediction": prediction,
        "confidence": confidence,
        "recommended_foods": recommended_foods
    }


# ==========================================
# ทดสอบจาก Terminal
# ==========================================

if __name__ == "__main__":

    print("\n========================================")
    print("       AI PET FOOD SYSTEM")
    print("========================================")

    pet_type = input(
        "ประเภทสัตว์ (Dog/Cat): "
    )

    breed = input(
        "สายพันธุ์: "
    )

    age_years = float(
        input("อายุ (ปี): ")
    )

    weight_kg = float(
        input("น้ำหนัก (kg): ")
    )

    health_issue = input(
        "ปัญหาสุขภาพ: "
    )

    activity_level = input(
        "ระดับกิจกรรม (Low/Medium/High): "
    )

    budget_per_kg = float(
        input("งบประมาณ (บาท/kg): ")
    )

    recommend_food(
        pet_type=pet_type,
        breed=breed,
        age_years=age_years,
        weight_kg=weight_kg,
        health_issue=health_issue,
        activity_level=activity_level,
        budget_per_kg=budget_per_kg
    )