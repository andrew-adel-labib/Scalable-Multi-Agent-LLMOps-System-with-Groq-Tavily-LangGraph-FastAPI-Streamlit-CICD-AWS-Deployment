import requests
import streamlit as st
from pathlib import Path
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi-Agent LLMOps", layout="wide", page_icon="🤖")

css_path = Path(__file__).parent / "assets" / "style.css"
html_path = Path(__file__).parent / "assets" / "template.html"

with open(css_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open(html_path, encoding="utf-8") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

system_prompt = st.text_area("🧠 Define your AI agent:", height=80)
selected_model = st.selectbox("🧩 Select AI Model:", settings.ALLOWED_MODEL_NAMES)
allow_web_search = st.checkbox("🌐 Allow Web Search")
user_query = st.text_area("💬 Enter your query:", height=180)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("🚀 Ask Agent") and user_query.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    try:
        logger.info("Sending request to backend...")

        with st.spinner("🤖 The AI agent is thinking..."):
            response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend.")

            st.markdown('<div class="response-box"><h4>🧩 Agent Response</h4>', unsafe_allow_html=True)
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Backend returned an error.")
    except Exception as e:
        st.error(str(CustomException("Failed to communicate with backend", error_detail=e)))

st.markdown(
    """
    <div class="footer">
        Developed by <span class="author-name">Andrew Adel</span>
    </div>
    """,
    unsafe_allow_html=True
)
