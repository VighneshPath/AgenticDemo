from typing import Annotated, Iterable, Sequence, TypedDict
from app.agents.sql_agent.tools import call_sql
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, START, END


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash-lite", temperature = 0
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

tools = {call_sql.name: call_sql}
llm = llm.bind_tools(tools = list(tools.values()))

def tool_node(state: AgentState) -> AgentState:
    """Execute tool calls from LLMs response"""

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
You will get a user query that will have some requirements related to people.

People has the following schema

CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    department TEXT NOT NULL,
    staffing_status TEXT NOT NULL CHECK (staffing_status IN ('staffed', 'bench', 'available')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

You can write read only sql queries on this schema to get the output that matches the requirements.
You can write multiple queries if there is something that you think you need to figure out first.
"""

def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state"""
    messages = list(state['messages'])
    messages = [SystemMessage(content = system_prompt)] + messages

    message = llm.invoke(messages)
    return {'messages': [message]}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("sql_agent", tool_node)
graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        'continue': "sql_agent",
        'end': END
    }
)
graph.add_edge("sql_agent", "llm")
graph.set_entry_point("llm")

orchestrator_agent = graph.compile()


def running_agent():
    print("\n==SQL AGENT==\n")

    while True:
        user_input = input("What is your question?\n")

        if user_input.lower() in ['exit', 'quit']:
            break

        initial_message = [HumanMessage(content = user_input)]

        result = orchestrator_agent.invoke({"messages": initial_message})

        print("\n==ANSWER==\n")
        print(result['messages'][-1].content)

# running_agent()