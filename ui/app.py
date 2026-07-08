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
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from chatbot import SafeXFAQChatbot

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
ICON_PATH = os.path.join(ASSETS_DIR, "icon.png")

st.set_page_config(page_title="SafeX FAQ Chatbot", page_icon=ICON_PATH, layout="wide")


@st.cache_resource
def load_bot():
    return SafeXFAQChatbot()


bot = load_bot()

if "history" not in st.session_state:
    st.session_state.history = []

# Quick example questions grouped by category, pulled from the real dataset
QUICK_QUESTIONS = {
    "About & Careers": [
        "Tell me about SafeX Solutions",
        "Does SafeX Solutions offer internships?",
        "Does SafeX Solutions offer careers or jobs?",
    ],
    "Services": [
        "What services does SafeX Solutions offer?",
        "Does SafeX offer cybersecurity services?",
        "Do you build websites?",
    ],
    "Products & Contact": [
        "What products has SafeX built?",
        "How can I contact SafeX Solutions?",
        "What is URL2Video.online?",
    ],
}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image(ICON_PATH, width=60)
    st.markdown("### Quick Questions")

    for group_name, questions in QUICK_QUESTIONS.items():
        st.markdown(f"**{group_name}**")
        for q in questions:
            if st.button(q, key=f"quick_{q}", use_container_width=True):
                st.session_state.pending_question = q
        st.markdown("")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    with col2:
        chat_text = "\n\n".join(
            f"{'You' if role == 'user' else 'Bot'}: {text}" for role, text in st.session_state.history
        )
        st.download_button(
            "⬇️ Export",
            data=chat_text if chat_text else "No conversation yet.",
            file_name=f"safex_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# ---------------- HEADER ----------------
import base64
with open(ICON_PATH, "rb") as _f:
    _icon_b64 = base64.b64encode(_f.read()).decode()

st.markdown(
    f"""
    <div style="
        background: linear-gradient(90deg, #1F4E79, #2E86C1);
        padding: 20px 28px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
    ">
        <img src="data:image/png;base64,{_icon_b64}" style="height: 48px; width: auto;" />
        <div>
            <h2 style="color: white; margin: 0;">SafeX Solutions FAQ Chatbot</h2>
            <p style="color: #DCE9F5; margin: 4px 0 0 0;">
                Ask me anything about SafeX Solutions — services, products, contact info, or internships.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- CHAT HISTORY ----------------
if not st.session_state.history:
    with st.chat_message("assistant"):
        st.write(
            "Hello! I'm the **SafeX Solutions** assistant. Ask me about our **services, "
            "contact details, careers,** and **company information**.\n\n"
            "Try a quick question from the sidebar, or type your own below."
        )

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.write(text)

# ---------------- HANDLE INPUT ----------------
user_input = st.chat_input("Ask a question about SafeX")

# A sidebar quick-question button click also counts as input
if "pending_question" in st.session_state:
    user_input = st.session_state.pending_question
    del st.session_state.pending_question

if user_input:
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    result = bot.get_response(user_input)

    with st.chat_message("assistant"):
        st.write(result["answer"])

    st.session_state.history.append(("assistant", result["answer"]))
    st.rerun()
