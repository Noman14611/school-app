import streamlit as st
import pandas as pd
import os, json
from datetime import date

def run_fee_app():

    DATA_FILE = "students_data.json"
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            students = json.load(f)
    else:
        students = []

    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def export_excel(data):
        df = pd.DataFrame(data)
        df.to_excel("students_record.xlsx", index=False)
        return "students_record.xlsx"

    st.title("📚 Nizami I/H School - Fee Manager")

    tab1, tab2, tab3 = st.tabs(["➕ Add Student", "📋 View", "📤 Export"])

    with tab1:
        with st.form("add_form"):
            name = st.text_input("Student Name")
            roll = st.text_input("Roll Number")
            student_class = st.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            fee = st.number_input("Monthly Fee", value=0)
            paid = st.selectbox("Fee Paid?", ["Yes", "No"])
            parent_contact = st.text_input("Parent Contact (03xx-xxxxxxx)")
            submitted = st.form_submit_button("Add Student")

            if submitted:
                students.append({
                    "Name": name,
                    "Roll": roll,
                    "Class": student_class,
                    "Fee": fee,
                    "Paid": paid,
                    "ParentContact": parent_contact,
                    "Date": str(date.today())
                })
                save_data(students)
                st.success("✅ Student added!")

    with tab2:
        df = pd.DataFrame(students)
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                search_name = st.text_input("Search by Name").lower()
            with col2:
                search_roll = st.text_input("Search by Roll").lower()
            filtered_df = df[
                df["Name"].str.lower().str.contains(search_name) & df["Roll"].str.lower().str.contains(search_roll)
            ]
            if st.checkbox("Show only unpaid"):
                filtered_df = filtered_df[filtered_df["Paid"] == "No"]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No student data found.")

    with tab3:
        if students and st.button("📤 Export to Excel"):
            path = export_excel(students)
            st.success(f"✅ Exported to `{path}`")
