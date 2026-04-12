import streamlit as st
from utils.db import run_query

st.title('Active Disruptions')
st.subheader('Details of Current Disruptions')

st.table({
    "Route": ["No disruptions"],
    "Stop": ["N/A"],
    "Description": ["N/A"],
    "Cause": ["N/A"],
    "Effect": ["N/A"],
    "Start Time": ["N/A"],
    "End Time": ["N/A"],
    "Severity": ["N/A"]
})

#optional chart: active impacts by route
