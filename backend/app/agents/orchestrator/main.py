from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage # Foundational class for all message types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.tools import tool

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
    """This is an addition function that adds two numbers together"""
    return a+b

@tool
def subtract(a: int, b: int):
    """This is an subtract function that subtract two numbers together"""
    return a-b

@tool
def multiply(a: int, b: int):
    """This is an multiply function that multiply two numbers together"""
    return a*b

tools = {add.name: add, subtract.name: subtract, multiply.name: multiply}

model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-lite").bind_tools(list(tools.values()))


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content = "You are my AI assistant, please answer my query to the best of your ability")
    response = model.invoke([system_prompt] + list(state["messages"]))

    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    messages: Sequence[BaseMessage] = state["messages"]
    last_message: BaseMessage = messages[-1]

    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

def tool_node(state: AgentState) -> AgentState:
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_fn = tools[tool_call["name"]]
        observation = tool_fn.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))

    return {"messages": result}


graph = StateGraph(AgentState)

graph.add_node("our_agent", model_call)

graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")

agent = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s['messages'][-1]
        if(isinstance(message, tuple)):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [HumanMessage(content= "Add 34 + 21, Add 3+4, add 12 + 12, then subtract 9 from 1, and multiply 9 with 7. Then tell me a joke.")]}

print_stream(agent.stream(inputs, stream_mode="values"))