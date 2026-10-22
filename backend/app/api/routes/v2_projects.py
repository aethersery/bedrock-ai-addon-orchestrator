from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.services.repositories import ProjectRepository, VersionRepository

router = APIRouter(prefix="/v2", tags=["v2"])

project_repository = ProjectRepository()
version_repository = VersionRepository()


class ProjectPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=2, max_length=120)
    theme: str = Field(..., min_length=2, max_length=250)
    style: str = Field(default="inspiracao-fiel")
    fidelity: str = Field(default="high")
    version: str = Field(default="0.0.1")
    target_platform: str = Field(default="bedrock-1.20+")


@router.post("/projects")
def create_project(payload: ProjectPayload):
    project = project_repository.create({
        "name": payload.name,
        "theme": payload.theme,
        "style": payload.style,
        "fidelity": payload.fidelity,
        "version": payload.version,
        "target_platform": payload.target_platform,
        "created_at": datetime.utcnow().isoformat(),
    })
    return project


@router.get("/projects")
def list_projects():
    return project_repository.list()


@router.get("/projects/{project_id}")
def get_project(project_id: str):
    if project_id not in project_repository._projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_repository.get(project_id)


@router.post("/projects/{project_id}/versions")
def add_version(project_id: str):
    if project_id not in project_repository._projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = project_repository.get(project_id)
    version = {
        "id": f"ver-{len(version_repository.list_for_project(project_id)) + 1:04d}",
        "project_id": project_id,
        "version": project["version"],
        "created_at": datetime.utcnow().isoformat(),
        "status": "created",
        "summary": f"Versão inicial do projeto {project['name']}.",
    }
    return version_repository.add(project_id, version)


@router.get("/projects/{project_id}/versions")
def list_versions(project_id: str):
    if project_id not in project_repository._projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return version_repository.list_for_project(project_id)
