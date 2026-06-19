import streamlit as st
import requests

st.title("🚀 Lead Processor API Dashboard")

if "history" not in st.session_state:
    st.session_state.history = []

ENVIRONMENTS = {
    "Production": "https://leadpro-f8gm.onrender.com/process",
    "Local": "http://127.0.0.1:8000/process"
}

selected_env = st.selectbox(
    "Environment",
    list(ENVIRONMENTS.keys())
)

default_api = ENVIRONMENTS[selected_env]

# Inputs
api_url = st.text_input("API URL", default_api)
api_key = st.text_input("API Key", "dev-key-123")
raw_text = st.text_area("Raw Text Input", "Imran, Computer Science, 1")

lead_count = len([line for line in raw_text.split("\n") if line.strip()])

st.metric("Requests This Session", len(st.session_state.history))
st.metric("Detected Leads", lead_count)

st.subheader("Request History")
for item in reversed(st.session_state.history):
    st.write(item)

# Button
if st.button("Send Request"):
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {"raw_text": raw_text}

    try:
        response = requests.post(api_url, json=payload, headers=headers)

        st.subheader("Status Code")
        st.write(response.status_code)

        st.subheader("Response")
        try:
            st.json(response.json())
        except Exception:
            st.write(response.text)

        st.session_state.history.append({
            "status": response.status_code,
            "input": raw_text,
            "url": api_url,
            "time": str(__import__('datetime').datetime.now())
        })

    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        st.session_state.history.append({
            "status": "error",
            "error": str(e),
            "input": raw_text,
            "url": api_url,
            "time": str(__import__('datetime').datetime.now())
        })