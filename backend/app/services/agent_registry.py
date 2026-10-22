from __future__ import annotations

from typing import Dict, List


class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, dict] = {
            "research_agent": {
                "name": "Research Agent",
                "role": "Pesquisa contextual da obra e do tema.",
                "responsibilities": [
                    "identificar elementos-chave da obra",
                    "mapear fontes visuais e narrativas",
                    "definir regras de fidelidade",
                    "coletar contexto para planejamento",
                ],
            },
            "style_agent": {
                "name": "Style Agent",
                "role": "Definir identidade visual e estilo do addon.",
                "responsibilities": [
                    "definir estética principal",
                    "determinar nível de originalidade",
                    "mapear elementos de interface e textura",
                    "estabelecer coerência visual",
                ],
            },
            "asset_agent": {
                "name": "Asset Agent",
                "role": "Gerar estrutura de mobs, itens, texturas e UI.",
                "responsibilities": [
                    "projetar mobs e itens",
                    "organizar referência de textura",
                    "mapear UI customizada",
                    "gerar estrutura de recursos do pack",
                ],
            },
            "review_agent": {
                "name": "Review Agent",
                "role": "Revisar e corrigir divergências do addon.",
                "responsibilities": [
                    "validar consistência da obra",
                    "comparar proposta com regras do projeto",
                    "corrigir divergências estruturais",
                    "sugerir refinamentos de versão",
                ],
            },
            "export_agent": {
                "name": "Export Agent",
                "role": "Preparar e empacotar a entrega final.",
                "responsibilities": [
                    "montar estrutura de exportação",
                    "gerar zip e pacote final",
                    "validar dados finais para Bedrock",
                    "organizar histórico de versões",
                ],
            },
        }

    def list_agents(self) -> List[dict]:
        return [
            {
                "id": agent_id,
                "name": agent["name"],
                "role": agent["role"],
                "responsibilities": agent["responsibilities"],
            }
            for agent_id, agent in self.agents.items()
        ]
