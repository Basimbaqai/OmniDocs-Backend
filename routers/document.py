from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from typing import List
import io
from PIL import Image
from fastapi.params import Form
from sqlalchemy.orm import Session
from database import get_db
from models import Documents
import schemas
import oauth
from aws_config import s3_client, S3_BUCKET_NAME, S3_REGION

router = APIRouter(
    prefix='/documents',
    tags=['Documents']
)

@router.post("/upload-document/")
async def upload_document(
    title: str = Form(...), 
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth.get_current_user)
):
    """
    Receives a title and a list of images, creates a PDF, 
    uploads it to S3, and records the link in the database.
    """
    if not images:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No images provided.")

    # Validate S3 client is available
    if not s3_client:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="S3 service unavailable")

    # 1. Generate PDF from images in memory
    pdf_buffer = io.BytesIO()
    img_list = []

    for image in images:
        # Validate file type
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid file type: {image.filename}")
        
        try:
            # Open image using Pillow and convert to RGB mode for PDF compatibility
            img_content = await image.read()
            img = Image.open(io.BytesIO(img_content)).convert('RGB')
            img_list.append(img)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Error processing image {image.filename}: {e}")

    # Save all images into a single multi-page PDF in the buffer
    if img_list:
        img_list[0].save(
            pdf_buffer, 
            "PDF", 
            save_all=True, 
            append_images=img_list[1:], 
            resolution=100.0
        )
        pdf_buffer.seek(0)  # Rewind the buffer to the beginning

    # 2. Upload the PDF to AWS S3
    s3_key = f"documents/user_{current_user.user_id}/{title.replace(' ', '_')}_{len(images)}_images.pdf"
    try:
        s3_client.upload_fileobj(
            pdf_buffer, 
            S3_BUCKET_NAME, 
            s3_key,
            ExtraArgs={'ContentType': 'application/pdf'}
        )
        s3_link = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"S3 upload failed: {e}")

    # 3. Store the title and link in the database
    try:
        new_doc = Documents(
            title=title, 
            s3_link=s3_link, 
            owner_id=current_user.user_id
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

    return {
        "message": "Document successfully created and uploaded",
        "document_id": new_doc.document_id,
        "title": new_doc.title,
        "s3_link": new_doc.s3_link
    }

@router.get("/my-documents/")
async def get_my_documents(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth.get_current_user)
):
    """Get all documents owned by the current user"""
    documents = db.query(Documents).filter(Documents.owner_id == current_user.user_id).all()
    if documents:
        return {"documents": documents}
    else:
        return {"message": "No documents found."}
    
@router.delete("/delete-document/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth.get_current_user)
):
    """Delete a document owned by the current user"""
    document = db.query(Documents).filter(
        Documents.document_id == document_id,
        Documents.owner_id == current_user.user_id
    ).first()
    
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    try:
        # Delete from S3 (optional - you might want to keep files for backup)
        # s3_key = document.s3_link.split('.amazonaws.com/')[-1]
        # s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting document: {e}")