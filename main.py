import streamlit as st
from feeapp import run_fee_app
from attendanceapp import run_attendance_app

st.set_page_config(page_title="📚 School Management App", layout="centered")

st.sidebar.title("📂 Select App")
app_option = st.sidebar.selectbox("Choose an app", ["Fee Management", "Attendance"])

if app_option == "Fee Management":
    run_fee_app()
elif app_option == "Attendance":
    run_attendance_app()
