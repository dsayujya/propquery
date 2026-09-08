"""API routes for file uploads."""

import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

# Base URL for local development. In production, this would be an S3 bucket URL.
BASE_URL = "http://127.0.0.1:8000"

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user)
):
    """
    Simulate cloud storage (like AWS S3) by saving the uploaded file 
    locally to the `uploads/` directory and returning a public URL.
    """
    # Restrict file types
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
        
    # Generate unique filename to avoid collisions
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    
    file_location = os.path.join("uploads", unique_filename)
    
    # Save the file
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")
        
    # Return the generated "cloud" URL
    public_url = f"{BASE_URL}/uploads/{unique_filename}"
    
    return {"image_url": public_url}
