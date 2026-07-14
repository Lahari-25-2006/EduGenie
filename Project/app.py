import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables (for local testing)
load_dotenv()

# Configure Gemini API Key securely
# It checks your Streamlit Secrets first (for cloud), then falls back to local .env
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing Gemini API Key. Please configure it in your Secrets or .env file.")
else:
    genai.configure(api_key=api_key)

# 1. Set up page configuration
st.set_page_config(
    page_title="EduGenie - AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)

# 2. Sidebar Navigation Interface (Organized Student Style)
st.sidebar.title("🎒 EduGenie Menu")
st.sidebar.markdown("Choose a feature to start learning:")
choice = st.sidebar.radio(
    "Navigation",
    [
        "🤖 Intelligent Q&A",
        "💡 Concept Explanations",
        "📝 AI Quiz Generator",
        "📚 Text Summarization",
        "🎯 Learning Path Recommendations"
    ]
)

st.sidebar.info("Designed as an AI-powered student companion tool.")

# Instantiate the Gemini model
model = genai.GenerativeModel("gemini-3.5-flash")

# --- FEATURE 1: INTELLIGENT QUESTION ANSWERING ---
if choice == "🤖 Intelligent Q&A":
    st.title("🤖 Intelligent Question Answering")
    st.caption("Get clear, accurate answers to any academic questions instantly.")
    
    user_query = st.text_input("Enter your question here:", placeholder="e.g., Why is the sky blue?")
    if st.button("Ask EduGenie"):
        if user_query:
            with st.spinner("Analyzing and finding answers..."):
                prompt = f"Act as an encouraging academic tutor. Answer the following question thoroughly but in easy-to-understand language: {user_query}"
                response = model.generate_content(prompt)
                st.success("Here is your answer:")
                st.write(response.text)
        else:
            st.warning("Please type a question first!")

# --- FEATURE 2: SIMPLIFIED CONCEPT EXPLANATIONS ---
elif choice == "💡 Concept Explanations":
    st.title("💡 Simplified Concept Explanations")
    st.caption("Break down complex, scary topics into simple, digestible words.")
    
    concept = st.text_input("What concept do you want to learn?", placeholder="e.g., Quantum Computing, Photosynthesis")
    level = st.selectbox("Explain it like I am a:", ["5-year-old", "High School Student", "College Student"])
    
    if st.button("Simplify Concept"):
        if concept:
            with st.spinner("Simplifying logic..."):
                prompt = f"Explain the concept of '{concept}' tailored exactly for a {level}. Use real-world analogies, simple terms, and keep it highly engaging."
                response = model.generate_content(prompt)
                st.success(f"Explanation for a {level}:")
                st.write(response.text)
        else:
            st.warning("Please enter a concept name!")

# --- FEATURE 3: AI-POWERED QUIZ GENERATION ---
elif choice == "📝 AI Quiz Generator":
    st.title("📝 AI-Powered Quiz Generation")
    st.caption("Test your knowledge by generating customized pop-quizzes on any topic.")
    
    quiz_topic = st.text_input("Enter quiz topic/subject:", placeholder="e.g., Indian History, Python Functions")
    num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
    
    if st.button("Generate Quiz"):
        if quiz_topic:
            with st.spinner("Formulating test questions..."):
                prompt = f"Create a quiz with {num_questions} Multiple Choice Questions (MCQs) on the topic: {quiz_topic}. Include options (A, B, C, D) and provide the correct answers clearly hidden at the very bottom so the student can test themselves."
                response = model.generate_content(prompt)
                st.success("Your Test Paper is Ready!")
                st.write(response.text)
        else:
            st.warning("Please enter a topic for the quiz!")

# --- FEATURE 4: EDUCATIONAL TEXT SUMMARIZATION ---
elif choice == "📚 Text Summarization":
    st.title("📚 Educational Text Summarization")
    st.caption("Paste long paragraphs, textbook pages, or essays to extract quick summary notes.")
    
    long_text = st.text_area("Paste your long textbook content or notes here:", height=250)
    summary_style = st.radio("Choose Summary Style:", ["Quick Bullet Points", "Short Detailed Paragraph"])
    
    if st.button("Summarize Content"):
        if long_text:
            with st.spinner("Condensing text..."):
                prompt = f"Summarize the following educational text in the style of '{summary_style}'. Highlight the core key takeaways clearly:\n\n{long_text}"
                response = model.generate_content(prompt)
                st.success("Summary Generated:")
                st.write(response.text)
        else:
            st.warning("Please paste some text first!")

# --- FEATURE 5: PERSONALIZED LEARNING PATH RECOMMENDATIONS ---
elif choice == "🎯 Learning Path Recommendations":
    st.title("🎯 Personalized Learning Path Recommendations")
    st.caption("Tell EduGenie your learning goal, and get a structured, step-by-step roadmap.")
    
    goal = st.text_input("What skill or subject do you want to master?", placeholder="e.g., Data Science in 3 months, Web Development from scratch")
    time_commitment = st.text_input("How many hours per week can you study?", placeholder="e.g., 5 hours/week")
    
    if st.button("Build Roadmap"):
        if goal:
            with st.spinner("Mapping out your curriculum..."):
                prompt = f"Act as a professional academic advisor. Create a highly structured, weekly step-by-step learning roadmap to master: '{goal}'. Consider that the student has a time commitment of {time_commitment}. Recommend free topics to study and actionable milestones."
                response = model.generate_content(prompt)
                st.success("Your Personalized Roadmap:")
                st.write(response.text)
        else:
            st.warning("Please enter a learning goal!")