import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

DATA_FILE = "students.json"

def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_students(students):
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

def run_fee_app():
    st.set_page_config(page_title="🎓 Fee Management", layout="centered")
    st.title("🎓 School Fee Submission App")

    students = load_students()

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Add Student",
        "📋 View/Search",
        "💰 Fee Submission",
        "🚨 Unpaid Students"
    ])

    # ➕ Add Student
    with tab1:
        st.subheader("➕ Add New Student")
        name = st.text_input("Student Name")
        father_name = st.text_input("Father's Name")
        student_class = st.text_input("Class")
        family_id = st.text_input("Family Group ID (same for siblings)")
        monthly_fee = st.number_input("Monthly Fee", 0)
        admission_fee = st.number_input("Admission Fee", 0)
        exam_fee = st.number_input("Exam Fee", 0)
        annual_fund = st.number_input("Annual Fund", 0)

        if st.button("Add Student"):
            student = {
                "Name": name,
                "FatherName": father_name,
                "Class": student_class,
                "FamilyID": family_id,
                "MonthlyFee": monthly_fee,
                "AdmissionFee": admission_fee,
                "ExamFee": exam_fee,
                "AnnualFund": annual_fund,
                "PaidMonths": [],
                "FeeRecords": [],
                "MonthlyFeeStatus": "Unpaid"
            }
            students.append(student)
            save_students(students)
            st.success("Student added successfully!")

    # 📋 View/Search
    with tab2:
        st.subheader("🔍 View or Search Students")
        search_name = st.text_input("Search by Name")
        df = pd.DataFrame(students)
        if search_name:
            df = df[df["Name"].str.contains(search_name, case=False)]
        st.dataframe(df, use_container_width=True)

    # 💰 Fee Submission
    with tab3:
        st.subheader("💰 Submit Fee")
        student_names = [s["Name"] for s in students]
        selected_name = st.selectbox("Select Student", student_names)
        fee_type = st.selectbox("Fee Type", ["Monthly", "Admission", "Exam", "Annual"])
        selected_month = st.selectbox("Month", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])

        if st.button("Submit Fee"):
            for s in students:
                if s["Name"] == selected_name:
                    record = {
                        "Date": str(datetime.now().date()),
                        "FeeType": fee_type,
                        "Month": selected_month,
                        "Amount": 0
                    }
                    if fee_type == "Monthly":
                        record["Amount"] = s["MonthlyFee"]
                        if selected_month not in s["PaidMonths"]:
                            s["PaidMonths"].append(selected_month)
                            s["MonthlyFeeStatus"] = "Paid"
                    elif fee_type == "Admission":
                        record["Amount"] = s["AdmissionFee"]
                    elif fee_type == "Exam":
                        record["Amount"] = s["ExamFee"]
                    elif fee_type == "Annual":
                        record["Amount"] = s["AnnualFund"]

                    s["FeeRecords"].append(record)
                    st.success(f"{fee_type} fee submitted for {selected_name}.")
                    break
            save_students(students)

    # 🚨 Unpaid Students
    with tab4:
        st.subheader("📌 Class-wise Unpaid Students")
        df = pd.DataFrame(students)

        if not df.empty:
            class_options = ["All"] + sorted(df["Class"].unique())
            selected_class = st.selectbox("Select Class", class_options)
            unpaid_df = df[df["MonthlyFeeStatus"] == "Unpaid"]

            if selected_class != "All":
                unpaid_df = unpaid_df[unpaid_df["Class"] == selected_class]

            st.dataframe(unpaid_df, use_container_width=True)
        else:
            st.info("No student records found.")
