import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API URL
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Function to query Groq API
def chat_with_groq(messages, model="llama3-70b-8192", temperature=0.7):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        reply = result['choices'][0]['message']['content']
        return reply
    else:
        return f"Error {response.status_code}: {response.text}"

# Streamlit app UI
st.title("💬 AI Chatbot Powered by Groq LLM")
st.caption("Built with LLaMA 3 via Groq API")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI chatbot."}
    ]

# Display chat history
for message in st.session_state.messages[1:]:
    if message["role"] == "user":
        st.write(f"🧑 You: {message['content']}")
    else:
        st.write(f"🤖 Bot: {message['content']}")

# User input
user_input = st.text_input("Your message:", key="user_input")

if st.button("Send"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = chat_with_groq(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()