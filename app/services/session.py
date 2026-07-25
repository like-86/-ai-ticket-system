import json
import redis
from app.config import settings
from langchain_core.messages import message_to_dict, messages_from_dict, HumanMessage

redis_client = redis.Redis.from_url(settings.REDIS_URL, protocol=2)

SUMMARY_PROMPT = "请用一段话总结以上对话的核心内容，保留关键信息（用户的问题、已解决的问题、待办事项）。只返回总结，不要其他内容。"

def get_history(session_id: str, keep_rounds: int = 2)->list:
    """从 Redis 获取历史消息。
    如果有总结，返回 [总结SystemMessage] + 最近 N 轮原文。
    没有总结则返回全部历史。
    """
    from langchain_core.messages import SystemMessage
    summary = get_summary(session_id)
    data = redis_client.get(f"session:{session_id}")
    if not data:
        return []
    all_msgs = messages_from_dict(json.loads(data))

    if not summary:
        return all_msgs  # 还没总结，返回全部

    # 有总结 → 截取最近 keep_rounds 轮（每轮 1 条用户 + 1 条 AI = 2 条）
    recent = all_msgs[-(keep_rounds * 2):]
    return [SystemMessage(content=f"以下是对之前对话的总结：\n{summary}")] + recent

def get_summary(session_id: str) -> str:
    """获取历史总结"""
    data = redis_client.get(f"session:{session_id}:summary")
    return data.decode() if data else ""

def save_messages(session_id:str, messages:list):
    """保存消息到 Redis（24小时过期）。返回 'summarize' 表示需要总结"""
    dicts = [message_to_dict(m) for m in messages]
    redis_client.setex(f"session:{session_id}",86400,json.dumps(dicts))

    # 判断用户消息是否达到第 5 轮（5 条 HumanMessage）
    user_msgs = [m for m in messages if isinstance(m, HumanMessage)]
    if user_msgs and len(user_msgs) > 0 and len(user_msgs) % 5 == 0:
        return "summarize"
    return None

def summarize_and_store(session_id: str):
    """异步：读取历史消息 → LLM 总结 → 存入 Redis"""
    from app.agents.base_agent import BaseAgent
    history = get_history(session_id)
    # 把历史消息转为文本传给 LLM
    history_text = "\n".join([f"{type(m).__name__}: {m.content}" for m in history])
    summary = BaseAgent().chat(history_text, SUMMARY_PROMPT)
    redis_client.setex(f"session:{session_id}:summary", 86400, summary)
    print(f"📝 session {session_id} 总结完成")