import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


# ==========================================
# 1. โหลดประวัติการวิเคราะห์
# ==========================================

file = "recommendation_history.csv"

df = pd.read_csv(
    file,
    encoding="utf-8-sig"
)

print("\n========================================")
print("       AI PET FOOD DASHBOARD")
print("========================================")


# ==========================================
# 2. ข้อมูลพื้นฐาน
# ==========================================

print("\nจำนวนการวิเคราะห์ทั้งหมด :", len(df))

if "ประเภทสัตว์" in df.columns:
    print("\nประเภทสัตว์")
    print(df["ประเภทสัตว์"].value_counts())


# ==========================================
# 3. กราฟจำนวนสัตว์
# ==========================================

if "ประเภทสัตว์" in df.columns:

    plt.figure(figsize=(8, 5))

    df["ประเภทสัตว์"].value_counts().plot(
        kind="bar"
    )

    plt.title("Number of Pets Analyzed")
    plt.xlabel("Pet Type")
    plt.ylabel("Number")

    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.show()


# ==========================================
# 4. กราฟปัญหาสุขภาพ
# ==========================================

if "ปัญหาสุขภาพ" in df.columns:

    plt.figure(figsize=(8, 5))

    df["ปัญหาสุขภาพ"].value_counts().plot(
        kind="bar"
    )

    plt.title("Common Health Problems")
    plt.xlabel("Health Problem")
    plt.ylabel("Number")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# ==========================================
# 5. กราฟงบประมาณ
# ==========================================

if "งบประมาณ" in df.columns:

    plt.figure(figsize=(8, 5))

    df["งบประมาณ"].plot(
        kind="hist",
        bins=10
    )

    plt.title("Budget Distribution")
    plt.xlabel("Budget (Baht/kg)")
    plt.ylabel("Number of Analysis")

    plt.tight_layout()
    plt.show()


# ==========================================
# 6. อาหารที่แนะนำบ่อยที่สุด
# ==========================================

food_counter = Counter()

if "อาหารที่แนะนำ" in df.columns:

    for foods in df["อาหารที่แนะนำ"].dropna():

        foods = str(foods)

        for food in foods.split(";"):

            food = food.strip()

            if food:
                food_counter[food] += 1


# ==========================================
# 7. แสดงอันดับอาหาร
# ==========================================

print("\n========================================")
print("       MOST RECOMMENDED FOODS")
print("========================================")

if food_counter:

    for i, (food, count) in enumerate(
        food_counter.most_common(),
        start=1
    ):

        print(
            f"{i}. {food} → {count} ครั้ง"
        )


# ==========================================
# 8. กราฟอาหารที่แนะนำ
# ==========================================

if food_counter:

    food_data = pd.Series(
        dict(food_counter.most_common())
    )

    plt.figure(figsize=(10, 6))

    food_data.plot(
        kind="bar"
    )

    plt.title(
        "Most Recommended Pet Foods"
    )

    plt.xlabel("Pet Food")

    plt.ylabel(
        "Number of Recommendations"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    plt.show()


# ==========================================
# 9. สรุป Dashboard
# ==========================================

print("\n========================================")
print("             SUMMARY")
print("========================================")

print(
    f"จำนวนการวิเคราะห์ทั้งหมด: {len(df)} ครั้ง"
)

if "ประเภทสัตว์" in df.columns:

    pet_count = df["ประเภทสัตว์"].value_counts()

    print(
        f"สัตว์ที่วิเคราะห์มากที่สุด: "
        f"{pet_count.idxmax()}"
    )

if "ปัญหาสุขภาพ" in df.columns:

    health_count = df[
        "ปัญหาสุขภาพ"
    ].value_counts()

    print(
        f"ปัญหาสุขภาพที่พบบ่อยที่สุด: "
        f"{health_count.idxmax()}"
    )

if food_counter:

    top_food = food_counter.most_common(1)[0]

    print(
        f"อาหารที่ถูกแนะนำมากที่สุด: "
        f"{top_food[0]}"
    )

print("\n========================================")
print("          DASHBOARD COMPLETE")
print("========================================")