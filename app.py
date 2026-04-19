# 🔥 FINAL SMART ENERGY DASHBOARD (ALL-IN-ONE)

import streamlit as st
import requests
import pandas as pd

st.title("⚡ Smart Energy Meter Dashboard")

# ---- INPUTS ----
voltage = st.number_input("Voltage (V)", value=230)
current = st.number_input("Current (A)", value=5)

# ---- POWER CALCULATION ----
power = voltage * current
st.write(f"⚡ Power Consumption: {power} Watts")

# ---- SMART ALERT SYSTEM ----
if current > 15:
    st.error("🚨 Critical Overload!")
elif current > 10:
    st.warning("⚠️ High Load")
else:
    st.success("✅ Normal Load")

# ---- STORE DATA FOR LIVE GRAPH ----
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Voltage", "Current", "Power"])

new_data = pd.DataFrame([[voltage, current, power]],
                        columns=["Voltage", "Current", "Power"])

st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

# ---- LIVE GRAPH ----
st.subheader("📊 Live Energy Data")
st.line_chart(st.session_state.data)

# ---- THINGSPEAK API ----
API_KEY = st.secrets["OO5TX7X8H9UUC0LJ"]  # secure key (use secrets in deployment)

if st.button("Send Data to ThingSpeak"):
    url = "https://api.thingspeak.com/update"
    
    params = {
        "api_key": API_KEY,
        "field1": voltage,
        "field2": current,
        "field3": power
    }

    response = requests.get(url, params=params)

    st.write("Response Code:", response.status_code)
    st.write("Response Text:", response.text)

    response = requests.get(url, params=params)

    if response.status_code == 200:
        st.success("✅ Data Sent to ThingSpeak")
    else:
        st.error("❌ Failed to send data")
