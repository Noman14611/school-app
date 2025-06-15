import streamlit as st
from feeapp.py import run_fee_app

# You can add more apps later like attendance or salary
app = st.sidebar.selectbox("Select App", ["Fee Submission"])

if app == "Fee Submission":
    run_fee_app()
