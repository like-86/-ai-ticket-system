from  fastapi import  APIRouter
from pydantic import BaseModel
from app.graph.workflow import run_agent_stream
import json
from fastapi.responses import StreamingResponse
from fastapi import BackgroundTasks, Request



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
async def chat(chat_req: ChatRequest):
    """非流式接口：内部复用流式逻辑，攒满再返回"""
    full_reply = ""
    async for token in run_agent_stream(chat_req.message, chat_req.session_id or None):
        full_reply += token
    return ChatResponse(reply=full_reply)
#流式输出SSE
@router.post("/stream")
async def chat_stream(chat_req: ChatRequest, http_request: Request, background_tasks:BackgroundTasks):
    generator = run_agent_stream(
        chat_req.message,
        chat_req.session_id or None,
        cancel_check=lambda: http_request.is_disconnected(),
    )
    async def generate():
        try:
            async for token in generator:
                yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"
        finally:
            yield f"data: {json.dumps({'token': '', 'done': True})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
