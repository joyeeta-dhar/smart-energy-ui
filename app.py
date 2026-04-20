import streamlit as st
import requests

st.title("Smart Energy Meter Dashboard")

# Inputs
voltage = st.number_input("Voltage (V)", value=230)
current = st.number_input("Current (A)", value=5)

# ---- ADD LOGIC HERE ----
if current > 10:
    st.error("⚠️ Overload Detected!")
else:
    st.success("✅ Normal Load")

# API Key
API_KEY = "OO5TX7X8H9UUC0LJ"

# Send button
if st.button("Send Data"):
    url = "https://api.thingspeak.com/update"
    
    params = {
        "api_key": API_KEY,
        "field1": voltage,
        "field2": current
    }

    requests.get(url, params=params)
    st.success("Data Sent to ThingSpeak")
