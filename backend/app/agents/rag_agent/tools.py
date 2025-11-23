from langchain_core.tools import tool
from langchain_chroma import Chroma
from app.agents.rag_agent.const import *
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-001"
)

vector_store = Chroma(
    persist_directory=persist_dir,
    collection_name=collection_name,
    embedding_function=embeddings
)

retriver = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 5} # Amount of chunks to return
)

@tool
def retriver_tool(query: str) -> str:
    """
    This tool searches and returns the information from sahaj policy documents.
    You have information about
        - Laptop Replacement Policy
        - Data Breach and incident response
        - Anti-Piracy Policy
        - Disaster Recovery and Business continuity
    """

    docs = retriver.invoke(query)

    if not docs:
        return "I found no relevant information in the Stock Market Performance 2024 document."
    
    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")

    return "\n\n".join(results)