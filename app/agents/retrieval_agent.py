from app.agents.base_agent import BaseAgent
from app.services.knowledge_base import search_knowledge

class RetrievalAgent(BaseAgent):
    def search(self, query: str) -> str:
        return search_knowledge(query)

