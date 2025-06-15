import streamlit as st
import pandas as pd
import json
import os
from datetime import date

DATA_FILE = "students_data.json"
MONTHS = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run_fee_app():
    st.set_page_config(page_title="🎓 Fee Manager", layout="centered")
    st.title("📚 Nizami I/H School – Fee Submission")

    students = load_data()
    tab1, tab2 = st.tabs(["➕ Add Student", "💳 Submit/View Fee"])

    # ➕ Add Student Tab
    with tab1:
        with st.form("add_student_form"):
            name = st.text_input("Student Name")
            f_name = st.text_input("Father's Name")
            roll = st.text_input("Roll Number")
            family_id = st.text_input("Family Group ID (for siblings)", value="")
            student_class = st.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            monthly_fee = st.number_input("Monthly Fee", value=0)
            admission_fee = st.number_input("Admission Fee", value=0)
            exam_fee = st.number_input("Exam Fee", value=0)
            annual_fund = st.number_input("Annual Fund", value=0)
            months_paid = st.multiselect("Select Paid Months", MONTHS)
            submitted = st.form_submit_button("Add Student")

            if submitted:
                students.append({
                    "Name": name,
                    "Father": f_name,
                    "Roll": roll,
                    "FamilyID": family_id,
                    "Class": student_class,
                    "MonthlyFee": monthly_fee,
                    "AdmissionFee": admission_fee,
                    "ExamFee": exam_fee,
                    "AnnualFund": annual_fund,
                    "PaidMonths": months_paid,
                    "DateAdded": str(date.today())
                })
                save_data(students)
                st.success(f"✅ {name} added successfully!")

    # 💳 Submit/View Fee Tab
    with tab2:
        if not students:
            st.warning("No students added yet.")
            return

        df = pd.DataFrame(students)

        st.subheader("🎓 Search Student")
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("Search by Name").lower()
        with col2:
            search_roll = st.text_input("Search by Roll Number").lower()
        with col3:
            selected_class = st.selectbox("Filter by Class", ["All"] + sorted(df["Class"].unique().tolist()))

        filtered_df = df[
            df["Name"].str.lower().str.contains(search_name) &
            df["Roll"].str.lower().str.contains(search_roll)
        ]

        if selected_class != "All":
            filtered_df = filtered_df[filtered_df["Class"] == selected_class]

        if st.checkbox("Show Only Unpaid Students"):
            filtered_df = filtered_df[filtered_df["PaidMonths"].apply(lambda x: len(x) < 12)]

        st.dataframe(filtered_df, use_container_width=True)

        st.subheader("💸 Fee Submission")
        student_names = [f"{s['Name']} - {s['Roll']}" for s in students]
        selected_student = st.selectbox("Select Student", student_names)

        student = next(s for s in
