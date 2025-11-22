from typing import TypedDict, Dict, List, Union
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite"
)

def process(state: AgentState) -> AgentState:
    """
        This node will solve the request you input
    """

    response = llm.invoke(state["messages"])

    state['messages'].append(AIMessage(content = response.content))

    print(f"AI: {response.content}")

    return state



graph = StateGraph(AgentState)

graph.add_node("process", process)

graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")


while user_input != 'exit':
    conversation_history.append(HumanMessage(user_input))

    result = agent.invoke({'messages': conversation_history})

    print(result['messages'])
    conversation_history = result['messages']

    user_input = input("Enter: ")