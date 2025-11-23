from langchain_core.tools import tool

from app.agents.sql_agent.agent import orchestrator_agent, AgentState as SqlAgentState
from app.agents.api_agent.agent import api_agent, AgentState as ApiAgentState
from app.agents.rag_agent.agent import rag_agent, AgentState as RagAgentState

@tool
def call_sql_agent(message: str) -> str:
    """
    This tool calls the SQL agent with a string.
    It can be used for any queries about people that are part of Sahaj Software, a company.
    The agent is autonomous and the message that is passed can be plain text and it will write it's own query to 
    figure stuff out. 
    """
    print(f"Calling SQL agent with {message}")
    results = orchestrator_agent.invoke(SqlAgentState({"messages": [message]}))
    print(f"Response {results['messages'][-1].content}")
    return results['messages'][-1].content

@tool
def call_api_agent(message: str) -> str:
    """
    This tool calls the API agent with a string.
    It can be used for any queries all of the people on beach.
    The agent is autonomous and the message that is passed can be plain text and it will figure stuff out. 
    """
    print(f"Calling API agent with {message}")
    results = api_agent.invoke(ApiAgentState({"messages": [message]}))
    print(f"Response {results['messages'][-1].content}")
    return results['messages'][-1].content

@tool
def call_rag_agent(message: str) -> str:
    """
    This tool calls the RAG agent with a string.
    It can be used to get information about the policies that are present in Sahaj Software, a company.
    It has the following policies
        - Laptop Replacement Policy
        - Data Breach and incident response
        - Anti-Piracy Policy
        - Disaster Recovery and Business continuity
    The agent is autonomous and the message that is passed can be plain text and it will figure stuff out. 
    """
    print(f"Calling RAG agent with {message}")
    results = rag_agent.invoke(RagAgentState({"messages": [message]}))
    print(f"Response {results['messages'][-1].content}")
    return results['messages'][-1].content
