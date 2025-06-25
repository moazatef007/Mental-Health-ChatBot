from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            "أنت مساعد ذكي مختص فقط في مواضيع الحزن، القلق، التوتر، والاكتئاب. كن متعاطف وودود، لا تقدم نصائح طبية ولا تشخيص، فقط قدم دعم نفسي."
        ]
    }
])

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def ask_bot(req: ChatRequest):
    allowed_keywords = ["اكتئاب", "حزن", "تعب", "قلق", "توتر", "وحدة", "ضغط", "نفسي"]
    try:
        if not any(word in req.message for word in allowed_keywords) and len(chat.history) <= 1:
            return {
                "response": "أنا بوت متخصص في مواضيع القلق، الحزن، الاكتئاب والتوتر فقط. ممكن تحكيلي أكتر عن شعورك؟ ❤️"
            }

        response = chat.send_message(req.message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
