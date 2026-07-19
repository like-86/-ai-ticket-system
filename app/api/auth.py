from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from app.db.database import SessionLocal
from app.db.models import User
import bcrypt

from app.services.user_service import create_user, authenticate_user, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str
#注册接口
@router.post("/register")
def register(request: RegisterRequest):
    user = create_user(request.username, request.password)
    if user is None:
        raise HTTPException(400,"用户已存在")
    return {"message":"注册成功","username":user.username}
#登录接口
@router.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if user is None:
        raise HTTPException(401,"用户名或密码错误")
    token = create_access_token(user)
    return {"token":token,"message":"登录成功"}

