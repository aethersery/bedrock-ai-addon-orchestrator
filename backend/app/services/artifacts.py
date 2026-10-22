from __future__ import annotations


class ArtifactService:
    def __init__(self):
        self._artifacts = {}

    def create_artifact(self, project_id: str, artifact_type: str, payload: dict) -> dict:
        artifact = {
            "project_id": project_id,
            "type": artifact_type,
            **payload,
        }
        self._artifacts.setdefault(project_id, []).append(artifact)
        return artifact

    def list_for_project(self, project_id: str):
        return self._artifacts.get(project_id, [])
