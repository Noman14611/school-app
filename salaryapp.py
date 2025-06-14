import streamlit as st
import pandas as pd
import json
import os
from datetime import date

DATA_FILE = "salary_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def export_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel("teacher_salary.xlsx", index=False)
    return "teacher_salary.xlsx"

def run_salary_app():
    st.title("💰 Teacher Salary Manager")

    salary_data = load_data()

    tab1, tab2, tab3 = st.tabs(["➕ Add Salary", "📋 View/Search", "📤 Export"])

    # ➕ Add Salary
    with tab1:
        with st.form("salary_form"):
            name = st.text_input("Teacher Name")
            month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June",
                                           "July", "August", "September", "October", "November", "December"])
            amount = st.number_input("Salary Amount", min_value=0)
            paid = st.selectbox("Paid?", ["Yes", "No"])
            date_paid = st.date_input("Date of Payment", date.today())

            submit = st.form_submit_button("Submit Salary")

            if submit:
                salary_data.append({
                    "Name": name,
                    "Month": month,
                    "Amount": amount,
                    "Paid": paid,
                    "Date": str(date_paid)
                })
                save_data(salary_data)
                st.success("✅ Salary record added!")

    # 📋 View/Search
    with tab2:
        st.subheader("🔍 Search Records")
        df = pd.DataFrame(salary_data)
        if not df.empty:
            search_name = st.text_input("Search by Teacher Name").lower()
            filtered_df = df[df["Name"].str.lower().str.contains(search_name)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No salary records yet.")

    # 📤 Export
    with tab3:
        if salary_data:
            if st.button("📤 Export to Excel"):
                path = export_to_excel(salary_data)
                st.success(f"✅ Exported to `{path}`")
        else:
            st.warning("No data to export.")
