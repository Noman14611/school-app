import streamlit as st
from feeapp import run_fee_app
from attendanceapp import run_attendance_app
from salaryapp import run_salary_app

st.set_page_config(page_title="School App", layout="centered")

app = st.selectbox("Choose App", ["Fee", "Attendance", "Salary"])

if app == "Fee":
    run_fee_app()
elif app == "Attendance":
    run_attendance_app()
elif app == "Salary":
    run_salary_app()
