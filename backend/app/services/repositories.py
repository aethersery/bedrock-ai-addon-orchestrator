from __future__ import annotations

from typing import List


class ProjectRepository:
    def __init__(self):
        self._projects: dict = {}

    def create(self, payload: dict) -> dict:
        project_id = f"proj-{len(self._projects) + 1:04d}"
        project = {
            **payload,
            "id": project_id,
            "status": "draft",
            "created_at": payload.get("created_at"),
            "summary": payload.get("summary", "Projeto criado e aguardando planejamento."),
        }
        self._projects[project_id] = project
        return project

    def list(self) -> List[dict]:
        return list(self._projects.values())

    def get(self, project_id: str) -> dict:
        return self._projects[project_id]

    def update(self, project_id: str, patch: dict) -> dict:
        self._projects[project_id].update(patch)
        return self._projects[project_id]

    def delete(self, project_id: str) -> None:
        self._projects.pop(project_id, None)


class VersionRepository:
    def __init__(self):
        self._versions: dict = {}

    def list_for_project(self, project_id: str) -> List[dict]:
        return self._versions.get(project_id, [])

    def add(self, project_id: str, version: dict) -> dict:
        current = self._versions.setdefault(project_id, [])
        current.append(version)
        return version
