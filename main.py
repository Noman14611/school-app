import streamlit as st
st.set_page_config(page_title="🏫 School Manager", layout="centered")

from app import run_fee_app
from attendanceapp import run_attendance_app
from salaryapp import run_salary_app  # ✅ make sure this line is added

st.sidebar.title("📋 Select App")
app_choice = st.sidebar.selectbox("Choose an app", ["🎓 Fee Manager", "📅 Attendance", "💰 Teacher Salary"])

if app_choice == "🎓 Fee Manager":
    run_fee_app()
elif app_choice == "📅 Attendance":
    run_attendance_app()
elif app_choice == "💰 Teacher Salary":
    run_salary_app()
