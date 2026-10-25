from __future__ import annotations
import os
from pathlib import Path
import urllib.request
import json

class AIService:
    def __init__(self):
        env_path = Path(__file__).resolve().parent.parent.parent / ".env"
        self.api_key = os.getenv("GEMINI_API_KEY", "")

        if not self.api_key and env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        self.api_key = line.split("=", 1)[1].strip()
                        break

    def generate_chat_response(self, question: str, retrieved_context: list[str], prior_message_count: int = 0) -> str:
        if not self.api_key:
            return "Gemini API key not configured in .env file."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"You are CampusMind AI, an intelligent academic assistant. Answer accurately and clearly: {question}"}]
            }]
        }

        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Gemini API Error: {str(e)}"

    def build_summary(self, text: str, summary_type: str = "short") -> dict:
        return {"summary": "Summary processed."}