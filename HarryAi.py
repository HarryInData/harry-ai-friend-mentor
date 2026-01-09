import streamlit as st
import pyttsx3
from groq import Groq
import os

client = Groq(api_key="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")

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def get_ai_response(user_message):
    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

st.set_page_config(page_title="JARVIS AI", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

jarvis_css = """<style>
body, .main { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #00d9ff; }
.jarvis-header { text-align: center; padding: 30px; background: linear-gradient(90deg, rgba(0,217,255,0.1), rgba(255,0,100,0.1)); border: 2px solid #00d9ff; border-radius: 15px; box-shadow: 0 0 30px rgba(0,217,255,0.3); }
.jarvis-title { font-size: 48px; color: #00d9ff; text-shadow: 0 0 20px #00d9ff, 0 0 40px #ff0064; letter-spacing: 3px; }
.chat-bubble-user { text-align: right; color: #00d9ff; padding: 12px 20px; background: rgba(0,217,255,0.15); border-right: 3px solid #00d9ff; border-radius: 8px; margin: 10px 0; }
.chat-bubble-ai { text-align: left; color: #ff0064; padding: 12px 20px; background: rgba(255,0,100,0.15); border-left: 3px solid #ff0064; border-radius: 8px; margin: 10px 0; }
.stButton > button { background: linear-gradient(90deg, #00d9ff, #ff0064) !important; color: #0a0e27 !important; font-weight: bold !important; border-radius: 8px !important; }
</style>"""

st.markdown(jarvis_css, unsafe_allow_html=True)

if "bot_name" not in st.session_state:
    st.session_state.bot_name = "JARVIS"
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(f"<div class='jarvis-header'><h1 class='jarvis-title'>⚡ {st.session_state.bot_name}</h1><p style='color:#ff0064;'>AI Powered Intelligent Assistant</p></div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Status", "ONLINE", "🔥")
with col2: st.metric("Bot", st.session_state.bot_name, "Active")
with col3: st.metric("AI", "Groq", "🧠")
with col4: st.metric("Messages", len(st.session_state.messages), "Total")

st.divider()

with st.expander("⚡ SETTINGS", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Change Bot Name:", value=st.session_state.bot_name)
        if new_name and new_name != st.session_state.bot_name:
            st.session_state.bot_name = new_name
            speak(f"Hello! I am now {new_name}")
            st.success(f"✅ Bot renamed to: {new_name}")
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

st.divider()

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>🗣️ {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

st.divider()

user_input = st.chat_input("💬 Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("🤖 Thinking..."):
        response = get_ai_response(user_input)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    speak(response)
    st.rerun()

st.divider()
st.markdown(f"<div style='text-align:center; color:#00d9ff;'><p>⚡ {st.session_state.bot_name} - AI POWERED ⚡</p><p style='font-size:10px; color:#ff0064;'>Powered by Groq</p></div>", unsafe_allow_html=True)
