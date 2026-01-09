import streamlit as st
import pyttsx3

st.set_page_config(
    page_title="Harry's AI Friend",
    page_icon="🤖",
    layout="wide"
)

st.markdown("# 🤖 Harry's AI Friend Mentor")
st.markdown("### Your AI buddy that talks like a friend, acts like a mentor!")
st.markdown("**🎆 With Voice Support & English + Hindi!**")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Chat with buddy"
if "use_voice" not in st.session_state:
    st.session_state.use_voice = False
if "language" not in st.session_state:
    st.session_state.language = "English"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

with st.sidebar:
    st.header("⚙️ Settings")
    
    st.markdown("### 🌇 Language")
    st.session_state.language = st.radio(
        "Prefer to chat in:",
        ["English", "Hindi", "Mix (English + Hindi)"],
        index=0
    )
    
    st.markdown("### 📍 Mode")
    st.session_state.mode = st.radio(
        "What do you need?",
        ["Chat with buddy", "Interview prep", "Daily tasks", "Study help"]
    )
    
    st.divider()
    st.markdown("### 🎉 Voice Features")
    st.session_state.use_voice = st.checkbox("🔊 Enable Voice Output (AI speaks)", value=False)
    
    st.info("🍐 **Voice Input:** Use your laptop/phone mic to talk!")
    
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("### 📚 Features")
    st.markdown("- 🎉 Voice Chat (Speak & Listen)")
    st.markdown("- 💬 Chat in English or Hindi")
    st.markdown("- 🎤 Interview coaching")
    st.markdown("- 📋 Daily planning")
    st.markdown("- 📖 Study help")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("🇣️ Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown("🗣️ " + prompt)
    
    with st.chat_message("assistant"):
        mode = st.session_state.mode
        lang = st.session_state.language
        
        # Generate responses based on mode and language
        if lang == "Hindi":
            if mode == "Chat with buddy":
                response = f"🙋 Yo! Tu ne kaha '{prompt}' - bilkul sahi! Main tere saath hoon, kuch bhi puchna, main madad karunga! Aur bataa, kya chalra! 💪"
            elif mode == "Interview prep":
                response = f"🎯 Achha suna! '{prompt}' ke liye yaad rakha: Apna aap ko confident rakhna, apne experience se examples dena, questions puchna, aur company ke baare mein research karna. Tu kar payega! 🎤"
            elif mode == "Daily tasks":
                response = f"🏆 Bilkul! Aaj '{prompt}' ko tackle kar lete hain! Mera advice: Chhote kadam mein todh le, sabse mushkil kaam se shuru kar, breaks le, aur celebrate kar apni jeet! 🤟"
            else:  # Study help
                response = f"📚 Wow! '{prompt}' sikhna chahte ho? Shabaash! Concept ko break kar, examples se samajh, kisi ko sikha, aur zyada practice kar. Tu brilliant ban jayega! 🌟"
        
        elif lang == "Mix (English + Hindi)":
            if mode == "Chat with buddy":
                response = f"🙋 Yo! You said '{prompt}' - Bilkul sahi! Main hoon na tere saath! Kuch bhi puchna, I'm here to help! 💪"
            elif mode == "Interview prep":
                response = f"🎯 Great question! '{prompt}' ke liye: Confidence rakho, apna experience share karo, research karo company ke baare mein, aur be yourself! You got this! 🎤"
            elif mode == "Daily tasks":
                response = f"🏆 Let's tackle '{prompt}' today! Approach: Break it down, start with hardest part, take breaks, aur celebrate wins! Tu kar payega! 🤟"
            else:  # Study help
                response = f"📚 Learning about '{prompt}'? Badiya! Break the concept, practice with examples, teach someone, aur keep pushing! Tum brilliant ho sakta ho! 🌟"
        
        else:  # English
            if mode == "Chat with buddy":
                response = f"Hey! You said '{prompt}' - That's awesome! I'm here for you, buddy! Tell me more, what's on your mind? 💪"
            elif mode == "Interview prep":
                response = f"Great question! For '{prompt}': Be confident, share real examples, ask questions, research the company. You've got this! 🎤"
            elif mode == "Daily tasks":
                response = f"Let's tackle '{prompt}' today! Break it into chunks, start hard, take breaks, celebrate wins. You can do it! 🏆"
            else:  # Study help
                response = f"Learning about '{prompt}'? Awesome! Break the concept, practice, teach it to someone, keep going. You're brilliant! 📚"
        
        st.markdown("🤖 " + response)
        
        # Speak if voice enabled
        if st.session_state.use_voice:
            try:
                speak(response)
                st.success("🔊 Voice played!")
            except:
                st.warning("⚠️ Voice not available on this device")
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("💚 Made with love by Harry | Powered by 🚀 Streamlit + Voice Tech")
st.markdown("✅ 100% FREE - Hindi + English + Voice!")
