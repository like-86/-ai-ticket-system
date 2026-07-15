from app.tools.mcp_server import TOOLS
from langgraph.graph import StateGraph, MessagesState
from app.agents.intent_agent import IntentAgent
from app.agents.base_agent import BaseAgent



# 工具查找函数
def call_tool(name:str,**kwargs)->dict:
    for tool in TOOLS:
        if tool["name"]==name:
            return tool["handler"](**kwargs)
    raise ValueError(f"工具{name}不存在")

#定义状态
class AgentState(MessagesState):
    intent: str="" #意图识别结果
    user_message: str=""    #用户原始消息
    final_reply: str=""        #最终回复
    retrieved_context: str = ""

#定义节点
def classify_intent(state: AgentState) -> dict:
    agent=IntentAgent()
    intent = agent.classify(state["user_message"])
    return {"intent":intent}

def handle_ticket(state: AgentState) -> dict:
    result = call_tool("create_ticket",title =f"用户请求:{state['user_message']}",description=state['user_message'])

    reply = f"[工单已创建] 工单编号{result['id']}，我们会尽快处理。您的请求：{state['user_message']}"
    return {"final_reply":reply}

def handle_inquiry(state: AgentState) -> dict:
    agent=BaseAgent()
    reply = agent.chat(f"请回答这个产品咨询问题:{state['user_message']}")
    return {"final_reply":reply}

def handle_chat(state: AgentState) -> dict:
    agent=BaseAgent()
    reply = agent.chat(state["user_message"])
    return {"final_reply":reply}

def retrieve_knowledge(state: AgentState) -> dict:
    context = call_tool("search_knowledge", query=state['user_message'])
    return {"retrieved_context": context}

def generate_answer(state: AgentState) -> dict:
    agent= BaseAgent()
    prompt=f"""基于以下知识库内容回答用户问题。

          知识库内容：
          {state['retrieved_context']}
        
          用户问题：{state['user_message']}
        
          请用中文回答。"""
    reply = agent.chat(prompt)
    return {"final_reply": reply}
#定义路由
def route_after_intent(state:AgentState):
    if state["intent"]=="ticket":
        return "handle_ticket"
    elif state["intent"]=="inquiry":
        return "retrieve_knowledge"
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
    workflow.add_node("retrieve_knowledge",retrieve_knowledge)
    workflow.add_node("generate_answer",generate_answer)
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
    workflow.add_edge("retrieve_knowledge", "generate_answer")
    workflow.add_edge("generate_answer", "__end__")

    return workflow.compile()
graph = build_graph()
def run_agent(user_message:str)->dict:
    result = graph.invoke({
        "user_message":user_message,
        "intent":"",
        "final_reply":"",

    })
    return {
        "reply": result["final_reply"],
        "intent": result["intent"],
    }

