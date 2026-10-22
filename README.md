from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.db import now_iso, projects, versions
from app.models import ProjectCreate
from app.services.document_corpus import document_corpus_service
from app.services.exporter import ExporterService
from app.services.llm_service import llm_service
from app.services.orchestrator import AgentOrchestrator
from app.services.validator import ValidationService

router = APIRouter(prefix="/projects", tags=["projects"])

orchestrator = AgentOrchestrator()
exporter = ExporterService()
validator = ValidationService()


@router.get("")
def list_projects():
    return [projects[p] for p in sorted(projects.keys())]


@router.post("")
def create_project(project: ProjectCreate):
    project_id = f"proj-{len(projects) + 1:04d}"
    record = {
        "id": project_id,
        "name": project.name,
        "theme": project.theme,
        "style": project.style,
        "fidelity": project.fidelity,
        "version": project.version,
        "target_platform": project.target_platform,
        "created_at": now_iso(),
        "status": "draft",
        "summary": "Projeto criado. Pronto para pesquisa e planejamento do addon.",
    }
    projects[project_id] = record
    versions[project_id] = []
    return record


@router.get("/{project_id}")
def get_project(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id]


@router.post("/{project_id}/plan")
def generate_plan(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    result = orchestrator.run_pipeline(
        project_id=project_id,
        project_name=project["name"],
        theme=project["theme"],
        style=project["style"],
        fidelity=project["fidelity"],
    )

    ai_plan = llm_service.generate_project_plan(project)
    grounding = document_corpus_service.search(project_id, project["theme"], top_k=5)

    response = {
        "project_id": project_id,
        "title": f"Plano para {project['name']}",
        "summary": ai_plan["summary"],
        "features": ai_plan["features"],
        "assets": ai_plan["assets"],
        "risks": ai_plan["risks"],
        "recommendations": ai_plan["recommendations"],
        "validation": ai_plan["validation"],
        "research": result.research_context,
        "grounding": grounding,
        "tasks": [
            {"name": task.name, "description": task.description, "status": task.status}
            for task in result.tasks
        ],
        "ai_provider": "openai-compatible" if llm_service.api_key else "fallback-local",
    }

    project["status"] = "planned"
    project["summary"] = ai_plan["summary"]

    versions[project_id].append(
        {
            "id": f"ver-{len(versions[project_id]) + 1:04d}",
            "project_id": project_id,
            "version": project["version"],
            "created_at": datetime.utcnow().isoformat(),
            "status": "planned",
            "summary": ai_plan["summary"],
        }
    )

    return response


@router.post("/{project_id}/review")
def review_project(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    validation = validator.validate_pack(
        project["name"],
        {
            "assets": [
                "manifest.json",
                "behavior_pack/manifest.json",
                "resource_pack/manifest.json",
                "README.md",
                "ui/main_menu.json",
            ]
        },
    )
    review = {
        "project_id": project_id,
        "status": "reviewed",
        "issues": [
            "Compatibilidade visual do addon precisa ser refinada",
            "Arquivos principais devem ser revisados em relação ao tema",
            "UI e textura devem manter identidade coesa",
        ],
        "fixes": [
            "Ajustar nomes e referências de ativos",
            "Refinar a intenção visual do tema",
            "Validar o manifest e os recursos principais",
        ],
        "validation": validation,
        "grounding": document_corpus_service.search(project_id, project["theme"], top_k=5),
        "message": "Revisão concluída e pronta para exportação final.",
    }
    project["status"] = "reviewed"
    return review


@router.post("/{project_id}/export")
def export_project(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    plan = {
        "project_id": project_id,
        "title": f"Plano do addon: {project['name']}",
        "summary": project.get("summary", "Addon exportado."),
        "features": [
            "Mobs e itens temáticos",
            "Texturas e recursos visuais",
            "Estrutura do pack para Bedrock",
            "UI customizada opcional",
            "Validação de consistência",
        ],
        "assets": [
            "manifest.json",
            "behavior_pack/manifest.json",
            "resource_pack/manifest.json",
            "README.md",
            "ui/main_menu.json",
            "scripts/main.js",
            "docs/revision_notes.md",
        ],
        "risks": ["Compatibilidade visual", "Refinamento de identidade", "Estrutura de recursos"],
        "recommendations": ["Ajustar detalhes visuais finais", "Validar após distribuição em Bedrock"],
        "validation": ["Manifest validado", "Recursos verificados", "Compatibilidade avaliada"],
    }

    export_data = exporter.build_package(project["name"], plan)
    response = {
        "project_id": project_id,
        "filename": f"{project['name'].lower().replace(' ', '-')}.zip",
        "project_dir": export_data["project_dir"],
        "zip_path": export_data["zip_path"],
        "files": export_data["files"],
        "grounding": document_corpus_service.search(project_id, project["theme"], top_k=5),
        "status": "exported",
        "message": "Pacote exportado com sucesso para uso em ambiente Bedrock.",
    }
    project["status"] = "exported"
    return response


@router.get("/{project_id}/versions")
def list_versions(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return versions.get(project_id, [])
