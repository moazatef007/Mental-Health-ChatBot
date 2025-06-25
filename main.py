from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# استخدم موديل Gemini الصحيح
model = genai.GenerativeModel("models/gemini-1.5-flash")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def ask_bot(req: ChatRequest):
    allowed_keywords = ["اكتئاب", "حزن", "تعب", "قلق", "توتر", "وحدة", "ضغط", "نفسي"]
    if not any(word in req.message for word in allowed_keywords):
        return {
            "response": "أنا بوت متخصص فقط في مواضيع القلق، الاكتئاب، التوتر والحزن. من فضلك اسألني سؤالًا ضمن هذا النطاق ❤️"
        }

    try:
        prompt = f"""أنت مساعد ذكي متخصص في تقديم الدعم النفسي فقط في حالات الحزن، الاكتئاب، التوتر أو القلق. لا تقدم تشخيصًا طبيًا أو نصائح دوائية. كن مستمعًا ودودًا.
        
سؤال المستخدم: {req.message}
"""
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
