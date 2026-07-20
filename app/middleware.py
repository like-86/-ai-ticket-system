
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
app = FastAPI()


# 注册中间件
@app.middleware("http")
async def middleware(request: Request, call_next):

    token=request.headers.get("Authorization")
    if request.url.path == "/api/auth/register" or request.url.path == "/api/auth/login":
        return await call_next(request)
    if not token or token == "":
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    else:
         return  await call_next(request)
