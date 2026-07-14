from app.agents.base_agent import BaseAgent
class IntentAgent(BaseAgent):
    INTENTS = ["ticket","inquiry","chat"]
    def classify(self,message: str) -> str:
        prompt = f"""
        你是一个工单系统的意图识别器，当用户输入内容时，请分析用户的消息，判断消息属于以下哪一类：
        - ticket: 用户需要人工处理（报错、投诉、申请、账号被封、支付失败等需要后台介入的）
        - inquiry: 用户咨询如何使用（问价格、问功能、问操作方法、问重置密码步骤等）
        - chat: 普通聊天（问候、闲聊、没有明确目的）
         只返回一个词：ticket, inquiry, chat.
         用户消息：{message}
        """
        return self.chat(prompt)