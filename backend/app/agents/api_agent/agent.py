from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage # Foundational class for all message types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv
from langgraph.graph.message import add_messages

from app.agents.api_agent.tools import call_api


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash-lite", temperature = 0
)

tools = {
    call_api.name: call_api
}

llm = llm.bind_tools(tools = list(tools.values()))


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def tool_node(state: AgentState) -> AgentState:
    """Execute tool calls from LLMs response"""
    print(f"Tool call")
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_fn = tools[tool_call["name"]]
        observation = tool_fn.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))

    return {"messages": result}

def should_continue(state: AgentState):
    """Check if last message contains tool calls"""
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "continue"
    return "end"

system_prompt = """
You can answer any requests related to beach.

For this you have a tool that can call the beach API, it has information about everything related to beach.

If someone asks for a specific person or thing, you can still call the API and filter the response.

It gives you details of all people on the beach
"""

def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state"""
    print("Call LLM")
    messages = list(state['messages'])
    messages = [SystemMessage(content = system_prompt)] + messages

    message = llm.invoke(messages)
    return {'messages': [message]}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("api_agent", tool_node)
graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        'continue': "api_agent",
        'end': END
    }
)
graph.add_edge("api_agent", "llm")
graph.set_entry_point("llm")

api_agent = graph.compile()


def running_agent():
    print("\n==API AGENT==\n")

    while True:
        user_input = input("What is your question?\n")

        if user_input.lower() in ['exit', 'quit']:
            break

        initial_message = [HumanMessage(content = user_input)]

        result = api_agent.invoke({"messages": initial_message})

        print("\n==ANSWER==\n")
        print(result['messages'][-1].content)

# running_agent()