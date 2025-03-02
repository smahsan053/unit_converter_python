import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

st.header("Unit Converter")

url = "https://api.happi.dev/v1/unit-converter"
headers = {
    "accept": "application/json",
    "x-happi-token": API_KEY
}
response = requests.get(url, headers=headers)

name = set()
measure = set()
from_unit = ""
to_unit = ""

for measures in response.json()["allowedUnits"]:
    measure.add(measures["measure"])
measurement_options = st.selectbox("Select Measurements", (measure), index=1)

for measures in response.json()["allowedUnits"]:
    if measures["measure"] == measurement_options:
        name.add(measures["name"])
from_name = st.selectbox("Select Unit to Convert From: ", name)
to_name = st.selectbox("Select Unit to Convert To: ", name)

for measures in response.json()["allowedUnits"]:
    if measures["name"] == from_name:
        from_unit = measures["unit"]
    if measures["name"] == to_name:
        to_unit = measures["unit"]

value = st.text_input("Enter Value")
url = f"https://api.happi.dev/v1/unit-converter?from={from_unit}&to={to_unit}&value={value}"
if st.button("Convert"):
    if from_unit and to_unit and value:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            from_unit = result.get('from', '').capitalize()
            to_unit = result.get('to', '').capitalize()
            converted_value = result.get('result', '')
            st.write(f"{value} {from_unit} is equals to {float(converted_value):.2f} {to_unit}")
        else:
            st.error(f"API Error: {response.status_code}")
    else:
        st.warning("Please fill all fields")
