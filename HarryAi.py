import streamlit as st
import pyttsx3
import time

st.set_page_config(
    page_title="JARVIS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

jarvis_css = """
<style>
    body, .main { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #00d9ff; }
    .jarvis-header { text-align: center; padding: 30px; background: linear-gradient(90deg, rgba(0,217,255,0.1), rgba(255,0,100,0.1)); border: 2px solid #00d9ff; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 0 30px rgba(0,217,255,0.3); }
    .jarvis-title { font-size: 48px; color: #00d9ff; text-shadow: 0 0 20px #00d9ff, 0 0 40px #ff0064; letter-spacing: 3px; }
    .jarvis-subtitle { color: #ff0064; font-size: 18px; letter-spacing: 2px; margin-top: 10px; }
    .chat-bubble-user { text-align: right; color: #00d9ff; padding: 12px 20px; background: rgba(0,217,255,0.15); border-right: 3px solid #00d9ff; border-radius: 8px; margin: 10px 0; }
    .chat-bubble-ai { text-align: left; color: #ff0064; padding: 12px 20px; background: rgba(255,0,100,0.15); border-left: 3px solid #ff0064; border-radius: 8px; margin: 10px 0; }
    .voice-indicator { text-align: center; color: #00d9ff; font-size: 20px; margin: 20px 0; }
    .stButton > button { background: linear-gradient(90deg, #00d9ff, #ff0064) !important; color: #0a0e27 !important; font-weight: bold !important; border-radius: 8px !important; box-shadow: 0 0 15px rgba(0,217,255,0.5) !important; }
    .stButton > button:hover { box-shadow: 0 0 25px rgba(0,217,255,0.8) !important; }
</style>
"""

st.markdown(jarvis_css, unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if "use_voice" not in st.session_state: st.session_state.use_voice = False
if "language" not in st.session_state: st.session_state.language = "English"
if "mode" not in st.session_state: st.session_state.mode = "Chat with buddy"

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

st.markdown("<div class='jarvis-header'><h1 class='jarvis-title'>⚡ JARVIS</h1><p class='jarvis-subtitle'>J.A.R.V.I.S - Harry's AI Response & Voice Interactive System</p></div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Status", "ONLINE", "🔥")
with col2: st.metric("Language", st.session_state.language, "Active")
with col3: st.metric("Voice", "ON" if st.session_state.use_voice else "OFF", "Enabled")
with col4: st.metric("Messages", len(st.session_state.messages), "Total")

st.divider()

with st.expander("⚡ JARVIS SETTINGS", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.language = st.radio("Language:", ["English", "Hindi", "Mix"])
        st.session_state.mode = st.radio("Mode:", ["Chat with buddy", "Interview prep", "Daily tasks", "Study help"])
    with col2:
        st.session_state.use_voice = st.checkbox("🔊 Voice Output", value=False)
        if st.button("🗑️ RESET", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

st.divider()

if st.session_state.use_voice:
    st.markdown("<div class='voice-indicator'>🔊 VOICE ENABLED - LISTENING...</div>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>🗣️ {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

st.divider()

prompt = st.chat_input("🇣️ Enter command...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    mode = st.session_state.mode
    lang = st.session_state.language
    
    if lang == "Hindi":
        if mode == "Chat with buddy": response = f"🙋 Yo! '{prompt}' - bilkul! Main hoon! 💪"
        elif mode == "Interview prep": response = f"🎯 '{prompt}' ke liye: Confident reh, examples de! 🎤"
        elif mode == "Daily tasks": response = f"🏆 '{prompt}' - break kar, hard part pehle! 🤟"
        else: response = f"📚 '{prompt}' - break kar, practice kar! 🌟"
    elif lang == "Mix":
        if mode == "Chat with buddy": response = f"🙋 Yo! You said '{prompt}' - bilkul sahi! 💪"
        elif mode == "Interview prep": response = f"🎯 Great! '{prompt}' ke liye - be confident, examples de! 🎤"
        elif mode == "Daily tasks": response = f"🏆 Let's tackle '{prompt}' - break down, start hard! 🤟"
        else: response = f"📚 Learning '{prompt}'? - Break it, practice it! 🌟"
    else:
        if mode == "Chat with buddy": response = f"Hey! You said '{prompt}' - awesome! 💪"
        elif mode == "Interview prep": response = f"Great! For '{prompt}' - be confident, share examples! 🎤"
        elif mode == "Daily tasks": response = f"Let's tackle '{prompt}' - break down, celebrate wins! 🏆"
        else: response = f"Learning '{prompt}'? - Break it, practice it! 📚"
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    if st.session_state.use_voice: speak(response)
    st.rerun()

st.divider()
st.markdown("<div style='text-align:center; color:#00d9ff; margin-top:30px;'><p style='font-size:12px;'>⚡ JARVIS ONLINE ⚡</p><p style='font-size:10px; color:#ff0064;'>Made by Harry | Powered by Streamlit</p></div>", unsafe_allow_html=True)
