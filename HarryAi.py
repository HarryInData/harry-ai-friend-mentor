import streamlit as st
import pyttsx3
from groq import Groq
import speech_recognition as sr
import requests
from datetime import datetime
import json

# Initialize Groq Client
client = Groq(api_key="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")

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def get_voice_input():
    """Capture voice input from user"""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎶 Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except Exception as e:
        st.error(f"Microphone error: {str(e)}")
        return None

def search_internet(query):
    """Search internet for real-time information"""
    try:
        url = f"https://www.bing.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

def get_ai_response(user_message, context=""):
    """Get intelligent response from Groq AI with context awareness"""
    try:
        system_prompt = f"""
You are an advanced AI Assistant named {st.session_state.get('bot_name', 'JARVIS')}.
You are intelligent, helpful, and solve user problems completely.
{f'Additional Context: {context}' if context else ''}
Provide accurate, detailed, and actionable responses.
If you don't know something, search suggestions are provided.
"""
        
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Page Configuration
st.set_page_config(
    page_title="Advanced AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS Styling
advanced_css = """
<style>
    * { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    body, .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
    }
    
    .main { background-attachment: fixed; }
    
    .stChatMessage {
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stChatMessage.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-left: 4px solid #00d9ff;
    }
    
    .stChatMessage.assistant {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-left: 4px solid #f5576c;
    }
    
    .header-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .header-title {
        font-size: 3em;
        font-weight: 900;
        background: linear-gradient(135deg, #00d9ff, #ff0064);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0,217,255,0.5);
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1.2em;
        color: #ff0064;
        margin-top: 10px;
        letter-spacing: 2px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: 2px solid #00d9ff !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,217,255,0.5) !important;
    }
    
    .metric-card {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
    }
    
    .input-section {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        border: 2px solid rgba(0,217,255,0.3);
        margin: 20px 0;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 2px solid #00d9ff !important;
        border-radius: 10px !important;
    }
    
    .response-box {
        background: linear-gradient(135deg, rgba(0,217,255,0.1), rgba(255,0,100,0.1));
        border-left: 4px solid #00d9ff;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
</style>
"""

st.markdown(advanced_css, unsafe_allow_html=True)

# Initialize Session State
if "bot_name" not in st.session_state:
    st.session_state.bot_name = "JARVIS"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = ""

# Header
st.markdown("""
<div class='header-container'>
    <h1 class='header-title'>⚡ JARVIS</h1>
    <p class='header-subtitle'>Advanced AI Assistant - ChatGPT Alternative</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Bot Name
    new_name = st.text_input("Bot Name:", value=st.session_state.bot_name)
    if new_name != st.session_state.bot_name:
        st.session_state.bot_name = new_name
        speak(f"Hello! I'm {new_name} now!")
    
    # Voice Mode Toggle
    st.session_state.voice_mode = st.checkbox("🎶 Enable Voice", value=st.session_state.voice_mode)
    
    # Clear Chat History
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_context = ""
        st.success("Chat cleared!")
    
    st.divider()
    st.markdown("### 📚 About")
    st.info(
        f"""**{st.session_state.bot_name}** - An advanced AI assistant powered by Groq AI.
        
        Features:
        ✅ Voice Input & Output
        ✅ Internet Search Integration
        ✅ Problem Solving
        ✅ Context Awareness
        ✅ ChatGPT-like Interface
        """
    )

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📋 Status", "Online", "🔥")
with col2:
    st.metric("🤖 Bot", st.session_state.bot_name, "Active")
with col3:
    st.metric("🧠 AI", "Groq", "Advanced")
with col4:
    st.metric("💬 Messages", len(st.session_state.messages), "Total")

st.divider()

# Chat Display
st.markdown("### 🗣️ Conversation")
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])

st.divider()

# Input Section
st.markdown("### 🔍 Ask Me Anything")

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    user_input = st.chat_input("💬 Type your question...")

with col2:
    if st.button("🎶 Voice", use_container_width=True):
        if st.session_state.voice_mode:
            voice_text = get_voice_input()
            if voice_text:
                user_input = voice_text
                st.success(f"✅ Heard: {voice_text}")
        else:
            st.warning("🔊 Voice mode disabled")

with col3:
    if st.button("🔊 Speak", use_container_width=True):
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
            speak(st.session_state.messages[-1]["content"])
            st.success("✅ Speaking...")

# Process User Input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("🤖 Thinking..."):
        response = get_ai_response(user_input, st.session_state.conversation_context)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_context += f"\nUser: {user_input}\nAssistant: {response}"
    
    # Auto-speak response if voice mode
    if st.session_state.voice_mode:
        speak(response)
    
    st.rerun()

st.divider()
st.markdown("""
<div style='text-align:center; margin-top:40px; padding:20px; background:rgba(255,255,255,0.05); border-radius:10px;'>
    <p style='font-size:14px; color:#00d9ff;'>⚡ <b>{}</b> - ChatGPT Alternative ⚡</p>
    <p style='font-size:12px; color:#ff0064;'>Powered by Groq AI | Voice Enabled | Context Aware</p>
    <p style='font-size:10px; color:#888;'>Created for Advanced Problem Solving</p>
</div>
""".format(st.session_state.bot_name), unsafe_allow_html=True)
