import streamlit as st
from app import run_fee_app
from attendanceapp import run_attendance_app

st.set_page_config(page_title="🏫 School Management", layout="wide")
st.sidebar.title("📂 Select Application")

selected = st.sidebar.selectbox("📌 Choose App", ["📅 Attendance", "💰 Fee Manager"])

if selected == "📅 Attendance":
    run_attendance_app()
elif selected == "💰 Fee Manager":
    run_fee_app()
