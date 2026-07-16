from fastapi import  FastAPI
from fastapi.middleware.cors import  CORSMiddleware
from app.config import settings
from app.api import chat as chat_api
from app.db.database import init_db
from app.api import tickets as ticket_api
from app.api import knowledge as knowledge_api
from app.services.knowledge_base import init_knowledge_base

#创建fastapi实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
#初始化
init_db()
init_knowledge_base()
#接入路由
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
            },
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )