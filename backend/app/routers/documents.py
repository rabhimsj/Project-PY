from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import Document, User
from app.services.ai_service import AIService
from app.services.document_service import DocumentService

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    try:
        file_bytes = file.file.read()
        document = service.store_document(current_user, file.filename or "untitled.pdf", file_bytes, file.content_type or "application/octet-stream")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"message": "Document uploaded successfully", "document_id": document.id, "filename": document.filename}


@router.get("")
def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = DocumentService(db)
    documents = service.list_documents(current_user.id)
    return [{"id": item.id, "filename": item.filename, "summary": item.summary, "created_at": item.created_at.isoformat()} for item in documents]


@router.get("/search")
def search_documents(query: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = DocumentService(db)
    results = service.search_query(current_user.id, query)
    return [{"document_id": document.id, "filename": document.filename, "match": content} for document, content in results]


@router.post("/{document_id}/summarize")
def summarize_document(document_id: int, summary_type: str = "short", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    service = DocumentService(db)
    text = service.get_document_text(document.id)
    summary = AIService().build_summary(text, summary_type)
    return summary
