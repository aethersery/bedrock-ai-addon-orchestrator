from __future__ import annotations

from typing import Any, Dict, List

from app.services.grounded_addon_exporter import GroundedAddonExporter
from app.services.grounded_project_planner import GroundedProjectPlanner


class GroundedProductionPipeline:
    def __init__(self):
        self.planner = GroundedProjectPlanner()
        self.exporter = GroundedAddonExporter()

    def run(self, project_id: str, project_name: str, theme: str, style: str, fidelity: str, grounding: List[Dict[str, Any]]) -> Dict[str, Any]:
        plan = self.planner.build_plan(project_id, theme, style, fidelity, grounding)
        export = self.exporter.build(project_name, {
            "summary": plan.summary,
            "mobs": [
                {"name": item.name, "description": item.description, "evidence": item.evidence}
                for item in plan.mobs
            ],
            "items": [
                {"name": item.name, "description": item.description, "evidence": item.evidence}
                for item in plan.items
            ],
            "ui": [
                {"name": item.name, "description": item.description, "evidence": item.evidence}
                for item in plan.ui
            ],
            "world": [
                {"name": item.name, "description": item.description, "evidence": item.evidence}
                for item in plan.world
            ],
            "validation": plan.validation,
            "evidence": plan.evidence,
        })

        return {
            "project_id": project_id,
            "project_name": project_name,
            "summary": plan.summary,
            "mobs": [
                {"name": item.name, "description": item.description, "risks": item.risks, "evidence": item.evidence}
                for item in plan.mobs
            ],
            "items": [
                {"name": item.name, "description": item.description, "risks": item.risks, "evidence": item.evidence}
                for item in plan.items
            ],
            "ui": [
                {"name": item.name, "description": item.description, "risks": item.risks, "evidence": item.evidence}
                for item in plan.ui
            ],
            "world": [
                {"name": item.name, "description": item.description, "risks": item.risks, "evidence": item.evidence}
                for item in plan.world
            ],
            "validation": plan.validation,
            "evidence": plan.evidence,
            "export": export,
            "status": "completed",
        }


grounded_production_pipeline = GroundedProductionPipeline()
