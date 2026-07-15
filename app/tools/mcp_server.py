from app.db.database import SessionLocal
from app.db.models import Ticket
from app.agents.retrieval_agent import RetrievalAgent


def create_ticket_tool(title: str, description: str)->dict:
    """创建表单工具"""
    db = SessionLocal()
    ticket = Ticket(title=title, description=description)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.close()
    return {"id":ticket.id, "status":ticket.status}


def search_knowledge_tool(query: str) -> str:
    """知识库检索工具"""
    agent = RetrievalAgent()
    return agent.search(query)

#工具注册表
TOOLS = [
      {
          "name": "create_ticket",
          "description": "创建工单",
          "handler": create_ticket_tool,
      },
      {
          "name": "search_knowledge",
          "description": "检索知识库",
          "handler": search_knowledge_tool,
      },
  ]