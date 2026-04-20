import streamlit as st
import requests

st.title("Smart Energy Meter Dashboard")

# 1. Inputs
voltage = st.number_input("Voltage (V)", value=230)
current = st.number_input("Current (A)", value=5, step=1)
power = voltage * current

# 2. NILM Simulation Logic (Defining Signatures)
# In a real NILM system, these would be in a database
AC_SIGNATURE = 8.0  # AC usually pulls 8A
FRIDGE_SIGNATURE = 2.0 
HEATER_SIGNATURE = 12.0

# 3. Enhanced Logic for Overload & Identification
overload_status = 0 # 0 for Normal, 1 for Overload

if current > 12:
    overload_status = 1
    st.error("⚠️ OVERLOAD DETECTED!")
    
    # Simple NILM Logic: Guessing the culprit based on current levels
    if current >= 15:
        st.warning("Prediction: Heavy Load (Heater/Industrial Motor) detected. Check for insulation wear.")
    elif current >= 10:
        st.warning("Prediction: AC Unit is drawing abnormal current. Maintenance required.")
else:
    st.success("✅ Normal Load")
    st.info(f"System Health: Stable. Total Power: {power}W")

# 4. API Key & Data Sending
API_KEY = "OO5TX7X8H9UUC0LJ"

if st.button("Send Data"):
    url = "https://api.thingspeak.com/update"
    
    # We add Field 5 for the Overload Status (the 0 or 1 you saw in your chart)
    params = {
        "api_key": API_KEY,
        "field1": voltage,
        "field2": current,
        "field3": power,
        "field5": overload_status # This populates the red dots in your chart!
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            st.success("Data Sent to ThingSpeak Successfully!")
    except:
        st.error("Failed to connect to ThingSpeak.")
