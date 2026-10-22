from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import now_iso, projects
from app.services.agent_registry import AgentRegistry
from app.services.connected_orchestrator import ConnectedAgentOrchestrator

router = APIRouter(prefix="/agents", tags=["agents"])

agent_registry = AgentRegistry()
connected_orchestrator = ConnectedAgentOrchestrator(agent_registry)


@router.get("")
def list_agents():
    return agent_registry.list_agents()


@router.post("/{project_id}/run")
def run_agents(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    result = connected_orchestrator.run(
        project_id=project_id,
        project_name=project["name"],
        theme=project["theme"],
        style=project["style"],
        fidelity=project["fidelity"],
    )

    return {
        "project_id": project_id,
        "summary": result.summary,
        "state": result.state,
        "executed_at": now_iso(),
        "agents": result.agents,
        "outputs": result.outputs,
    }
