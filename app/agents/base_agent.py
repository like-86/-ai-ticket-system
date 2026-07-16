from langchain_openai import ChatOpenAI
from app.config import settings


class BaseAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            model=settings.LLM_MODEL,
            streaming=True,
        )


    def chat(self, message:str,system_prompt:str = None)->str:
        messages=[]
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", message))
        response = self.llm.invoke(messages)
        return response.content
    """
    设置流式对话提高用户体验
    """

    def chat_stream(self, message: str, system_prompt: str = None):
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", message))
        for chunk in self.llm.stream(messages):
            token = chunk.content
            if token:
                yield token
