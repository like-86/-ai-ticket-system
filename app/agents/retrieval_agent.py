from app.agents.base_agent import BaseAgent

class RetrievalAgent(BaseAgent):
    knowledge_base = {
        "密码": "密码重置方法：在登录页面点击'忘记密码'，输入注册邮箱接收重置链接",
        "账号": "账号激活：注册后请查收激活邮件，如未收到请检查垃圾邮箱",
        "退款": "退款政策：购买后7天内可申请全额退款，退款将在3-5个工作日原路返回",
        "价格": "定价方案：基础版免费，专业版99元/月，企业版联系销售定制",
    }