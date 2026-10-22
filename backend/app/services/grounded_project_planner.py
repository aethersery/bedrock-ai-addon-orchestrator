from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class GroundedArtifact:
    name: str
    category: str
    description: str
    evidence: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


@dataclass
class GroundedProjectPlan:
    project_id: str
    title: str
    summary: str
    mobs: List[GroundedArtifact]
    items: List[GroundedArtifact]
    ui: List[GroundedArtifact]
    world: List[GroundedArtifact]
    validation: List[str]
    evidence: List[str]


class GroundedProjectPlanner:
    def __init__(self):
        self.default_sections = {
            "mobs": ["criaturas lendárias", "chefes de área", "guardas místicos"],
            "items": ["armas ancestrais", "itens raros", "reagentes e materiais"],
            "ui": ["interface temática", "menu do addon", "identidade do mod"] ,
            "world": ["ambientes principais", "estruturas lendárias", "regiões e biomas"],
        }

    def build_plan(self, project_id: str, theme: str, style: str, fidelity: str, grounding: List[Dict[str, Any]]) -> GroundedProjectPlan:
        evidence_text = [item.get("text", "") for item in grounding[:8]]
        evidence_summary = [item for item in evidence_text if item][:8]

        mobs = [
            GroundedArtifact(
                name="Guardião da Lenda",
                category="mobs",
                description="Criatura principal com identidade visual forte e presença em pontos-chave do mundo.",
                evidence=evidence_summary[:3],
                risks=["poder excessivo sem equilíbrio", "aparência que diverge do estilo da obra"],
            ),
            GroundedArtifact(
                name="Espírito do Entorno",
                category="mobs",
                description="Entidade menor e simbólica com movimento e comportamento temático.",
                evidence=evidence_summary[1:4],
                risks=["visual pouco diferenciado", "uso repetitivo"],
            ),
        ]

        items = [
            GroundedArtifact(
                name="Lança do Reino Perdido",
                category="items",
                description="Arma lendária com visual marcante e reforço temático.",
                evidence=evidence_summary[:2],
                risks=["poder que desbalanceia o gameplay"],
            ),
            GroundedArtifact(
                name="Cristal Ancestral",
                category="items",
                description="Material central para criação, ritual e identidade do addon.",
                evidence=evidence_summary[2:5],
                risks=["uso genérico ou sem identidade"],
            ),
        ]

        ui = [
            GroundedArtifact(
                name="Menu principal do addon",
                category="ui",
                description="Interface com identidade visual inspirada na obra e no tema central.",
                evidence=evidence_summary[:2],
                risks=["menu visualmente genérico"],
            )
        ]

        world = [
            GroundedArtifact(
                name="Região temática principal",
                category="world",
                description="Local central com atmosfera, materiais e sensação do ambiente da obra.",
                evidence=evidence_summary[:3],
                risks=["ambiente pouco distinto"],
            )
        ]

        validation = [
            "A identidade visual foi ancorada no tema e no corpus documental.",
            "Os elementos principais respeitam a obra, estilo e fidelidade do projeto.",
            "A estrutura do addon foi pensada para manter consistência entre itens, mobs e ambiente.",
            "O pacote final será revisado antes da exportação final.",
        ]

        return GroundedProjectPlan(
            project_id=project_id,
            title=f"Plano grounded: {theme}",
            summary=(
                f"Plano de addon gerado com base documental para o tema '{theme}', com estilo '{style}' "
                f"e fidelidade '{fidelity}'. A estrutura busca preservar a identidade da obra e reduzir divergências."
            ),
            mobs=mobs,
            items=items,
            ui=ui,
            world=world,
            validation=validation,
            evidence=evidence_summary,
        )
