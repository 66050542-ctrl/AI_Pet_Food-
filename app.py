import tkinter as tk
from tkinter import ttk, messagebox
import recommend
import io
import contextlib
import csv
import os
from datetime import datetime


# ==========================================
# บันทึกประวัติการวิเคราะห์
# ==========================================

def save_history(pet_type, breed, age, weight, health, activity, budget, recommended_foods):
    file_exists = os.path.exists("recommendation_history.csv")

    food_text = "; ".join(recommended_foods)

    with open(
        "recommendation_history.csv",
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "วันที่วิเคราะห์",
                "ประเภทสัตว์",
                "สายพันธุ์",
                "อายุ",
                "น้ำหนัก",
                "ปัญหาสุขภาพ",
                "ระดับกิจกรรม",
                "งบประมาณ",
                "อาหารที่แนะนำ"
            ])

        writer.writerow([
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            pet_type,
            breed,
            age,
            weight,
            health,
            activity,
            budget,
            food_text
        ])

# ==========================================
# ล้างข้อมูล
# ==========================================

def reset_form():

    pet_type_var.set("Dog")
    breed_var.set("")
    age_var.set("")
    weight_var.set("")
    health_var.set("")
    activity_var.set("Medium")
    budget_var.set("")

    result_text.delete(
        "1.0",
        tk.END
    )


# ==========================================
# ปิดโปรแกรม
# ==========================================

def exit_app():

    root.destroy()


# ==========================================
# วิเคราะห์ AI
# ==========================================

def run_ai():

    # ------------------------------
    # ตรวจสอบข้อมูล
    # ------------------------------

    if breed_var.get().strip() == "":
        messagebox.showwarning(
            "ข้อมูลไม่ครบ",
            "กรุณากรอกสายพันธุ์"
        )
        return

    if age_var.get().strip() == "":
        messagebox.showwarning(
            "ข้อมูลไม่ครบ",
            "กรุณากรอกอายุ"
        )
        return

    if weight_var.get().strip() == "":
        messagebox.showwarning(
            "ข้อมูลไม่ครบ",
            "กรุณากรอกน้ำหนัก"
        )
        return

    if health_var.get().strip() == "":
        messagebox.showwarning(
            "ข้อมูลไม่ครบ",
            "กรุณากรอกปัญหาสุขภาพ"
        )
        return

    if budget_var.get().strip() == "":
        messagebox.showwarning(
            "ข้อมูลไม่ครบ",
            "กรุณากรอกงบประมาณ"
        )
        return


    # ------------------------------
    # แปลงตัวเลข
    # ------------------------------

    try:

        age = float(
            age_var.get()
        )

        weight = float(
            weight_var.get()
        )

        budget = float(
            budget_var.get()
        )

    except ValueError:

        messagebox.showerror(
            "ข้อมูลไม่ถูกต้อง",
            "อายุ น้ำหนัก และงบประมาณต้องเป็นตัวเลข"
        )

        return


    # ------------------------------
    # รับข้อมูล
    # ------------------------------

    pet_type = pet_type_var.get()
    breed = breed_var.get()
    health = health_var.get()
    activity = activity_var.get()


    # ------------------------------
    # เรียก AI
    # ------------------------------

    output = io.StringIO()

    try:

        with contextlib.redirect_stdout(output):

            result = recommend.recommend_food(
                pet_type=pet_type,
                breed=breed,
                age_years=age,
                weight_kg=weight,
                health_issue=health,
                activity_level=activity,
                budget_per_kg=budget
            )

    except Exception as e:

        messagebox.showerror(
            "เกิดข้อผิดพลาด",
            str(e)
        )

        return


    # ------------------------------
    # แสดงผล
    # ------------------------------

    result_text.delete(
        "1.0",
        tk.END
    )

    result_text.insert(
        tk.END,
        output.getvalue()
    )


    # ------------------------------
    # บันทึกประวัติ
    # ------------------------------

    try:

        recommended_foods = result.get(
            "recommended_foods",
            []
        )

        save_history(
    pet_type,
    breed,
    age,
    weight,
    health,
    activity,
    budget,
    recommended_foods
)

        result_text.insert(
            tk.END,
            "\n\n✅ บันทึกประวัติการวิเคราะห์แล้ว"
        )

    except Exception as e:

        messagebox.showwarning(
            "แจ้งเตือน",
            f"วิเคราะห์สำเร็จ แต่บันทึกประวัติไม่ได้\n{e}"
        )


# ==========================================
# สร้างหน้าต่าง
# ==========================================

root = tk.Tk()

root.title(
    "AI PET FOOD SYSTEM"
)

root.geometry(
    "900x700"
)

root.configure(
    bg="#F4F6F8"
)


# ==========================================
# Header
# ==========================================

header = tk.Frame(
    root,
    bg="#1F4E78",
    height=100
)

header.pack(
    fill="x"
)


title = tk.Label(
    header,
    text="🐾 AI PET FOOD SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#1F4E78",
    fg="white"
)

title.pack(
    pady=(20, 5)
)


subtitle = tk.Label(
    header,
    text="ระบบปัญญาประดิษฐ์สำหรับวิเคราะห์และแนะนำอาหารสัตว์เลี้ยง",
    font=("Arial", 11),
    bg="#1F4E78",
    fg="white"
)

subtitle.pack()


# ==========================================
# Input Frame
# ==========================================

input_frame = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)

input_frame.pack(
    fill="x",
    padx=25,
    pady=20
)


# ==========================================
# Variables
# ==========================================

pet_type_var = tk.StringVar(
    value="Dog"
)

breed_var = tk.StringVar()

age_var = tk.StringVar()

weight_var = tk.StringVar()

health_var = tk.StringVar()

activity_var = tk.StringVar(
    value="Medium"
)

budget_var = tk.StringVar()


# ==========================================
# Input helper
# ==========================================

def add_label(
    text,
    row
):

    label = tk.Label(
        input_frame,
        text=text,
        font=("Arial", 10, "bold"),
        bg="white"
    )

    label.grid(
        row=row,
        column=0,
        padx=15,
        pady=7,
        sticky="w"
    )


# ==========================================
# Inputs
# ==========================================

add_label(
    "ประเภทสัตว์",
    0
)

pet_type_box = ttk.Combobox(
    input_frame,
    textvariable=pet_type_var,
    values=["Dog", "Cat"],
    state="readonly",
    width=30
)

pet_type_box.grid(
    row=0,
    column=1,
    padx=10,
    pady=7
)


add_label(
    "สายพันธุ์",
    1
)

tk.Entry(
    input_frame,
    textvariable=breed_var,
    width=33
).grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


add_label(
    "อายุ (ปี)",
    2
)

tk.Entry(
    input_frame,
    textvariable=age_var,
    width=33
).grid(
    row=2,
    column=1,
    padx=10,
    pady=7
)


add_label(
    "น้ำหนัก (kg)",
    3
)

tk.Entry(
    input_frame,
    textvariable=weight_var,
    width=33
).grid(
    row=3,
    column=1,
    padx=10,
    pady=7
)


add_label(
    "ปัญหาสุขภาพ",
    4
)

tk.Entry(
    input_frame,
    textvariable=health_var,
    width=33
).grid(
    row=4,
    column=1,
    padx=10,
    pady=7
)


add_label(
    "ระดับกิจกรรม",
    5
)

activity_box = ttk.Combobox(
    input_frame,
    textvariable=activity_var,
    values=[
        "Low",
        "Medium",
        "High"
    ],
    state="readonly",
    width=30
)

activity_box.grid(
    row=5,
    column=1,
    padx=10,
    pady=7
)


add_label(
    "งบประมาณ (บาท/kg)",
    6
)

tk.Entry(
    input_frame,
    textvariable=budget_var,
    width=33
).grid(
    row=6,
    column=1,
    padx=10,
    pady=7
)


# ==========================================
# Buttons
# ==========================================

button_frame = tk.Frame(
    root,
    bg="#F4F6F8"
)

button_frame.pack(
    pady=5
)


analyze_button = tk.Button(
    button_frame,
    text="🔍 วิเคราะห์และแนะนำอาหาร",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8,
    command=run_ai
)

analyze_button.pack(
    side="left",
    padx=5
)


reset_button = tk.Button(
    button_frame,
    text="🔄 ล้างข้อมูล",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8,
    command=reset_form
)

reset_button.pack(
    side="left",
    padx=5
)


exit_button = tk.Button(
    button_frame,
    text="❌ ออกจากโปรแกรม",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8,
    command=exit_app
)

exit_button.pack(
    side="left",
    padx=5
)


# ==========================================
# Result
# ==========================================

result_frame = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)

result_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)


result_title = tk.Label(
    result_frame,
    text="📊 ผลการวิเคราะห์จาก AI",
    font=("Arial", 14, "bold"),
    bg="white"
)

result_title.pack(
    anchor="w",
    padx=15,
    pady=10
)


result_text = tk.Text(
    result_frame,
    font=("Consolas", 10),
    wrap="word"
)

result_text.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(10, 0),
    pady=(0, 10)
)


scrollbar = ttk.Scrollbar(
    result_frame,
    orient="vertical",
    command=result_text.yview
)

scrollbar.pack(
    side="right",
    fill="y",
    pady=(0, 10)
)


result_text.configure(
    yscrollcommand=scrollbar.set
)


# ==========================================
# Start
# ==========================================

root.mainloop()