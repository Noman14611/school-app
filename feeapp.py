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

tab1, tab2, tab3 = st.tabs(["➕ Add Student", "📋 View/Search/Filter", "📤 Export"])

# ➕ Add Student Tab
with tab1:
    with st.form("add_form"):
        name = st.text_input("Student Name")
        roll = st.text_input("Roll Number")
        student_class = st.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        fee = st.number_input("Monthly Fee", value=0)
        paid = st.selectbox("Fee Paid?", ["Yes", "No"])
        parent_contact = st.text_input("Parent Contact Number (e.g., 03xx-xxxxxxx)")
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
            st.success("✅ Student added successfully!")

# 📋 View/Search/Filter Tab
with tab2:
    st.subheader("🔍 Search & Filter Students")
    df = pd.DataFrame(students)

    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            search_name = st.text_input("Search by Name").lower()
        with col2:
            search_roll = st.text_input("Search by Roll Number").lower()

        filtered_df = df[
            df["Name"].str.lower().str.contains(search_name) &
            df["Roll"].str.lower().str.contains(search_roll)
        ]

        if st.checkbox("Show only unpaid students"):
            filtered_df = filtered_df[filtered_df["Paid"] == "No"]

        st.dataframe(filtered_df, use_container_width=True)

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
