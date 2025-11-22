import os
from typing import TypedDict, Annotated, Sequence
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage # Foundational class for all message types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_chroma import Chroma


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash-lite", temperature = 0
)

# Embedding model should be compatible with LLM
embeddings = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-001"
)

pdf_path = "stock_market_2024.pdf"

pdf_loader = PyPDFLoader(pdf_path)

pages = pdf_loader.load()

# Chunk in 1k tokens with some overlap between chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

pages = text_splitter.split_documents(pages)

persist_dir = "./rag_db"
collection_name = "stock_market"

if not os.path.exists(persist_dir):
    os.makedirs(persist_dir)

vector_store = Chroma.from_documents(
    documents=pages,
    embedding=embeddings,
    persist_directory=persist_dir,
    collection_name=collection_name
)

retriver = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 5} # Amount of chunks to retur
)


@tool
def retriver_tool(query: str) -> str:
    """
    This tool searches and returns the information from the Stock Market Performance 2024 document.
    """

    docs = retriver.invoke(query)

    if not docs:
        return "I found no relevant information in the Stock Market Performance 2024 document."
    
    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")

    return "\n\n".join(results)

tools = {retriver_tool.name: retriver_tool}

llm = llm.bind_tools(tools = list(tools.values()))


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state: AgentState):
    """Check if last message contains tool calls"""
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "continue"
    return "end"

system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024.
Use the retriever tool available to answer questions about the stock market performance data. 
You can If you need to look up some information before asking a follow up question, you are allowed to do that.
Please always cite the specific parts of the documents you use in your answers.
"""

def call_llm(state: AgentState):
    """Function to call the LLM with the current state"""
    messages = list(state['messages'])
    messages = [SystemMessage(content = system_prompt)] + messages

    message = llm.invoke(messages)
    return {'messages': [message]}


def tool_node(state: AgentState) -> AgentState:
    """Execute tool calls from LLMs response"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_fn = tools[tool_call["name"]]
        observation = tool_fn.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))

    return {"messages": result}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriver_agent", tool_node)
graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        'continue': "retriver_agent",
        'end': END
    }
)
graph.add_edge("retriver_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()


def running_agent():
    print("\n==RAG AGENT==\n")

    while True:
        user_input = input("What is your question?\n")

        if user_input.lower() in ['exit', 'quit']:
            break

        initial_message = [HumanMessage(content = user_input)]

        result = rag_agent.invoke({"messages": initial_message})

        print("\n==ANSWER==\n")
        print(result['messages'][-1].content)

running_agent()