import streamlit as st
import requests
import os

# Load Hugging Face API token from env or Streamlit secrets
HF_API_TOKEN = os.getenv("HF_API_TOKEN") or st.secrets.get("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/gpt2"  # example model

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API request failed with status code {response.status_code}"}

st.title("🤖 Hugging Face Chatbot Demo")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me anything."}
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")
    else:
        st.markdown(f"**You:** {msg['content']}")

# User input
prompt = st.text_input("You:", "")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Query HF API
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }
    output = query(payload)
    
    if "error" in output:
        response = output["error"]
    else:
        # output is a list of generated texts
        response = output[0]["generated_text"]
        # To clean up, remove prompt repetition:
        if response.startswith(prompt):
            response = response[len(prompt):].strip()

    st.session_state.messages.append({"role": "assistant", "content": response})

    # Refresh to show new messages
    st.experimental_rerun()
