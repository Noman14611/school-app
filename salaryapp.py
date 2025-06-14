import streamlit as st
import pandas as pd
import json
import os
from datetime import date

DATA_FILE = "teacher_salary_data.json"

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
    df.to_excel("teachers_salary_record.xlsx", index=False)
    return "teachers_salary_record.xlsx"

# Main function
def run_salary_app():
    st.title("💰 Teacher Salary Manager")

    salary_data = load_data()

    tab1, tab2, tab3 = st.tabs(["➕ Add Salary", "📋 View/Search", "📤 Export"])

    # ➕ Add Salary Tab
    with tab1:
        with st.form("salary_form"):
            name = st.text_input("Teacher Name")
            teacher_id = st.text_input("Teacher ID")
            designation = st.selectbox("Designation", ["Principal", "Vice Principal", "Senior Teacher", "Junior Teacher"])
            salary = st.number_input("Monthly Salary (Rs.)", value=0)
            status = st.selectbox("Salary Paid?", ["Yes", "No"])
            date_paid = str(date.today())

            submit = st.form_submit_button("Add Salary Record")

            if submit:
                salary_data.append({
                    "Name": name,
                    "ID": teacher_id,
                    "Designation": designation,
                    "Salary": salary,
                    "Status": status,
                    "Date": date_paid
                })
                save_data(salary_data)
                st.success("✅ Salary record added!")

    # 📋 View/Search Tab
    with tab2:
        st.subheader("🔍 Search & Filter")
        df = pd.DataFrame(salary_data)

        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                search_name = st.text_input("Search by Name").lower()
            with col2:
                search_id = st.text_input("Search by ID").lower()

            filtered_df = df[
                df["Name"].str.lower().str.contains(search_name) &
                df["ID"].str.lower().str.contains(search_id)
            ]

            if st.checkbox("Show only unpaid"):
                filtered_df = filtered_df[filtered_df["Status"] == "No"]

            st.dataframe(filtered_df, use_container_width=True)

        else:
            st.info("No salary records found.")

    # 📤 Export Tab
    with tab3:
        if salary_data:
            if st.button("📤 Export to Excel"):
                path = export_to_excel(salary_data)
                st.success(f"✅ Exported to `{path}`")
        else:
            st.warning("No records to export.")
