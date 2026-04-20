import streamlit as st
import requests

st.title("🚀 Smart Energy Meter: Predictive Maintenance Mode")

# 1. Inputs
voltage = st.number_input("Voltage (V)", value=230)
current = st.number_input("Current (A)", value=0.0, step=0.1)
power = voltage * current

# 2. Signature Database (Simulating NILM Library)
# We define ranges because real appliances vary slightly
signatures = {
    "LED Bulb": (0.1, 0.5),
    "Laptop/TV": (0.6, 2.0),
    "Refrigerator": (2.1, 4.0),
    "Microwave/Toaster": (5.0, 9.0),
    "Air Conditioner (AC)": (9.1, 13.0),
    "Electric Water Heater": (13.1, 18.0)
}

# 3. Logic for Identification & Overload
overload_status = 0
identified_appliance = "None/Standby"

# Find which appliance matches the current
for name, (low, high) in signatures.items():
    if low <= current <= high:
        identified_appliance = name
        break
if current > 18.0:
    identified_appliance = "UNKNOWN HIGH LOAD"

st.subheader(f"Detected Appliance: {identified_appliance}")

# 4. Predictive Maintenance & Overload Alerts
if current > 12.0:
    overload_status = 1
    st.error(f"⚠️ OVERLOAD! Current ({current}A) exceeds 12A Safety Limit.")
    
    if identified_appliance == "Air Conditioner (AC)":
        st.warning("PREDICTIVE ALERT: AC is drawing max current. Check compressor health or clean filters.")
    elif identified_appliance == "Electric Water Heater":
        st.warning("CRITICAL ALERT: High Power heating detected. Ensure wiring is rated for this load.")
else:
    st.success("✅ System Operating Within Safe Limits")

# 5. Send Data to ThingSpeak
API_KEY = "OO5TX7X8H9UUC0LJ"

if st.button("Update Cloud Data"):
    url = "https://api.thingspeak.com/update"
    params = {
        "api_key": API_KEY,
        "field1": voltage,
        "field2": current,
        "field3": power,
        "field5": overload_status
    }
    
    try:
        requests.get(url, params=params)
        st.info(f"Cloud Sync: {identified_appliance} data pushed to Field 2 & 5.")
    except:
        st.error("Connection Error")
