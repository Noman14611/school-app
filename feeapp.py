import streamlit as st
import pandas as pd
import json
import os
from datetime import date

DATA_FILE = "students_fee_data.json"

# Load student data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save student data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# App layout
st.set_page_config(page_title="📚 Fee Manager", layout="centered")
st.title("🏫 Nizami I/H School - Fee Manager")

students = load_data()

tabs = st.tabs(["➕ Add Student", "💸 Submit Fee", "📋 View/Filter", "📤 Export"])

# ➕ Add Student
with tabs[0]:
    with st.form("add_student"):
        name = st.text_input("Student Name")
        fname = st.text_input("Father's Name")
        family_id = st.text_input("Family Group ID (same for siblings)")
        roll = st.text_input("Roll Number")
        student_class = st.selectbox("Class", ["Nursery", "KG"] + [str(i) for i in range(1, 11)])
        monthly_fee = st.number_input("Monthly Fee", min_value=0)
        admission_fee = st.number_input("Admission Fee", min_value=0)
        exam_fee = st.number_input("Exam Fee", min_value=0)
        annual_fund = st.number_input("Annual Fund", min_value=0)
        contact = st.text_input("Parent Contact Number")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            students.append({
                "Name": name,
                "Father": fname,
                "FamilyID": family_id,
                "Roll": roll,
                "Class": student_class,
                "MonthlyFee": monthly_fee,
                "AdmissionFee": admission_fee,
                "ExamFee": exam_fee,
                "AnnualFund": annual_fund,
                "Contact": contact,
                "Payments": {}  # Structure: {"2025-06": ["Monthly", "Admission"]}
            })
            save_data(students)
            st.success("✅ Student added!")

# 💸 Submit Fee
with tabs[1]:
    st.subheader("💰 Submit Fee")
    if students:
        selected_student = st.selectbox("Select Student", [f"{s['Name']} ({s['Roll']})" for s in students])
        fee_type = st.selectbox("Fee Type", ["Monthly", "Admission", "Exam", "Annual"])
        today = date.today()
        current_month = today.strftime("%Y-%m")

        if st.button("Submit Fee"):
            for s in students:
                label = f"{s['Name']} ({s['Roll']})"
                if label == selected_student:
                    if current_month not in s["Payments"]:
                        s["Payments"][current_month] = []
                    if fee_type not in s["Payments"][current_month]:
                        s["Payments"][current_month].append(fee_type)
                        save_data(students)
                        st.success(f"✅ {fee_type} Fee marked as paid for {s['Name']} ({current_month})")
                    else:
                        st.warning("⚠️ This fee type already marked as paid.")
    else:
        st.warning("❌ No students found.")

# 📋 View/Filter
with tabs[2]:
    st.subheader("📋 Student Fee Status")
    df = pd.DataFrame(students)

    if not df.empty:
        col1, col2 = st.columns(2)
        class_filter = col1.selectbox("Filter by Class", ["All"] + sorted(df["Class"].unique()))
        unpaid_type = col2.selectbox("Filter Unpaid Type", ["None", "Monthly", "Admission", "Exam", "Annual"])

        result = []
        current_month = date.today().strftime("%Y-%m")

        for s in students:
            is_unpaid = unpaid_type != "None" and (
                current_month not in s["Payments"] or unpaid_type not in s["Payments"][current_month]
            )
            if (class_filter == "All" or s["Class"] == class_filter) and (
                unpaid_type == "None" or is_unpaid
            ):
                result.append({
                    "Name": s["Name"],
                    "Father": s["Father"],
                    "Roll": s["Roll"],
                    "Class": s["Class"],
                    "Unpaid Fee": unpaid_type if is_unpaid else "-"
                })

        st.dataframe(pd.DataFrame(result), use_container_width=True)
    else:
        st.info("No students to show.")

# 📤 Export
with tabs[3]:
    if st.button("📥 Export to Excel"):
        df_export = pd.DataFrame(students)
        df_export.to_excel("full_fee_records.xlsx", index=False)
        st.success("✅ Data exported to full_fee_records.xlsx")
