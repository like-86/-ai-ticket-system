import json
import redis
from app.config import settings
from langchain_core.messages import message_to_dict, messages_from_dict

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def get_history(session_id: str)->list:
    """从 Redis 获取历史消息"""
    data = redis_client.get(f"session:{session_id}")
    if data:
        return messages_from_dict(json.loads(data))
    return []

def save_messages(session_id:str,messages:list):
    """保存消息到 Redis（24小时过期）"""
    dicts = [message_to_dict(m) for m in messages]
    redis_client.setex(f"session:{session_id}",86400,json.dumps(dicts))