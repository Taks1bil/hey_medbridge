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
    .stApp { /* Main app container */
        background-color: #0a192f; /* Dark blue background */
        color: #ccd6f6; /* Light gray text */
    }
    .st-emotion-cache-10qaj7l { /* Header/Title area */
        background-color: #0a192f;
        color: #64ffda; /* Teal for title */
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        text-align: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .st-emotion-cache-10qaj7l h1 { /* Title text */
        color: #64ffda;
        text-shadow: 0px 0px 10px rgba(100, 255, 218, 0.5);
    }
    .st-emotion-cache-10qaj7l p { /* Subtitle text */
        color: #8892b0;
    }
    .st-emotion-cache-13ln4jo { /* Chat message container */
        background-color: #0a192f;
    }
    .st-emotion-cache-1r6y40v { /* User message bubble */
        background-color: #0066CC; /* Darker blue for user */
        color: #ffffff;
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }
    .st-emotion-cache-1y4pmz5 { /* Assistant message bubble */
        background-color: #00A896; /* Teal for assistant */
        color: #ffffff;
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }
    .st-emotion-cache-1c7y2o9 { /* Chat input container */
        background-color: #0a192f;
        border-top: 1px solid #1a3054;
        padding-top: 15px;
    }
    .st-emotion-cache-vj1c9o { /* Chat input text area */
        background-color: #1a3054;
        color: #ccd6f6;
        border: 1px solid #0066CC;
        border-radius: 10px;
        padding: 10px;
    }
    .st-emotion-cache-vj1c9o:focus { /* Chat input focus */
        border-color: #64ffda;
        box-shadow: 0px 0px 8px rgba(100, 255, 218, 0.5);
    }
    .st-emotion-cache-10qaj7l button { /* Send button */
        background-color: #F26419; /* Orange accent */
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .st-emotion-cache-10qaj7l button:hover {
        background-color: #e05c15;
    }
    .st-emotion-cache-10qaj7l .st-emotion-cache-1v0mbvd { /* Chat message avatar */
        color: #64ffda;
    }
    .st-emotion-cache-10qaj7l .st-emotion-cache-1v0mbvd img { /* Chat message avatar image */
        border-radius: 50%;
        border: 2px solid #64ffda;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MedBridgeChatbot()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting from the bot
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am MedBridge AI, your personal health assistant. How can I help you today?"})

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


