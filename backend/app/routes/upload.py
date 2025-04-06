from fastapi import APIRouter, HTTPException, UploadFile, File
import os
from app.rag.loader import load_and_store_documents
from app.rag.vector_store import get_vectorstore
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the /upload endpoint
@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Check if the uploaded file is a PDF
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        # Get the upload directory path from the environment or use the default
        upload_dir = os.getenv("UPLOAD_DIR", "data/uploads")
        
        # Log the upload directory to ensure it's correct
        logger.info(f"Using upload directory: {upload_dir}")
        
        # Ensure the upload directory exists
        os.makedirs(upload_dir, exist_ok=True)

        # Save the uploaded file to the specified directory
        file_path = os.path.join(upload_dir, file.filename)
        
        # Log the full file path
        logger.info(f"Saving file to: {file_path}")
        
        # Save the file content
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # After saving the file, call load_and_store_documents to process it
        logger.info(f"📄 File '{file.filename}' uploaded successfully, processing it...")

        # Now load and store the document into the vector store
        try:
            load_and_store_documents(directory=upload_dir)
        except Exception as e:
            logger.error(f"Error processing file '{file.filename}': {str(e)}")
            # Delete the file if processing failed
            os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")

        # Optionally, you can delete the file after processing (if no longer needed)
        os.remove(file_path)

        return {"message": f"File '{file.filename}' uploaded and processed successfully!"}

    except Exception as e:
        logger.error(f"Error processing file '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
