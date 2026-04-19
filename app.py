import streamlit as st
import requests

st.title("Smart Energy Meter Dashboard")

st.write("Send data to ThingSpeak")

# Input UI
field1 = st.number_input("Enter Power Value", min_value=0, max_value=500, value=50)
field2 = st.number_input("Enter Voltage Value", min_value=0, max_value=500, value=30)

# Your API Key
API_KEY = "OO5TX7X8H9UUC0LJ"

# Button
if st.button("Send Data"):
    url = "https://api.thingspeak.com/update"

    params = {
        "api_key": API_KEY,
        "field1": field1,
        "field2": field2
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        st.success("Data sent to ThingSpeak!")
    else:
        st.error("Error sending data")