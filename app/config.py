# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
      APP_NAME: str = "AI Ticket System"
      APP_VERSION: str = "1.0.0"
      DEBUG: bool = False

      # API Keys
      DEEPSEEK_API_KEY: str = ""
      DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"

      # 模型
      LLM_MODEL: str = "deepseek-chat"
      #EMBEDDING_MODEL: str = "BAAI/bge-m3"
      #VECTOR_DIMENSION: int = 1024

      # 数据库
      DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/ai_ticket"
      REDIS_URL: str = "redis://localhost:6379/0"

      model_config = {"env_file": ".env"}

      #token
      JWT_SECRET_KEY: str = "change-this-in-production"  # 生产环境要改
      JWT_EXPIRE_HOURS: int = 24
settings = Settings()
