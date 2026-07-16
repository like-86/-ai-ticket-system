from  fastapi import  APIRouter
from pydantic import BaseModel
from app.graph.workflow import run_agent, run_agent_stream
import json
from fastapi.responses import StreamingResponse



router = APIRouter(prefix="/api/chat", tags=["chat"])
#请求体模型
class ChatRequest(BaseModel):
    message: str
    session_id: str = ""
#响应体模型
class ChatResponse(BaseModel):
    reply:str
    session_id: str = ""

@router.post("",response_model=ChatResponse)
def chat(request: ChatRequest):
    result = run_agent(request.message,request.session_id or None)
    return ChatResponse(reply=result["reply"])
#流式输出SSE
@router.post("/stream")
async def chat_stream(request: ChatRequest):
    generator = run_agent_stream(request.message,request.session_id or None)
    async def generate():
        async for token in generator:
            yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"
        yield f"data: {json.dumps({'token': '', 'done': True})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
