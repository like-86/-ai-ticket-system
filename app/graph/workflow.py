from langgraph.graph import StateGraph, MessagesState
from app.tools.mcp_server import TOOLS
from app.agents.base_agent import BaseAgent
from langgraph.prebuilt import ToolNode


class AgentState(MessagesState):
    final_reply: str = ""


def agent_node(state: AgentState):
    llm = BaseAgent().llm.bind_tools(TOOLS)
    response = llm.invoke(state["messages"])
    return {"messages": [response], "final_reply": response.content}


def should_continue(state: AgentState):
    last_msg = state["messages"][-1]
    if last_msg.tool_calls:
          return "tools"
    return "__end__"

#绘图
def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(TOOLS))

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")   # tools 执行完回到 agent 继续思考

    return workflow.compile()


graph = build_graph()


def run_agent(user_message: str):
      result = graph.invoke({
          "messages": [("human", user_message)],
          "final_reply": "",
      })
      return {"reply": result["final_reply"]}

async def run_agent_stream(user_message: str):
      """流式运行，走完所有节点，逐 token 输出"""
      input_data = {
          "messages": [("human", user_message)],
          "final_reply": "",
      }

      async for event in graph.astream_events(input_data, version="v2"):
          if event["event"] == "on_chat_model_stream":
              content = event["data"]["chunk"].content
              if content:
                  yield content


