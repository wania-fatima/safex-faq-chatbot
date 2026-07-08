"""
ui/app.py
---------
Streamlit web interface for the SafeX FAQ Chatbot.

Run with:
    streamlit run ui/app.py
(from the project root folder, with dependencies from requirements.txt installed)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from chatbot import SafeXFAQChatbot

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
ICON_PATH = os.path.join(ASSETS_DIR, "icon.png")

st.set_page_config(page_title="SafeX FAQ Chatbot", page_icon=ICON_PATH, layout="centered")

st.image(ICON_PATH, width=110)
st.title("SafeX FAQ Chatbot")
st.write("Welcome to the SafeX FAQ Chatbot! Ask me any question related to SafeX.")


@st.cache_resource
def load_bot():
    return SafeXFAQChatbot()


bot = load_bot()

if "history" not in st.session_state:
    st.session_state.history = []

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.write(text)

user_input = st.chat_input("Ask a question about SafeX")

if user_input:
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    result = bot.get_response(user_input)

    with st.chat_message("assistant"):
        st.write(result["answer"])

    st.session_state.history.append(("assistant", result["answer"]))
