import streamlit as st

st.set_page_config(
    page_title="Harry's AI Friend",
    page_icon="🤖",
    layout="wide"
)

st.markdown("# 🤖 Harry's AI Friend Mentor")
st.markdown("### Your AI buddy that talks like a friend, acts like a mentor!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Chat with buddy"

with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.mode = st.radio(
        "What do you need?",
        ["Chat with buddy", "Interview prep", "Daily tasks", "Study help"]
    )
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("### 📚 Features")
    st.markdown("- 💬 Conversational AI")
    st.markdown("- 🎤 Interview coaching")
    st.markdown("- 📋 Daily planning")
    st.markdown("- 📖 Study help")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tell me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
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
        
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("💚 Made with love by Harry | Powered by 🚀 Streamlit + Render")
st.markdown("✅ 100% FREE - No API keys required!")
