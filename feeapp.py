import streamlit as st
import pandas as pd
import json
import os
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

# Export to Excel
def export_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel("students_record.xlsx", index=False)
    return "students_record.xlsx"

st.set_page_config(page_title="🎓 Student Fee Manager", layout="centered")
st.title("📚 Nizami I/H School")

students = load_data()

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Tabs setup
tab1, tab2, tab3 = st.tabs(["➕ Add Student", "📋 View/Search/Filter", "📤 Export"])

# ➕ Add Student Tab
with tab1:
    with st.form("add_form"):
        name = st.text_input("Student Name")
        fname = st.text_input("Father's Name")
        family_id = st.text_input("Family Group ID (same for siblings)")
        roll = st.text_input("Roll Number")
        student_class = st.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        monthly_fee = st.number_input("Monthly Fee", value=0)
        annual_fee = st.number_input("Annual Fund", value=0)
        exam_fee = st.number_input("Exam Fee", value=0)
        admission_fee = st.number_input("Admission Fee", value=0)
        paid_months = st.multiselect("Select Paid Months", months)
        parent_contact = st.text_input("Parent Contact Number (e.g., 03xx-xxxxxxx)")
        submit = st.form_submit_button("Add Student")

        if submit:
            student_data = {
                "Name": name,
                "Father": fname,
                "FamilyID": family_id,
                "Roll": roll,
                "Class": student_class,
                "MonthlyFee": monthly_fee,
                "AnnualFee": annual_fee,
                "ExamFee": exam_fee,
                "AdmissionFee": admission_fee,
                "PaidMonths": paid_months,
                "ParentContact": parent_contact,
                "DateAdded": str(date.today())
            }
            students.append(student_data)
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

        filtered_df = df[
            df["Name"].str.lower().str.contains(search_name) &
            df["Roll"].str.lower().str.contains(search_roll)
        ]

        if selected_class != "All":
            filtered_df = filtered_df[filtered_df["Class"] == selected_class]

        st.write("### Filtered Students")
        st.dataframe(filtered_df, use_container_width=True)

        if st.checkbox("Show only unpaid students for a month"):
            selected_month = st.selectbox("Select Month to Check Unpaid", months)
            unpaid_df = df[~df["PaidMonths"].apply(lambda x: selected_month in x)]
            if selected_class != "All":
                unpaid_df = unpaid_df[unpaid_df["Class"] == selected_class]
            st.write(f"### Unpaid Students for {selected_month}")
            st.dataframe(unpaid_df, use_container_width=True)

        st.write("### Fee Breakdown and Remaining Amount")
        df["Remaining"] = df.apply(lambda row: row["MonthlyFee"] * (12 - len(row["PaidMonths"])) + row["AnnualFee"] + row["ExamFee"] + row["AdmissionFee"], axis=1)
        st.dataframe(df[["Name", "Roll", "Class", "MonthlyFee", "AnnualFee", "ExamFee", "AdmissionFee", "PaidMonths", "Remaining"]], use_container_width=True)

        del_roll = st.text_input("🎯 Enter Roll Number to Delete")
        if st.button("🗑️ Delete Student"):
            updated = [s for s in students if s["Roll"] != del_roll]
            if len(updated) < len(students):
                save_data(updated)
                st.success("✅ Student deleted.")
                st.experimental_rerun()
            else:
                st.warning("❌ Roll number not found.")
    else:
        st.info("No records available.")

# 📤 Export Tab
with tab3:
    if students:
        if st.button("📤 Export to Excel"):
            path = export_to_excel(students)
            st.success(f"✅ Exported to `{path}`")
    else:
        st.warning("No records to export.")
