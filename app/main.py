from fastapi import  FastAPI
from fastapi.middleware.cors import  CORSMiddleware
from app.config import settings
from app.api import chat as chat_api
from app.db.database import init_db
from app.api import tickets as ticket_api
from app.api import knowledge as knowledge_api
from app.services.knowledge_base import init_knowledge_base
from app.api import auth as auth_api
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request

#创建fastapi实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
# 注册中间件
@app.middleware("http")
async def middleware(request: Request, call_next):

    token=request.headers.get("Authorization")
    if request.url.path == "/api/auth/register" or request.url.path == "/api/auth/login":
        return await call_next(request)
    if not token or token == "":
        return JSONResponse(status_code=401, content={"detail": "未登录"})
    else:
         return  await call_next(request)
#初始化
init_db()
init_knowledge_base()
#接入路由
app.include_router(auth_api.router)
app.include_router(chat_api.router)
app.include_router(ticket_api.router)
app.include_router(knowledge_api.router)
#注册 cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": settings.APP_NAME,
            "version": settings.APP_VERSION,
            }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
