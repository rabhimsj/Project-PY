from __future__ import annotations

import os
import re
from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.ai.llm_provider import get_provider
from app.config import settings
from app.models import Document, DocumentChunk, User


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.storage_root = Path(__file__).resolve().parents[2] / "uploads"
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _chunk_text(self, text: str, chunk_size: int = 650) -> list[str]:
        cleaned = self._clean_text(text)
        if not cleaned:
            return []
        return [cleaned[i : i + chunk_size] for i in range(0, len(cleaned), chunk_size)]

    def _extract_text_from_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)
        return "\n".join(pages)

    def _extract_text(self, file_name: str, file_bytes: bytes) -> str:
        lower_name = file_name.lower()
        if lower_name.endswith(".pdf"):
            temp_path = self.storage_root / f"temp_{os.urandom(8).hex()}.pdf"
            temp_path.write_bytes(file_bytes)
            try:
                return self._extract_text_from_pdf(str(temp_path))
            finally:
                if temp_path.exists():
                    temp_path.unlink()

        text = file_bytes.decode("utf-8", errors="replace")
        return self._clean_text(text)

    def validate_upload(self, file_name: str, file_size: int) -> None:
        allowed = {".pdf", ".txt", ".md"}
        suffix = Path(file_name).suffix.lower()
        if suffix not in allowed:
            raise ValueError("Unsupported file type. Upload PDF, TXT, or Markdown files only.")
        if file_size > settings.max_upload_size_bytes:
            raise ValueError(f"File exceeds the allowed size of {settings.max_upload_size_mb} MB.")

    def store_document(self, user: User, file_name: str, file_bytes: bytes, content_type: str) -> Document:
        self.validate_upload(file_name, len(file_bytes))
        user_dir = self.storage_root / str(user.id)
        user_dir.mkdir(parents=True, exist_ok=True)

        safe_name = Path(file_name).name
        target_path = user_dir / safe_name
        count = 1
        while target_path.exists():
            target_path = user_dir / f"{Path(safe_name).stem}_{count}{Path(safe_name).suffix}"
            count += 1

        target_path.write_bytes(file_bytes)
        text = self._extract_text(safe_name, file_bytes)
        if not text:
            raise ValueError("The uploaded file does not contain readable text.")

        document = Document(
            user_id=user.id,
            filename=safe_name,
            content_type=content_type,
            file_path=str(target_path),
            summary=text[:500],
            metadata_json='{"source": "upload"}',
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        chunks = self._chunk_text(text)
        provider = get_provider()
        for index, chunk in enumerate(chunks):
            embedding = provider.embed_text(chunk)
            self.db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    embedding=str(embedding),
                )
            )
        self.db.commit()
        return document

    def list_documents(self, user_id: int) -> list[Document]:
        return self.db.query(Document).filter(Document.user_id == user_id).order_by(Document.created_at.desc()).all()

    def search_query(self, user_id: int, query: str) -> list[tuple[Document, str]]:
        if not query.strip():
            return []

        chunks = self.db.query(DocumentChunk).join(Document).filter(Document.user_id == user_id).all()
        scored = []
        for chunk in chunks:
            text = chunk.content.lower()
            score = text.count(query.lower())
            if score > 0:
                scored.append((chunk.document, chunk.content, score))

        if not scored:
            return []

        ranked = sorted(scored, key=lambda item: item[2], reverse=True)
        return [(document, content) for document, content, _ in ranked[:5]]

    def get_document_text(self, document_id: int) -> str:
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return ""
        file_path = Path(document.file_path)
        if file_path.exists():
            return file_path.read_text(errors="replace")
        return document.summary or ""
