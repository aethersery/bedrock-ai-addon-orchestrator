from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Dict, List, Tuple


class GroundingService:
    def __init__(self):
        self.documents_by_project: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def add_document(self, project_id: str, filename: str, content: bytes, content_type: str | None = None) -> Dict[str, Any]:
        text = self._decode_content(content)
        chunks = self._chunk_text(text)
        document = {
            "filename": filename,
            "content_type": content_type or "application/octet-stream",
            "chunks": chunks,
            "chunk_count": len(chunks),
            "grounded": True,
        }
        self.documents_by_project[project_id].append(document)
        return document

    def search(self, project_id: str, query: str, top_k: int = 8) -> List[Dict[str, Any]]:
        if not query:
            return []

        tokens = self._tokenize(query)
        ranked: List[Tuple[float, Dict[str, Any]]] = []
        for document in self.documents_by_project.get(project_id, []):
            for idx, chunk in enumerate(document["chunks"]):
                score = self._score_chunk(chunk, tokens)
                if score > 0:
                    ranked.append((score, {
                        "filename": document["filename"],
                        "chunk_index": idx,
                        "score": round(score, 4),
                        "text": chunk,
                    }))

        ranked.sort(key=lambda item: item[0], reverse=True)
        return [entry for _, entry in ranked[:top_k]]

    def build_project_context(self, project_id: str, theme: str, top_k: int = 8) -> Dict[str, Any]:
        evidence = self.search(project_id, theme, top_k=top_k)
        all_tokens = []
        for document in self.documents_by_project.get(project_id, []):
            for chunk in document["chunks"]:
                all_tokens.extend(self._tokenize(chunk))

        freq = defaultdict(int)
        for token in all_tokens:
            freq[token] += 1

        key_terms = [
            term for term, _ in sorted(freq.items(), key=lambda item: item[1], reverse=True)[:12]
            if len(term) > 3
        ]

        return {
            "project_id": project_id,
            "theme": theme,
            "document_count": len(self.documents_by_project.get(project_id, [])),
            "key_terms": key_terms,
            "evidence": evidence,
            "research_summary": (
                "O corpus documental foi carregado e segmentado. O sistema usará as evidências mais relevantes "
                "para orientar a geração de mobs, itens, identidade visual e revisão do addon."
            ),
        }

    def _decode_content(self, content: bytes) -> str:
        candidates = [
            ("utf-8", "utf-8"),
            ("latin-1", "latin-1"),
            ("utf-16", "utf-16"),
        ]
        for encoding, name in candidates:
            try:
                return content.decode(encoding)
            except Exception:
                continue
        return content.decode("utf-8", errors="ignore")

    def _chunk_text(self, text: str, chunk_size: int = 1400) -> List[str]:
        cleaned = re.sub(r"\s+", " ", text).strip()
        if not cleaned:
            return []
        return [
            chunk.strip()
            for chunk in [cleaned[i:i + chunk_size] for i in range(0, len(cleaned), chunk_size)]
            if chunk.strip()
        ]

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9À-ÿ]+", text.lower())

    def _score_chunk(self, chunk: str, tokens: List[str]) -> float:
        if not tokens:
            return 0.0
        chunk_tokens = self._tokenize(chunk)
        if not chunk_tokens:
            return 0.0

        counter = defaultdict(int)
        for token in chunk_tokens:
            counter[token] += 1

        score = 0.0
        for token in tokens:
            if token in counter:
                score += counter[token] * 2.0
                score += 0.5
        score += 0.3 * len(set(tokens) & set(chunk_tokens))
        return score


grounding_service = GroundingService()
