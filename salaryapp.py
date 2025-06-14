import streamlit as st
import pandas as pd
import os, json
from datetime import date

def run_salary_app():
    st.set_page_config(page_title="👩‍🏫 Teacher Salary", layout="centered")

    DATA_FILE = "salary_data.json"
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            salary_data = json.load(f)
    else:
        salary_data = []

    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def export_excel(data):
        df = pd.DataFrame(data)
        df.to_excel("teacher_salary.xlsx", index=False)
        return "teacher_salary.xlsx"

    st.title("👨‍🏫 Teacher Salary Record")

    tab1, tab2, tab3 = st.tabs(["➕ Add Salary", "📋 View", "📤 Export"])

    with tab1:
        with st.form("salary_form"):
            name = st.text_input("Teacher Name")
            subject = st.text_input("Subject")
            salary = st.number_input("Monthly Salary", value=0)
            paid = st.selectbox("Salary Paid?", ["Yes", "No"])
            date_given = str(date.today())
            submitted = st.form_submit_button("Add Salary")

            if submitted:
                salary_data.append({
                    "Name": name, "Subject": subject,
                    "Salary": salary, "Paid": paid,
                    "Date": date_given
                })
                save_data(salary_data)
                st.success("✅ Salary record added!")

    with tab2:
        df = pd.DataFrame(salary_data)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No salary records.")

    with tab3:
        if salary_data and st.button("📤 Export to Excel"):
            path = export_excel(salary_data)
            st.success(f"✅ Exported to `{path}`")
