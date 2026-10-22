from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

router = APIRouter(prefix="/reference", tags=["reference"])

REFERENCE_STORE: dict = {}


@router.post("/upload")
async def upload_reference(file: UploadFile = File(...), project_id: str = ""):
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")

    try:
        content = await file.read()
        REFERENCE_STORE.setdefault(project_id, []).append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "stored": True,
        })
        return {
            "project_id": project_id,
            "filename": file.filename,
            "status": "uploaded",
            "size": len(content),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}")


@router.get("/list/{project_id}")
def list_references(project_id: str):
    return REFERENCE_STORE.get(project_id, [])
