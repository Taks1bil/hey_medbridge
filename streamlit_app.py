import streamlit as st
from streamlit_lottie import st_lottie
import requests
from medbridge_chatbot import MedBridgeChatbot
import os
import tempfile

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Detect Streamlit Cloud environment ---
is_cloud = os.getenv("STREAMLIT_CLOUD", "") == "true"

# --- Sidebar options ---
st.sidebar.title("Settings")
if is_cloud:
    use_local_tts = False
    st.sidebar.info("Local TTS disabled on Streamlit Cloud. Using browser TTS instead.")
else:
    use_local_tts = st.sidebar.checkbox("Use local TTS (pyttsx3)", value=False)
show_3d_avatar = st.sidebar.checkbox("Show external 3D avatar", value=False)

# --- Lazy pyttsx3 engine initialization ---
engine = None
def get_engine():
    global engine
    if engine is None:
        import pyttsx3
        eng = pyttsx3.init()
        eng.setProperty('rate', 150)
        eng.setProperty('volume', 1)
        engine = eng
    return engine

def synthesize_speech(text):
    eng = get_engine()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        eng.save_to_file(text, tmp_file.name)
        eng.runAndWait()
        return tmp_file.name

# --- Page config ---
st.set_page_config(
    page_title="MedBridge AI Chatbot",
    page_icon=":robot_face:",
    layout="centered"
)

# --- CSS Styling ---
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
</style>
""", unsafe_allow_html=True)

# --- Load Lottie animation ---
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

lottie_robot = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_touohxv0.json")

# --- Avatar or animation ---
with st.container():
    if show_3d_avatar:
        st.markdown("""
            <iframe src="https://readyplayer.me/avatar/your-avatar-url"
            width="300" height="400" frameborder="0" allowfullscreen></iframe>
        """, unsafe_allow_html=True)
    elif lottie_robot:
        st_lottie(lottie_robot, height=200, key="robot")

# --- JavaScript TTS for browsers ---
if not use_local_tts:
    st.markdown("""
    <script>
    function speak(text) {
        const synth = window.speechSynthesis;
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = 'en-US';
        utter.pitch = 1;
        utter.rate = 1;
        synth.speak(utter);
    }
    </script>
    """, unsafe_allow_html=True)

# --- Initialize chatbot with GPT fallback ---
if "chatbot" not in st.session_state:
    st.session_state.chatbot = MedBridgeChatbot(use_gpt_fallback=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I am MedBridge AI, your personal health assistant. How can I help you today?"
    }]

# --- Display message history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if use_local_tts:
                audio_path = synthesize_speech(msg["content"])
                with open(audio_path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                os.remove(audio_path)
            else:
                st.markdown(f"<script>speak({repr(msg['content'])})</script>", unsafe_allow_html=True)

# --- Input and response ---
if prompt := st.chat_input("What can I help you with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.chatbot.get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
        if use_local_tts:
            audio_path = synthesize_speech(response)
            with open(audio_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove(audio_path)
        else:
            st.markdown(f"<script>speak({repr(response)})</script>", unsafe_allow_html=True)

# --- Download chat log ---
if st.sidebar.button("Download chat history"):
    chat_text = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    st.sidebar.download_button(
        label="Download as .txt",
        data=chat_text,
        file_name="medbridge_chat_history.txt",
        mime="text/plain"
    )
