# OLD:
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import Chroma

# NEW:
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embedding_model
    )
    return vectorstore

