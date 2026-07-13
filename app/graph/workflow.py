from typing import Literal
from langgraph.graph import StateGraph, MessagesState
from app.agents.intent_agent import IntentAgent
from app.agents.base_agent import BaseAgent

#定义状态
class AgentState(MessagesState):
    intent: str="" #意图识别结果
    user_message: str=""    #用户原始消息
    final_reply: str=""        #最终回复
#定义节点
def classify_intent(state: AgentState) -> dict:
    agent=IntentAgent()
    intent = agent.classify(state["user_message"])
    return {"intent":intent}
def handle_ticket(state: AgentState) -> dict:
    reply = f"[工单已创建]已收到您的请求:{state['user_message']}"
    return {"final_reply":reply}
def handle_inquiry(state: AgentState) -> dict:
    agent=BaseAgent()
    reply = agent.chat(f"请回答这个产品咨询问题:{state['user_message']}")
    return {"final_reply":reply}
def handle_chat(state: AgentState) -> dict:
    agent=BaseAgent()
    reply = agent.chat(state["user_message"])
    return {"final_reply":reply}
#定义路由
def route_after_intent(state:AgentState)->Literal["handle_ticket","handle_inquiry","handle_chat"]:
    if state["intent"]=="ticket":
        return "handle_ticket"
    elif state["intent"]=="inquiry":
        return "handle_inquiry"
    elif state["intent"]=="chat":
        return "handle_chat"
#组装图
def build_graph():
    workflow = StateGraph(AgentState)
    # 添加节点
    workflow.add_node("classify_intent",classify_intent)
    workflow.add_node("handle_ticket",handle_ticket )
    workflow.add_node("handle_inquiry", handle_inquiry)
    workflow.add_node("handle_chat",handle_chat )
    #设置入口
    workflow.set_entry_point("classify_intent")
    #设置条件路由
    workflow.add_conditional_edges(
        "classify_intent",
        route_after_intent,
    )
    #设置出口
    workflow.add_edge("handle_ticket","__end__")
    workflow.add_edge("handle_inquiry", "__end__")
    workflow.add_edge("handle_chat", "__end__")

    return workflow.compile()
graph = build_graph()
def run_agent(user_message:str)->str:
    result = graph.invoke({
        "user_message":user_message,
        "intent":"",
        "final_reply":"",

    })
    return result["final_reply"]


