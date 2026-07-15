from  fastapi import  APIRouter
from pydantic import BaseModel
from app.graph.workflow import run_agent

router = APIRouter(prefix="/api/chat", tags=["chat"])
#请求体模型
class ChatRequest(BaseModel):
    message: str
#响应体模型
class ChatResponse(BaseModel):
    reply:str
    intent:str=""

@router.post("",response_model=ChatResponse)
def chat(request: ChatRequest):
    result = run_agent(request.message)
    return ChatResponse(reply=result["reply"],intent =result["intent"] )