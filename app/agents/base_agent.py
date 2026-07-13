from openai import  OpenAI
from app.config import settings

class BaseAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )
        self.model = settings.LLM_MODEL

    def chat(self, message:str,system_prompt:str = None)->str:
        messages=[]
        if system_prompt :
            messages.append({"role":"system","content":system_prompt})
        messages.append({"role":"user","content":message})
        response = self.client.chat.completions.create(
            model=self.model,
            messages =messages,
        )
        return response.choices[0].message.content