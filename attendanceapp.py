import streamlit as st
import pandas as pd
import os, json
from datetime import date

def run_attendance_app():
    st.set_page_config(page_title="📅 Attendance App", layout="centered")

    DATA_FILE = "attendance_data.json"
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            attendance = json.load(f)
    else:
        attendance = []

    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def export_excel(data):
        df = pd.DataFrame(data)
        df.to_excel("attendance_record.xlsx", index=False)
        return "attendance_record.xlsx"

    st.title("🏫 Attendance Tracker")

    tab1, tab2, tab3 = st.tabs(["📝 Mark Attendance", "📊 View", "📤 Export"])

    with tab1:
        with st.form("attendance_form"):
            name = st.text_input("Student Name")
            roll = st.text_input("Roll Number")
            student_class = st.selectbox("Class", ["Nursery", "KG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            status = st.radio("Status", ["Present", "Absent"])
            today = date.today().strftime("%Y-%m-%d")
            submit = st.form_submit_button("✔️ Mark Attendance")
            if submit:
                attendance.append({
                    "Name": name, "Roll": roll, "Class": student_class,
                    "Status": status, "Date": today
                })
                save_data(attendance)
                st.success(f"✅ Attendance marked for {name} on {today}")

    with tab2:
        df = pd.DataFrame(attendance)
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                search_name = st.text_input("Search by Name").lower()
            with col2:
                search_roll = st.text_input("Search by Roll").lower()
            filtered_df = df[
                df["Name"].str.lower().str.contains(search_name) & df["Roll"].str.lower().str.contains(search_roll)
            ]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No attendance records yet.")

    with tab3:
        if attendance and st.button("📤 Export to Excel"):
            path = export_excel(attendance)
            st.success(f"✅ Exported to `{path}`")
