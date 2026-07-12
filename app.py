import streamlit as st
import streamlit.components.v1 as components
import requests
import os

st.set_page_config(page_title="EduGenie AI", page_icon="✨", layout="centered")

# --- CSS ANIMATIONS & HTML EDITOR SKILLS ---
# We inject custom CSS animations to make the headers pulse or move dynamically
custom_html_and_css = """
<style>
    @keyframes pulse {
        0% { transform: scale(1); color: #4f46e5; }
        50% { transform: scale(1.05); color: #ec4899; }
        100% { transform: scale(1); color: #4f46e5; }
    }
    .animated-header {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        animation: pulse 3s infinite;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-family: sans-serif;
    }
</style>
<div class="animated-header">✨ EduGenie AI Platform</div>
<p class="subtitle">FastAPI Core Engine & Streamlit Interface UI</p>
"""

# Render the custom animated HTML component
components.html(custom_html_and_css, height=120)

# Sidebar Feature Selection
feature = st.selectbox(
    "Select an AI/ML Inference Feature:",
    ["Concept Explanation", "Quiz Generation", "Learning Roadmap"]
)
user_prompt = st.text_area("Enter your prompt topic:")

if st.button("Run AI/ML Inference ✨", type="primary"):
    if not user_prompt.strip():
        st.warning("Please provide a prompt!")
    else:
        with st.spinner("Calling FastAPI Local Engine..."):
            try:
                # Directing the request to our FastAPI backend server running locally or on the cloud
                backend_url = "http://127.0.0.1:8000/api/generate"
                payload = {"feature": feature, "prompt": user_prompt}
                
                response = requests.post(backend_url, data=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Inference Complete!")
                    st.markdown("### EduGenie Output:")
                    st.write(data.get("result"))
                else:
                    st.error(f"Backend error: {response.status_code}")
            except Exception as e:
                st.error("Could not connect to FastAPI server. Ensure main.py is running on port 8000.")
