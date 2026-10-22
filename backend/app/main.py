from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, ConfigDict, Field

from app.services.grounding import grounding_service

router = APIRouter(prefix="/grounding", tags=["grounding"])


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=8, ge=1, le=25)


@router.post("/{project_id}/upload")
async def upload_document(project_id: str, file: UploadFile = File(...)):
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")
    if file.filename is None:
        raise HTTPException(status_code=400, detail="file filename is required")

    content = await file.read()
    document = grounding_service.add_document(project_id, file.filename, content, file.content_type)
    return {
        "project_id": project_id,
        "filename": file.filename,
        "status": "indexed",
        "chunks": document["chunk_count"],
    }


@router.get("/{project_id}/context")
def project_context(project_id: str, theme: str = ""):
    if not theme:
        theme = "tema principal do addon"
    return grounding_service.build_project_context(project_id, theme=theme, top_k=8)


@router.post("/{project_id}/search")
def search_project(project_id: str, request: SearchRequest):
    results = grounding_service.search(project_id, request.query, top_k=request.top_k)
    return {
        "project_id": project_id,
        "query": request.query,
        "results": results,
    }
