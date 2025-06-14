import streamlit as st
from feeapp import run_fee_app
from attendanceapp import run_attendance_app
from salaryapp import run_salary_app

st.set_page_config(page_title="📚 School Management", layout="wide")

st.sidebar.title("📂 Select App")
app = st.sidebar.selectbox("Choose one", ["Fee Manager", "Attendance", "Teacher Salary"])

if app == "Fee Manager":
    run_fee_app()
elif app == "Attendance":
    run_attendance_app()
elif app == "Teacher Salary":
    run_salary_app()
