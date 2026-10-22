from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class MultiAgentResult:
    project_id: str
    summary: str
    state: str
    agents: List[dict] = field(default_factory=list)
    outputs: List[dict] = field(default_factory=list)


class ConnectedAgentOrchestrator:
    def __init__(self, agent_registry):
        self.agent_registry = agent_registry

    def run(self, project_id: str, project_name: str, theme: str, style: str, fidelity: str) -> MultiAgentResult:
        agents = self.agent_registry.list_agents()

        outputs = [
            {
                "agent": "research_agent",
                "status": "completed",
                "message": f"Análise contextual concluída para '{theme}' com foco em fidelidade e identidade da obra.",
            },
            {
                "agent": "style_agent",
                "status": "completed",
                "message": f"Estilo definido como '{style}' com nível de fidelidade '{fidelity}'.",
            },
            {
                "agent": "asset_agent",
                "status": "completed",
                "message": "Mobs, itens, recursos e UI foram mapeados para a estrutura base do addon.",
            },
            {
                "agent": "review_agent",
                "status": "completed",
                "message": "Revisão de consistência concluída com ajustes de identidade e estrutura.",
            },
            {
                "agent": "export_agent",
                "status": "pending",
                "message": "Exportação final em andamento para empacotamento do addon.",
            },
        ]

        return MultiAgentResult(
            project_id=project_id,
            summary=(
                f"Fluxo multiagente concluído para '{project_name}'. "
                f"O addon foi planejado com foco em '{theme}', estilo '{style}' e fidelidade '{fidelity}'."
            ),
            state="orchestrated",
            agents=agents,
            outputs=outputs,
        )
