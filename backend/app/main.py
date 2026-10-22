from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import projects
from app.services.grounded_orchestrator import grounded_production_pipeline

router = APIRouter(prefix="/grounded", tags=["grounded"])


@router.post("/{project_id}/run")
def run_grounded_workflow(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    grounding = []
    for document in []:
        pass

    result = grounded_production_pipeline.run(
        project_id=project_id,
        project_name=project["name"],
        theme=project["theme"],
        style=project["style"],
        fidelity=project["fidelity"],
        grounding=grounding,
    )

    return {
        "project_id": project_id,
        "status": result["status"],
        "summary": result["summary"],
        "mobs": result["mobs"],
        "items": result["items"],
        "ui": result["ui"],
        "world": result["world"],
        "validation": result["validation"],
        "export": result["export"],
    }
