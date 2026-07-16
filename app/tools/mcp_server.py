from app.db.database import SessionLocal
from app.db.models import Ticket
from app.agents.retrieval_agent import RetrievalAgent
from langchain_core.tools import tool

@tool
def create_ticket_tool(title: str, description: str) -> str:
    """创建表单工具，该函数可以创建一个表单"""
    db = SessionLocal()
    ticket = Ticket(title=title, description=description)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.close()
    return f"工单已创建，编号：{ticket.id}，状态：{ticket.status}"


@tool
def search_knowledge_tool(query: str) -> str:
    """
    当用户提问时你应该先查询数据库，可以调用该工具
    知识库检索工具"""
    agent = RetrievalAgent()
    return agent.search(query)




#工具注册表
TOOLS = [search_knowledge_tool,create_ticket_tool]