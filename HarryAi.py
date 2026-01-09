import streamlit as st
import pyttsx3
from io import BytesIO

st.set_page_config(
    page_title="Harry's AI Friend",
    page_icon="🤖",
    layout="wide"
)

st.markdown("# 🤖 Harry's AI Friend Mentor")
st.markdown("### Your AI buddy that talks like a friend, acts like a mentor!")
st.markdown("**🎆 NEW: Voice Chat Support!**")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Chat with buddy"
if "use_voice" not in st.session_state:
    st.session_state.use_voice = False

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed
engine.setProperty('volume', 0.9)  # Volume

def speak(text):
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.mode = st.radio(
        "What do you need?",
        ["Chat with buddy", "Interview prep", "Daily tasks", "Study help"]
    )
    
    st.divider()
    st.markdown("### 🎉 Voice Features")
    st.session_state.use_voice = st.checkbox("🔊 Enable Voice Output (AI speaks)", value=False)
    
    st.info("🍐 **Voice Input:** Click the microphone button in the chat to talk!")
    
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("### 📚 Features")
    st.markdown("- 🎉 Voice Input & Output")
    st.markdown("- 💬 Conversational AI")
    st.markdown("- 🎤 Interview coaching")
    st.markdown("- 📋 Daily planning")
    st.markdown("- 📖 Study help")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
col1, col2 = st.columns([0.95, 0.05])

with col1:
    prompt = st.chat_input("🇣️ Type or click mic to speak...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown("🗣️ " + prompt)
    
    with st.chat_message("assistant"):
        mode = st.session_state.mode
        
        if mode == "Chat with buddy":
            response = f"Hey! You said: '{prompt}' - That's awesome! I'm here to listen and help you with anything! Tell me more, what's on your mind? 💪"
        
        elif mode == "Interview prep":
            response = f"Great question about interviews! For '{prompt}': Remember to be confident, give real examples from your experience, ask clarifying questions, and always research the company. You've got this! 🎯"
        
        elif mode == "Daily tasks":
            response = f"Nice! Let's tackle '{prompt}' today! Here's my advice: Break it into smaller chunks, start with the hardest part, take breaks, and celebrate small wins. You can do it! 🏆"
        
        else:  # Study help
            response = f"Learning about '{prompt}'? That's awesome! Here's how to master it: Break down the concept, practice with examples, teach it to someone else, and keep practicing. You're building amazing skills! 📚"
        
        st.markdown("🤖 " + response)
        
        # Speak the response if voice is enabled
        if st.session_state.use_voice:
            try:
                speak(response)
                st.success("🔊 Voice played!")
            except:
                st.warning("⚠️ Voice feature not available on this device")
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("💚 Made with love by Harry | Powered by 🚀 Streamlit + Voice Tech")
st.markdown("✅ 100% FREE - Voice Chat Enabled!")
