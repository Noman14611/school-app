import streamlit as st
import pandas as pd
import os
import json
from datetime import date

DATA_FILE = "students_data.json"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Export Excel
def export_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel("students_record.xlsx", index=False)
    return "students_record.xlsx"

st.set_page_config(page_title="🎓 Student Fee Manager", layout="centered")
st.title("📚 Nizami I/H School")

students = load_data()

# Helper: Calculate Remaining Fee
def calculate_remaining_fee(student):
    total_fee = student.get("MonthlyFee", 0) + student.get("AnnualFund", 0) + student.get("ExamFee", 0) + student.get("AdmissionFee", 0)
    paid_months = student.get("PaidMonths", [])
    remaining_months = 12 - len(paid_months)
    return (remaining_months * student.get("MonthlyFee", 0)) + student.get("AnnualFund", 0) + student.get("ExamFee", 0) + student.get("AdmissionFee", 0)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Student", "📋 View/Search/Filter", "✅ Mark Fee Paid", "📤 Export"])

# ➕ Add Student Tab
with tab1:
    with st.form("add_form"):
        name = st.text_input("Student Name")
        fname = st.text_input("Father's Name")
        roll = st.text_input("Roll Number")
        family_id = st.text_input("Family Group ID (for siblings)")
        student_class = st.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        monthly_fee = st.number_input("Monthly Fee", value=0)
        annual_fund = st.number_input("Annual Fund", value=0)
        exam_fee = st.number_input("Exam Fee", value=0)
        admission_fee = st.number_input("Admission Fee", value=0)
        parent_contact = st.text_input("Parent Contact Number (e.g., 03xx-xxxxxxx)")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            students.append({
                "Name": name,
                "Father": fname,
                "Roll": roll,
                "FamilyID": family_id,
                "Class": student_class,
                "MonthlyFee": monthly_fee,
                "AnnualFund": annual_fund,
                "ExamFee": exam_fee,
                "AdmissionFee": admission_fee,
                "ParentContact": parent_contact,
                "PaidMonths": [],
                "Date": str(date.today())
            })
            save_data(students)
            st.success("✅ Student added successfully!")

# 📋 View/Search/Filter Tab
with tab2:
    st.subheader("🔍 Search & Filter Students")
    df = pd.DataFrame(students)

    if not df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("Search by Name").lower()
        with col2:
            search_roll = st.text_input("Search by Roll Number").lower()
        with col3:
            selected_class = st.selectbox("Filter by Class", ["All"] + sorted(df["Class"].unique().tolist()))

        filtered_df = df[df["Name"].str.lower().str.contains(search_name) &
                         df["Roll"].str.lower().str.contains(search_roll)]

        if selected_class != "All":
            filtered_df = filtered_df[filtered_df["Class"] == selected_class]

        if st.checkbox("Show only unpaid students"):
            filtered_df = filtered_df[filtered_df["PaidMonths"].apply(lambda x: len(x) < 12)]

        if not filtered_df.empty:
            for i, row in filtered_df.iterrows():
                remaining = calculate_remaining_fee(row)
                st.write(f"**{row['Name']} ({row['Roll']})** | Class: {row['Class']} | Remaining Fee: Rs. {remaining}")
                st.write(f"Paid Months: {', '.join(row['PaidMonths']) if row['PaidMonths'] else 'None'}")
        else:
            st.info("No matching students found.")
    else:
        st.info("No records available.")

# ✅ Mark Fee Paid Tab
with tab3:
    st.subheader("✅ Mark Student Fee as Paid")
    if students:
        student_roll = st.selectbox("Select Roll Number", [s["Roll"] for s in students])
