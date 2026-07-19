from datetime import datetime,timedelta

from app.config import settings
from app.db.database import SessionLocal
from app.db.models import User
import bcrypt
import jwt

def create_user( username: str, password: str):
    """注册新用户"""
    db=SessionLocal()
    try:
        existing = db.query(User).filter(User.username==username).first()
        if existing:
            return None
        hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        user = User(username=username,password=hashed.decode())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def authenticate_user(username:str, password:str):
    """验证用户登录，成功返回 user，失败返回 None"""
    db=SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return None
        return user
    finally:
        db.close()

def create_access_token(user: User):
    pyload = {"user_id":user.id,"username":user.username,"exp":datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)}
    token = jwt.encode(pyload,settings.JWT_SECRET_KEY,algorithm="HS256")
    return token
