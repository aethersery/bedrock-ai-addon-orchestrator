from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, ConfigDict, Field

from app.services.document_corpus import document_corpus_service

router = APIRouter(prefix="/corpus", tags=["corpus"])


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("/{project_id}/upload")
async def upload_document(project_id: str, file: UploadFile = File(...)):
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")
    if file.filename is None:
        raise HTTPException(status_code=400, detail="file filename is required")

    content = await file.read()
    result = document_corpus_service.ingest_file(project_id, file.filename, content, file.content_type)
    return {
        "project_id": project_id,
        "filename": file.filename,
        "status": "ingested",
        "chunks": result["chunk_count"],
    }


@router.get("/{project_id}/documents")
def list_documents(project_id: str):
    return document_corpus_service.list_documents(project_id)


@router.post("/{project_id}/search")
def search_documents(project_id: str, request: SearchRequest):
    results = document_corpus_service.search(project_id, request.query, top_k=request.top_k)
    return {
        "project_id": project_id,
        "query": request.query,
        "results": results,
    }
