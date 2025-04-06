from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from app.rag.vector_store import get_vectorstore
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch HuggingFace API token from environment
api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Define the prompt template for the model
prompt_template = PromptTemplate.from_template(
    "You are a helpful college assistant. Use the context to answer:\n\nContext:\n{context}\n\nQuestion:\n{question}"
)

# Function to get the RAG chain
def get_rag_chain():
    # Initialize the retriever with the vector store
    retriever = get_vectorstore().as_retriever()

    # Define the LLM using Hugging Face's API (falcon-7b-instruct model)
    llm = HuggingFaceEndpoint(
        task="text-generation",               # Task type is text generation
        repo_id="tiiuae/falcon-7b-instruct",  # Model repo on Hugging Face
        huggingfacehub_api_token=api_token,   # API token for Hugging Face Hub
        temperature=0.5,                      # Control randomness in the output
        max_new_tokens=300                    # Limit the number of tokens in the response
    )

    # Create the RAG chain combining the retriever and LLM
    chain = RetrievalQA.from_chain_type(
        llm=llm,                               # The LLM model to use for response generation
        retriever=retriever,                   # The retriever used to fetch relevant context
        chain_type="stuff",                    # "stuff" method to inject the context directly into the prompt
        chain_type_kwargs={"prompt": prompt_template}, # Provide the prompt template for the chain
        return_source_documents=True          # Return source documents along with the response
    )

    return chain
