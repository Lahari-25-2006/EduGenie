import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os

# Page Configuration
st.set_page_config(
    page_title="EduGenie Dashboard", 
    page_icon="🎓", 
    layout="centered"
)

# --- INJECTING RAW HTML & CUSTOM CSS KEYFRAME ANIMATIONS ---
ui_header_html = """
<style>
    @keyframes smoothGlow {
        0% { color: #6366f1; text-shadow: 0 0 5px rgba(99, 102, 241, 0.2); }
        50% { color: #a855f7; text-shadow: 0 0 15px rgba(168, 85, 247, 0.4); }
        100% { color: #6366f1; text-shadow: 0 0 5px rgba(99, 102, 241, 0.2); }
    }
    .main-title {
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        letter-spacing: -0.5px;
        animation: smoothGlow 4s ease-in-out infinite;
    }
    .description {
        text-align: center;
        font-family: system-ui, sans-serif;
        color: #475569;
        font-size: 15px;
        margin-top: -5px;
        margin-bottom: 25px;
    }
</style>
<div class="main-title">EduGenie Intelligent Assistant</div>
<div class="description">Production Architecture: Integrated Generative AI Processing Interface</div>
"""

# Render animated banner
components.html(ui_header_html, height=100)

# Securely grab the API key from deployment environment secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.info("System Configuration Required: Please attach your GEMINI_API_KEY in the cloud deployment settings dashboard.", icon="🔑")
else:
    # Initialize the client engine
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Functional selection inputs
    feature = st.selectbox(
        "Choose System Modality / Action:",
        ["Concept Explanation", "Quiz Generation", "Learning Roadmap"]
    )

    placeholder_map = {
        "Concept Explanation": "e.g., Explain Pythagoras Theorem or Which is the largest ocean?",
        "Quiz Generation": "e.g., Oceans and Rivers or Basic Python Loops",
        "Learning Roadmap": "e.g., SQL Databases or Introduction to Machine Learning"
    }

    user_input = st.text_area("What would you like to learn?", placeholder=placeholder_map[feature])

    st.markdown("---")

    if st.button("Execute Core Inference ✨", type="primary"):
        if not user_input.strip():
            st.warning("Input prompt workspace cannot be left blank.")
        else:
            with st.spinner("Processing NLP Token Streams via Gemini Engine..."):
                # --- PROMPT ENGINEERING & NATURAL LANGUAGE PROCESSING (NLP) ---
                if "Explanation" in feature:
                    system_context = (
                        f"System: Act as an expert academic tutor. Break down the concept using simple terms, "
                        f"provide real-world analogies, and add necessary context.\n"
                        f"Task: Explain this clearly: {user_input}"
                    )
                elif "Quiz" in feature:
                    system_context = (
                        f"System: Act as an academic evaluation system. Generate a structured 3-question "
                        f"multiple-choice quiz (A, B, C, D) based on the topic. Provide answers clearly separate at the end.\n"
                        f"Task: Generate quiz for: {user_input}"
                    )
                elif "Roadmap" in feature:
                    system_context = (
                        f"System: Act as an educational consultant. Provide a detailed, step-by-step learning roadmap "
                        f"divided into Beginner, Intermediate, and Advanced tiers with actionable resource tips.\n"
                        f"Task: Create roadmap for: {user_input}"
                    )

                try:
                    response = model.generate_content(system_context)
                    st.success("Data Inference Complete!")
                    st.info(f"Modality Applied: {feature}")
                    
                    st.markdown("### 📋 EduGenie Output Results")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Inference Engine Failure: {str(e)}")
