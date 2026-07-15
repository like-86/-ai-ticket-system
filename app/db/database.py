from sqlalchemy.orm import sessionmaker,DeclarativeBase
from sqlalchemy import create_engine
from app.config import settings

# MYSQL 数据库文件存在项目根目录
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    """每次请求获取一个数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
      """创建所有表"""
      Base.metadata.create_all(bind=engine)
