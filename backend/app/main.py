from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models_db import ProjectRecord, ProjectVersionRecord, ReferenceRecord, UserRecord

router = APIRouter(prefix="/production", tags=["production"])

STORAGE_ROOT = Path(os.getenv("APP_STORAGE_DIR", "./storage"))
STORAGE_ROOT.mkdir(parents=True, exist_ok=True)


class CreateProjectPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    owner_id: int | None = None
    name: str = Field(..., min_length=2, max_length=120)
    theme: str = Field(..., min_length=2, max_length=250)
    style: str = Field(default="inspiracao-fiel")
    fidelity: str = Field(default="high")
    version: str = Field(default="0.0.1")
    target_platform: str = Field(default="bedrock-1.20+")


@router.get("/users")
def list_users():
    session = SessionLocal()
    try:
        rows = session.query(UserRecord).all()
        return [{
            "id": row.id,
            "username": row.username,
            "created_at": row.created_at.isoformat(),
        } for row in rows]
    finally:
        session.close()


@router.post("/projects")
def create_project(payload: CreateProjectPayload):
    session = SessionLocal()
    try:
        owner = None
        if payload.owner_id is not None:
            owner = session.query(UserRecord).filter(UserRecord.id == payload.owner_id).first()
        if owner is None:
            owner = session.query(UserRecord).filter(UserRecord.username == "demo").first()
            if owner is None:
                owner = UserRecord(username="demo", password="demo123")
                session.add(owner)
                session.commit()
                session.refresh(owner)

        project = ProjectRecord(
            name=payload.name,
            theme=payload.theme,
            style=payload.style,
            fidelity=payload.fidelity,
            version=payload.version,
            target_platform=payload.target_platform,
            summary="Projeto criado com persistência real e workflow de produção.",
            status="draft",
            owner_id=owner.id,
        )
        session.add(project)
        session.commit()
        session.refresh(project)

        version = ProjectVersionRecord(
            project_id=project.id,
            version=project.version,
            status="created",
            summary=f"Versão inicial para {project.name}.",
        )
        session.add(version)
        session.commit()

        return {
            "id": project.id,
            "owner_id": owner.id,
            "name": project.name,
            "theme": project.theme,
            "status": project.status,
            "version": project.version,
        }
    finally:
        session.close()


@router.get("/projects")
def list_projects():
    session = SessionLocal()
    try:
        rows = session.query(ProjectRecord).all()
        return [{
            "id": row.id,
            "name": row.name,
            "theme": row.theme,
            "style": row.style,
            "fidelity": row.fidelity,
            "version": row.version,
            "target_platform": row.target_platform,
            "status": row.status,
            "summary": row.summary,
            "owner_id": row.owner_id,
            "created_at": row.created_at.isoformat(),
        } for row in rows]
    finally:
        session.close()


@router.get("/projects/{project_id}")
def get_project(project_id: int):
    session = SessionLocal()
    try:
        project = session.query(ProjectRecord).filter(ProjectRecord.id == project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return {
            "id": project.id,
            "name": project.name,
            "theme": project.theme,
            "style": project.style,
            "fidelity": project.fidelity,
            "version": project.version,
            "target_platform": project.target_platform,
            "status": project.status,
            "summary": project.summary,
            "owner_id": project.owner_id,
        }
    finally:
        session.close()


@router.post("/projects/{project_id}/references")
async def upload_reference(project_id: int, file: UploadFile = File(...)):
    session = SessionLocal()
    try:
        project = session.query(ProjectRecord).filter(ProjectRecord.id == project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        file_dir = STORAGE_ROOT / str(project_id)
        file_dir.mkdir(parents=True, exist_ok=True)
        saved_path = file_dir / file.filename
        content = await file.read()
        saved_path.write_bytes(content)

        record = ReferenceRecord(
            project_id=project.id,
            filename=file.filename or "reference",
            stored_path=str(saved_path),
            content_type=file.content_type,
            file_size=len(content),
        )
        session.add(record)
        session.commit()

        return {
            "project_id": project.id,
            "filename": record.filename,
            "stored_path": record.stored_path,
            "file_size": record.file_size,
            "status": "uploaded",
        }
    finally:
        session.close()


@router.get("/projects/{project_id}/references")
def list_references(project_id: int):
    session = SessionLocal()
    try:
        rows = session.query(ReferenceRecord).filter(ReferenceRecord.project_id == project_id).all()
        return [{
            "id": row.id,
            "filename": row.filename,
            "path": row.stored_path,
            "content_type": row.content_type,
            "file_size": row.file_size,
            "uploaded_at": row.uploaded_at.isoformat(),
        } for row in rows]
    finally:
        session.close()


@router.post("/projects/{project_id}/run-workflow")
def run_workflow(project_id: int):
    session = SessionLocal()
    try:
        project = session.query(ProjectRecord).filter(ProjectRecord.id == project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        version = ProjectVersionRecord(
            project_id=project.id,
            version=project.version,
            status="workflow-run",
            summary=f"Workflow de produção executado para {project.name}.",
        )
        session.add(version)
        project.status = "workflow-running"
        session.commit()

        return {
            "project_id": project.id,
            "project_name": project.name,
            "status": "workflow-running",
            "version": version.version,
            "summary": version.summary,
        }
    finally:
        session.close()
