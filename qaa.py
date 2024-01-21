# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) settings
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # You can specify the HTTP methods you want to allow
    allow_headers=["*"],  # You can specify the HTTP headers you want to allow
)

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

class ChatInput(BaseModel):
    question: str

@app.post("/api/get_answer")
async def get_gemini_response(chat_input: ChatInput):
    prompt = """Now remember that you are a health chatbot and only gonna address questions or input is related to health.It can be a 
    diet related question or workout related question, keep you answer plain and simple,please avoid using any special characters in your answer
    and don't share any unnecessary information.Don't add anything to the output which is not asked.If the text input is something not related to health in any way you
    just give output "I don't have information regarding this topic".You read the text given after the alphabet Q and answer to that text as instructed. Q"""
    question = prompt + chat_input.question
    response = chat.send_message(question)

    if response.text == 'NO':
        return {"response": "I'm sorry, I can't provide any information regarding this topic."}

    response_text = "\n".join(chunk.text for chunk in response)
    return {"response": response_text}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
