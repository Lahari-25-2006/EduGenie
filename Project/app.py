import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(page_title="EduGenie Core Engine", page_icon="✨", layout="centered")

# Custom Title Animation (Matching your previous design!)
st.markdown("""
    <style>
    .title-text {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #FF4B4B, #FF8F8F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.02); }
    }
    </style>
    <h1 class="title-text">EduGenie Core Engine ✨</h1>
""", unsafe_allow_html=True)

# Fetch API Key directly
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 GEMINI_API_KEY is missing from your .env file setup!")
else:
    # Initialize the Google GenAI connection inside Streamlit directly
    genai.configure(api_key=api_key)
    # Using the current production-supported model version
    model = genai.GenerativeModel('gemini-3.5-flash')

    # Dropdown feature mapping matching your backend options
    feature = st.selectbox(
        "Select Core Inference Pipeline Feature Mode:",
        ["Academic Explanation Engine", "Automated Quiz Generator", "Learning Roadmap Designer"]
    )

    # Text Input Prompt area
    user_input = st.text_input("Enter your core instruction NLP text corpus script query:", "")

    # Execution Trigger Button
    if st.button("Execute Core Inference ✨"):
        if not user_input.strip():
            st.warning("Please enter a valid prompt topic before executing inference.")
        else:
            # Recreate the exact backend prompt contexts natively
            if "Explanation" in feature:
                system_context = f"System: Act as an expert academic tutor. Explain clearly: {user_input}"
            elif "Quiz" in feature:
                system_context = f"System: Act as an academic evaluation system. Generate a 3-question multiple choice quiz on: {user_input}"
            else:
                system_context = f"System: Act as an educational consultant. Create a detailed learning roadmap for: {user_input}"

            with st.spinner("Processing prompt query directly through Gemini Engine pipeline..."):
                try:
                    # Generate content directly on the frontend panel layout
                    response = model.generate_content(system_context)
                    
                    st.success("Data Inference Complete!")
                    st.markdown("### 📋 Generated Educational Content Output:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Inference Processing Error: {e}")