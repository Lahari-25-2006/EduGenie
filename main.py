import os
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI(title="EduGenie Core AI Engine")

# Enable CORS so Streamlit can communicate seamlessly with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/api/generate")
async def generate_educational_content(feature: str = Form(...), prompt: str = Form(...)):
    # --- PROMPT ENGINEERING & NATURAL LANGUAGE PROCESSING (NLP) SKILLS ---
    if "Explanation" in feature:
        system_prompt = f"System: Act as an expert tutor. Use NLP methodologies to simplify complex concepts. Task: Explain clearly: {prompt}"
    elif "Quiz" in feature:
        system_prompt = f"System: Act as an academic evaluation unit. Task: Generate a 3-question multiple choice quiz on: {prompt}"
    else:
        system_prompt = f"System: Act as a curriculum architect. Task: Create a step-by-step learning path for: {prompt}"
        
    try:
        # Run AI/ML Inference
        response = model.generate_content(system_prompt)
        return {"status": "success", "result": response.text}
    except Exception as e:
        return {"status": "error", "result": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
