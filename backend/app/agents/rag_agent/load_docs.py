from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os
from app.agents.rag_agent.const import *
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-001"
)

docs_path = os.path.join(os.getcwd(), "app", "agents", "rag_agent", "docs")
docx_files = os.listdir(docs_path)

all_docs = []

for file in docx_files:
    loader = Docx2txtLoader(os.path.join(docs_path, file))
    pages = loader.load()

    # Add metadata so we know which file each chunk came from
    for p in pages:
        p.metadata["source"] = file

    all_docs.extend(pages)

# Chunk in 1k tokens with some overlap between chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

pages = text_splitter.split_documents(all_docs)

if not os.path.exists(persist_dir):
    os.makedirs(persist_dir)

vector_store = Chroma.from_documents(
    documents=pages,
    embedding=embeddings,
    persist_directory=persist_dir,
    collection_name=collection_name
)