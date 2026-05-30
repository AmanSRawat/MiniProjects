from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI

from tool import all_tools

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

tool_node = ToolNode(all_tools)
llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

def agent_node(state: AgentState) -> AgentState:
    """The agent node that evaluate the history and choose a tool."""
    system_prompt = SystemMessage(
        content="""
        You are an advanced Lead Generation and Market Research assistant.
        Your goal is to gather information about companies, scrape details regarding their IT framework, and save relevant summaries.

        - Use 'search_web' if you need a broad overview or specific answers.
        - Use 'scrape_and_analyze' to extract technical footprint contexts about a company.
        - Use 'save_leads_to_file' when you have a definitive block of research text that the user wants to keep.
        """
    )
    
    message = [system_prompt] + list(state["messages"])
    response = llm.invoke(message)
    return {"messages": [response]}

def should_continue(state: AgentState)-> AgentState:
    """Conditional routing edge checking if the model wants to call a tool."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

graph = StateGraph(AgentState)
graph.add_node("agent",agent_node)
graph.add_node("tools",tool_node)

graph.add_edge(START,"agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools":"tools",
        "end": END
    }
)
graph.add_edge("tools","agent")

agent = graph.compile()