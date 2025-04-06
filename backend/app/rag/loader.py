import os
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.rag.vector_store import get_vectorstore
from chromadb import Client
from chromadb import PersistentClient

# Example of creating a persistent client and interacting with Chroma
client = PersistentClient(path="./chroma")  # Path to store data

# Now you can use the client to interact with the Chroma database


def load_and_store_documents(directory: str = "data"):
    # Get the vector store (Chroma collection)
    vectorstore = get_vectorstore()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            path = os.path.join(directory, file)
            print(f"📄 Loading PDF: {path}")
            loader = PyMuPDFLoader(path)
            docs = loader.load()

            print(f"✂️ Splitting document into chunks...")
            chunks = text_splitter.split_documents(docs)

            print(f"➕ Adding {len(chunks)} chunks to vector store...")

            # Add documents to the Chroma collection
            for idx, chunk in enumerate(chunks):
                # Create a unique ID using file name and chunk index
                unique_id = f"{file}_{idx}"

                vectorstore.add(
                    documents=[chunk.page_content],  # Document text content
                    metadatas=[{"source": file}],  # Metadata (e.g., source file name)
                    ids=[unique_id]  # Unique ID for each chunk
                )

    print("✅ Vector store updated successfully!")

def get_vectorstore():
    # Initialize the Chroma client with persistence enabled
    client = Client()  # You may add your configuration details if needed
    # Specify the persistent directory
    # Create or get an existing collection
    collection = client.get_or_create_collection("my_collection")

    # Return the collection (vector store)
    return collection  # Just return the collection
