import streamlit as st
from streamlit_lottie import st_lottie
import requests
from medbridge_chatbot import MedBridgeChatbot
import os

# --- Detect Streamlit Cloud environment ---
is_cloud = os.getenv("STREAMLIT_CLOUD", "") == "true"

# --- Sidebar options ---
st.sidebar.title("Settings")
if is_cloud:
    use_local_tts = False
    st.sidebar.info("Local TTS disabled on Streamlit Cloud. Using browser TTS instead.")
else:
    use_local_tts = st.sidebar.checkbox("Use local TTS (pyttsx3) instead of browser TTS", value=False)
show_3d_avatar = st.sidebar.checkbox("Show external 3D avatar (iframe)", value=False)

# --- Lazy pyttsx3 engine initialization ---
engine = None

def get_engine():
    global engine
    if engine is None:
        import pyttsx3
        eng = pyttsx3.init()
        eng.setProperty('rate', 150)  # Speed of speech
        eng.setProperty('volume', 1)  # Volume 0-1
        engine = eng
    return engine

def synthesize_speech(text):
    import tempfile
    eng = get_engine()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        eng.save_to_file(text, tmp_file.name)
        eng.runAndWait()
        return tmp_file.name

# --- Page config ---
st.set_page_config(
    page_title="MedBridge AI Chatbot",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="auto",
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
</style>
""", unsafe_allow_html=True)

# --- Lottie loader ---
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None

lottie_robot = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_gptgkzpu.json")

# --- Avatar display ---
with st.container():
    if show_3d_avatar:
        # External 3D avatar iframe (example Ready Player Me)
        st.markdown(
            """
            <iframe src="https://readyplayer.me/avatar/your-avatar-url" 
            width="300" height="400" frameborder="0" allowfullscreen></iframe>
            """, 
            unsafe_allow_html=True
        )
    else:
        st_lottie(lottie_robot, height=200, key="robot", speed=1)

# --- JavaScript Browser TTS ---
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

# --- Initialize chatbot & chat history ---
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = MedBridgeChatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am MedBridge AI, your personal health assistant. How can I help you today?"
    })

# --- Display chat messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if use_local_tts:
                audio_path = synthesize_speech(msg["content"])
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
                os.remove(audio_path)  # clean up temp file
            else:
                st.markdown(f"<script>speak({repr(msg['content'])})</script>", unsafe_allow_html=True)

# --- Chat input ---
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
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
            os.remove(audio_path)
        else:
            st.markdown(f"<script>speak({repr(response)})</script>", unsafe_allow_html=True)

# --- Download chat history as text ---
if st.sidebar.button("Download chat history"):
    chat_text = "\n\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]
    )
    st.sidebar.download_button(
        label="Download as .txt",
        data=chat_text,
        file_name="medbridge_chat_history.txt",
        mime="text/plain"
    )
