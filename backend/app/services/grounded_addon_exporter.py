from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


class GroundedAddonExporter:
    def __init__(self, output_dir: str = "/tmp/grounded-bedrock-export"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build(self, project_name: str, grounded_plan: dict) -> dict:
        project_dir = self.output_dir / project_name.lower().replace(" ", "-")
        project_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "format_version": 2,
            "header": {
                "name": project_name,
                "description": grounded_plan["summary"],
                "version": [1, 0, 0],
                "uuid": "10000000-0000-0000-0000-000000000001",
                "min_engine_version": [1, 20, 0],
            },
            "modules": [
                {"type": "data", "uuid": "10000000-0000-0000-0000-000000000002", "version": [1, 0, 0]},
                {"type": "resources", "uuid": "10000000-0000-0000-0000-000000000003", "version": [1, 0, 0]},
            ],
        }

        artifact_doc = {
            "project": project_name,
            "summary": grounded_plan["summary"],
            "mobs": [item["name"] for item in grounded_plan.get("mobs", [])],
            "items": [item["name"] for item in grounded_plan.get("items", [])],
            "ui": [item["name"] for item in grounded_plan.get("ui", [])],
            "world": [item["name"] for item in grounded_plan.get("world", [])],
            "validation": grounded_plan.get("validation", []),
            "evidence": grounded_plan.get("evidence", []),
        }

        for folder_name in ["behavior_pack", "resource_pack", "ui", "scripts", "docs"]:
            (project_dir / folder_name).mkdir(parents=True, exist_ok=True)

        (project_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        (project_dir / "docs" / "grounded_plan.json").write_text(json.dumps(artifact_doc, indent=2), encoding="utf-8")
        (project_dir / "ui" / "main_menu.json").write_text(json.dumps({"menu": {"title": project_name}}, indent=2), encoding="utf-8")
        (project_dir / "scripts" / "main.js").write_text("console.log('grounded addon initialized');\n", encoding="utf-8")
        (project_dir / "README.md").write_text(f"# {project_name}\n\n{grounded_plan['summary']}\n", encoding="utf-8")

        archive_path = self.output_dir / f"{project_name.lower().replace(' ', '-')}.zip"
        with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as zip_file:
            for file_path in sorted(project_dir.rglob("*")):
                if file_path.is_file():
                    zip_file.write(file_path, file_path.relative_to(project_dir.parent))

        return {
            "project_dir": str(project_dir),
            "archive_path": str(archive_path),
            "manifest": manifest,
            "artifacts": artifact_doc,
        }
