from app.agents.base_agent import BaseAgent
class IntentAgent(BaseAgent):
    INTENTS = ["ticket","inquiry","chat"]
    def classify(self,message: str) -> str:
        prompt = f"""
        你是一个工单系统的意图识别器，当用户输入内容时，请分析用户的消息，判断消息属于以下哪一类：
         - ticket: 用户需要创建工单（账号问题、报错、投诉、申请等需要后台处理的请求）
         - inquiry: 用户咨询产品信息（问价格、功能、使用方法等）
         - chat: 普通聊天（问候、闲聊、没有明确目的）
         只返回一个词：ticket, inquiry, chat.
         用户消息：{message}
        """
        return self.chat(prompt)