import streamlit as st
from medbridge_chatbot import MedBridgeChatbot

# Initialize the chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MedBridgeChatbot()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="MedBridge AI Chatbot", page_icon=":robot_face:")
st.title("MedBridge AI Chatbot")
st.markdown("Your personal health assistant. Ask me about symptoms, general health, or MedBridge AI.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        response = st.session_state.chatbot.get_response(prompt)
        st.markdown(response)
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


