import streamlit as st
import requests

st.title("🚀 Lead Processor API Dashboard")

# Inputs
api_url = st.text_input("API URL", "https://leadpro-f8gm.onrender.com/docs")
api_key = st.text_input("API Key", "dev-key-123")
raw_text = st.text_area("Raw Text Input", "Imran, Computer Science, 1")

# Button
if st.button("Send Request"):
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "raw_text": raw_text
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)

        st.subheader("Status Code")
        st.write(response.status_code)

        st.subheader("Response")
        st.json(response.json())

    except Exception as e:
        st.error(f"Request failed: {str(e)}")