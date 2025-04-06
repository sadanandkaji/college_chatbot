from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from app.db.database import get_db  # Database session utility
from app.db import models  # Your database models
from app.rag.chain import get_rag_chain  # The RAG chain for processing queries
from app.models.schemas import UserCreate ,QuestionRequest

router = APIRouter()

# Pydantic model for the incoming query
class ChatInput(BaseModel):
    query: str

# Initialize the RAG chain once at startup
rag_chain = get_rag_chain()

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.db.database import get_db  # Database session utility
from app.db import models  # Your database models
from app.rag.chain import get_rag_chain  # The RAG chain for processing queries
from app.models.schemas import QuestionRequest

router = APIRouter()

# Initialize the RAG chain once at startup
rag_chain = get_rag_chain()

# Endpoint for sending a query to the chatbot
@router.post("/", summary="Ask a question to the RAG chatbot", response_description="Answer with retrieved sources")
async def chat_with_bot(data: QuestionRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Process the user's query using the RAG chain
        result = rag_chain.invoke(data.question)

        # For this example, assuming the user ID is stored in the JWT token or session
        user_id = 1  # This is hardcoded; replace with actual user retrieval from JWT or session

        # Store the query and response in the database (query logging)
        query_log = models.QueryLog(user_id=user_id, question=data.question, answer=result["result"])
        db.add(query_log)
        await db.commit()
        await db.refresh(query_log)  # Refresh to get the new ID if necessary

        # Return the response and source documents without the greeting
        return {
            "response": result["result"],  # This is the chatbot's answer
            "sources": [
                {"content": doc.page_content, "metadata": doc.metadata}
                for doc in result.get("source_documents", [])  # These are the sources of information for the answer
            ]
        }
    except Exception as e:
        # If an error occurs, return an HTTPException with the error message
        raise HTTPException(status_code=500, detail=str(e))



# Endpoint for getting all query logs/messages
@router.get("/messages", summary="Get all previous chatbot interactions", response_description="List of chat messages")
async def get_messages(db: AsyncSession = Depends(get_db)):
    try:
        # Query all messages from the query logs
        query_logs = await db.execute(select(models.QueryLog).order_by(models.QueryLog.timestamp.desc()))
        query_logs = query_logs.scalars().all()

        # Return the messages
        return [
            {
                "user_id": log.user_id,
                "question": log.question,
                "answer": log.answer,
                "timestamp": log.timestamp
            }
            for log in query_logs
        ]
    except Exception as e:
        # If an error occurs, return an HTTPException with the error message
        raise HTTPException(status_code=500, detail=str(e))
