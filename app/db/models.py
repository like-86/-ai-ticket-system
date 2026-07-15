# app/db/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)       # 工单标题
    description = Column(Text, nullable=False)          # 工单描述
    status = Column(String(20), default="pending")      # pending / processing /resolved / closed
    priority = Column(String(10), default="normal")     # low / normal / high / urgent
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)