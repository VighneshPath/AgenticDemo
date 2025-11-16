from typing import TypedDict, Dict, List
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite"
)

def process(state: AgentState) -> AgentState:
    """
        Simple node that processes agent state
    """

    response = llm.invoke(state["messages"])

    print(f"AI: {response.content}")
    return state



graph = StateGraph(AgentState)

graph.add_node("process", process)

graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

user_input = input("Enter: ")

result = agent.invoke({"messages": [HumanMessage(content = user_input)]})

print(result)