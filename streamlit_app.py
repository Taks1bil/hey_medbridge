import streamlit as st
from medbridge_chatbot import MedBridgeChatbot

# Set Streamlit page configuration
st.set_page_config(
    page_title="MedBridge AI Chatbot",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for a modern, AI-centric dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0a192f;
        color: #ccd6f6;
    }
    .st-emotion-cache-10qaj7l {
        background-color: #0a192f;
        color: #64ffda;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        text-align: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .st-emotion-cache-10qaj7l h1 {
        color: #64ffda;
        text-shadow: 0px 0px 10px rgba(100, 255, 218, 0.5);
    }
    .st-emotion-cache-10qaj7l p {
        color: #8892b0;
    }
    .st-emotion-cache-13ln4jo {
        background-color: #0a192f;
    }
    .st-emotion-cache-1r6y40v {
        background-color: #0066CC;
        color: #ffffff;
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }
    .st-emotion-cache-1y4pmz5 {
        background-color: #00A896;
        color: #ffffff;
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }
    .st-emotion-cache-1c7y2o9 {
        background-color: #0a192f;
        border-top: 1px solid #1a3054;
        padding-top: 15px;
    }
    .st-emotion-cache-vj1c9o {
        background-color: #1a3054;
        color: #ccd6f6;
        border: 1px solid #0066CC;
        border-radius: 10px;
        padding: 10px;
    }
    .st-emotion-cache-vj1c9o:focus {
        border-color: #64ffda;
        box-shadow: 0px 0px 8px rgba(100, 255, 218, 0.5);
    }
    .st-emotion-cache-10qaj7l button {
        background-color: #F26419;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .st-emotion-cache-10qaj7l button:hover {
        background-color: #e05c15;
    }
</style>
""", unsafe_allow_html=True)

# 🧠 Add an avatar above the title
st.markdown("""
<div style='text-align:center; margin-top: -20px;'>
    <img src='https://media.giphy.com/media/LPjWFH7HDtvkk/giphy.gif' width='160'/>
</div>
""", unsafe_allow_html=True)

# 🗣️ Add text-to-speech JavaScript
st.markdown("""
<script>
function speak(text) {
    const synth = window.speechSynthesis;
    const utterThis = new SpeechSynthesisUtterance(text);
    utterThis.lang = 'en-US';
    utterThis.pitch = 1;
    utterThis.rate = 1;
    synth.speak(utterThis);
}
</script>
""", unsafe_allow_html=True)

# Initialize the chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MedBridgeChatbot()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am MedBridge AI, your personal health assistant. How can I help you today?"
    })

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            st.markdown(f"<script>speak({repr(message['content'])})</script>", unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("What can I help you with?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display bot response
    response = st.session_state.chatbot.get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
        st.markdown(f"<script>speak({repr(response)})</script>", unsafe_allow_html=True)
