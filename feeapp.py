import streamlit as st
import json
import os
from datetime import date
import pandas as pd

DATA_FILE = "students_fee_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run_fee_app():
    st.title("📚 Student Fee Management System")

    students = load_data()

    tab1, tab2 = st.tabs(["➕ Add Student", "💰 Submit Fee / View Students"])

    with tab1:
        with st.form("add_form"):
            name = st.text_input("Student Name")
            fname = st.text_input("Father Name")
            family_id = st.text_input("Family ID (same for siblings)")
            roll = st.text_input("Roll Number")
            student_class = st.selectbox("Class", [str(i) for i in range(1, 11)] + ["Nursery", "KG"])
            monthly_fee = st.number_input("Monthly Fee", min_value=0)
            admission_fee = st.number_input("Admission Fee", min_value=0)
            exam_fee = st.number_input("Exam Fee", min_value=0)
            annual_fee = st.number_input("Annual Fund", min_value=0)
            months = {m: "Unpaid" for m in ["January", "February", "March", "April", "May", "June", "July",
                                            "August", "September", "October", "November", "December"]}
            submitted = st.form_submit_button("Add Student")

            if submitted:
                students.append({
                    "Name": name,
                    "FatherName": fname,
                    "FamilyID": family_id,
                    "Roll": roll,
                    "Class": student_class,
                    "MonthlyFee": monthly_fee,
                    "AdmissionFee": admission_fee,
                    "ExamFee": exam_fee,
                    "AnnualFee": annual_fee,
                    "Months": months
                })
                save_data(students)
                st.success("✅ Student Added Successfully!")

    with tab2:
        if not students:
            st.warning("No student records found.")
            return

        df = pd.DataFrame(students)
        class_filter = st.selectbox("Filter by Class", ["All"] + sorted(df["Class"].unique().tolist()))
        unpaid_filter = st.selectbox("Show Unpaid Month Students", ["All"] + list(df["Months"][0].keys()))

        filtered_students = students
        if class_filter != "All":
            filtered_students = [s for s in students if s["Class"] == class_filter]

        if unpaid_filter != "All":
            filtered_students = [s for s in filtered_students if s["Months"][unpaid_filter] == "Unpaid"]

        st.subheader("📋 Student List")
        for student in filtered_students:
            with st.expander(f"{student['Name']} ({student['Roll']}) - Class {student['Class']}"):
                st.markdown(f"👨 Father: {student['FatherName']}")
                st.markdown(f"🏠 Family ID: {student['FamilyID']}")
                st.markdown(f"💵 Monthly Fee: {student['MonthlyFee']}")
                st.markdown(f"📚 Admission: {student['AdmissionFee']}, Exam: {student['ExamFee']}, Annual: {student['AnnualFee']}")

                unpaid_months = [m for m, v in student["Months"].items() if v == "Unpaid"]
                paid_months = [m for m, v in student["Months"].items() if v == "Paid"]

                st.markdown(f"📅 Paid Months: {', '.join(paid_months) if paid_months else 'None'}")
                st.markdown(f"📅 Unpaid Months: {', '.join(unpaid_months) if unpaid_months else 'None'}")

                fee_type = st.selectbox(f"Select Fee Type for {student['Name']}", ["Monthly", "Admission", "Exam", "Annual"], key=student['Roll'])
                if fee_type == "Monthly":
                    selected_month = st.selectbox("Select Month", unpaid_months, key="month_" + student["Roll"])
                else:
                    selected_month = None

                if st.button("💰 Submit Fee", key="btn_" + student["Roll"] + fee_type):
                    if fee_type == "Monthly" and selected_month:
                        student["Months"][selected_month] = "Paid"
                        st.success(f"{fee_type} Fee submitted for {selected_month}")
                    elif fee_type == "Admission":
                        student["AdmissionFee"] = 0
                        st.success("Admission Fee submitted!")
                    elif fee_type == "Exam":
                        student["ExamFee"] = 0
                        st.success("Exam Fee submitted!")
                    elif fee_type == "Annual":
                        student["AnnualFee"] = 0
                        st.success("Annual Fund submitted!")
                    save_data(students)
