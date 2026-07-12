import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = FastAPI(title="EduGenie Core Engine Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from configuration.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.5-flash')

@app.post("/api/v1/predict")
async def process_educational_request(feature: str = Form(...), prompt: str = Form(...)):
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Payload input cannot be empty.")

    if "Explanation" in feature:
        system_context = f"System: Act as an expert academic tutor. Explain clearly: {prompt}"
    elif "Quiz" in feature:
        system_context = f"System: Act as an academic evaluation system. Generate a 3-question multiple choice quiz on: {prompt}"
    else:
        system_context = f"System: Act as an educational consultant. Create a detailed learning roadmap for: {prompt}"

    try:
        response = model.generate_content(system_context)
        return {"status": "success", "data": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Make sure your terminal command matches this file name exactly!
    uvicorn.run("backend_api:app", host="0.0.0.0", port=8000, reload=True)