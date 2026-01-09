import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Harry's AI Friend Mentor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { background-color: #161b22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown("# 🤖 Harry's AI Friend Mentor")
st.markdown("### Your AI buddy that talks like a friend, acts like a mentor!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Chat with buddy"
if "user_name" not in st.session_state:
    st.session_state.user_name = "Harry"

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.mode = st.radio(
        "What do you need?",
        ["Chat with buddy", "Interview prep", "Daily tasks", "Study help"],
        index=0
    )
    st.session_state.user_name = st.text_input("Your name:", st.session_state.user_name)
    
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("### 📚 Features")
    st.markdown("- 💬 Conversational AI")
    st.markdown("- 🎤 Interview coaching")
    st.markdown("- 📋 Daily planning")
    st.markdown("- 📖 Study help")
    st.divider()
    st.markdown("**💰 Cost:** FREE")
    st.markdown("**🔌 Powered by:** Hugging Face")

# System prompts for different modes
SYSTEM_PROMPTS = {
    "Chat with buddy": """You are Harry's best friend and trusted mentor. You:
- Talk casually and supportively, like a real friend
- Use casual language and friendly tone
- Give honest, practical advice
- Celebrate wins and push him when needed
- Remember context from previous messages
- Use emojis naturally
Be his older brother who gets life, coding, interviews, and everything else.""",
    
    "Interview prep": """You are Harry's interview coach. You:
- Help prepare for tech interviews (DSA, System Design, Behavioral)
- Ask mock interview questions and give feedback
- Explain common patterns and best practices
- Give tips on how to answer behavioral questions
- Help with salary negotiation
- Be encouraging but honest
Make him ready to crush any interview!""",
    
    "Daily tasks": """You are Harry's daily mentor. You:
- Help plan his day effectively
- Motivate him to stay focused
- Celebrate completed tasks
- Push him when he's procrastinating
- Give practical tips for productivity
- Be his accountability partner
Know his goals (fitness, coding, learning) and support them!""",
    
    "Study help": """You are Harry's study buddy and teacher. You:
- Explain BCA concepts simply
- Break down complex topics
- Give real examples
- Test understanding with questions
- Cover: Python, DBMS, Data Structures, Algorithms, etc.
- Encourage learning without giving direct test answers
Make learning fun and easy!"""
}

def get_ai_response(messages_history):
    """Get response from Hugging Face Inference API"""
    API_TOKEN = os.getenv("HF_TOKEN")
    
    if not API_TOKEN:
        return "❌ Error: Hugging Face API token not set. Set HF_TOKEN in environment."
    
    try:
        # Use Hugging Face Inference API with a free model
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        
        # Format messages for the API
        prompt = ""
        
        # Add system prompt
        prompt += f"System: {SYSTEM_PROMPTS.get(st.session_state.mode, SYSTEM_PROMPTS['Chat with buddy'])}\n\n"
        
        # Add conversation history
        for msg in messages_history[-10:]:  # Last 10 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            prompt += f"{role}: {msg['content']}\n"
        
        prompt += "Assistant: "
        
        payload = {"inputs": prompt}
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "I'm thinking... please try again.").split("Assistant: ")[-1].strip()
            else:
                return "I'm thinking... please try again."
        else:
            return f"❌ API Error: {response.status_code}. Please try again in a moment."
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Tell me something..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 💭"):
            response = get_ai_response(st.session_state.messages)
        st.markdown(response)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.divider()
st.markdown("""
<center>
💚 Made with love by Harry | Powered by 🤗 Hugging Face | Hosted on 🚀 Render
</center>
""", unsafe_allow_html=True)
