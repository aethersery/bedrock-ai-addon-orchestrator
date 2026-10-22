from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Dict, List

from pypdf import PdfReader


class DocumentCorpusService:
    def __init__(self):
        self.documents_by_project: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def ingest_file(self, project_id: str, filename: str, content: bytes, content_type: str | None = None) -> Dict[str, Any]:
        ext = self._extension(filename)
        if ext == ".pdf":
            text = self._extract_pdf_text(content)
        elif ext in {".txt", ".md", ".json", ".csv"}:
            text = content.decode("utf-8", errors="ignore")
        else:
            text = content.decode("utf-8", errors="ignore")

        chunks = self._chunk_text(text)
        entry = {
            "filename": filename,
            "content_type": content_type or "application/octet-stream",
            "chunk_count": len(chunks),
            "chunks": chunks,
            "source": "uploaded",
        }
        self.documents_by_project[project_id].append(entry)
        return entry

    def list_documents(self, project_id: str) -> List[Dict[str, Any]]:
        return self.documents_by_project.get(project_id, [])

    def search(self, project_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not query:
            return []

        query_tokens = self._tokenize(query)
        results: List[Dict[str, Any]] = []

        for document in self.documents_by_project.get(project_id, []):
            for idx, chunk in enumerate(document["chunks"]):
                chunk_tokens = self._tokenize(chunk)
                score = self._score_chunk(chunk_tokens, query_tokens)
                if score > 0:
                    results.append({
                        "filename": document["filename"],
                        "chunk_index": idx,
                        "score": round(score, 4),
                        "text": chunk,
                    })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]

    def _extension(self, filename: str) -> str:
        return filename.lower()[filename.rfind("."):] if "." in filename else ""

    def _extract_pdf_text(self, content: bytes) -> str:
        try:
            reader = PdfReader(bytes_content(content))
            pages: List[str] = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)
            return "\n\n".join(pages)
        except Exception:
            return content.decode("utf-8", errors="ignore")

    def _chunk_text(self, text: str, chunk_size: int = 1200) -> List[str]:
        cleaned = re.sub(r"\s+", " ", text).strip()
        if not cleaned:
            return []
        chunks: List[str] = []
        for i in range(0, len(cleaned), chunk_size):
            chunk = cleaned[i:i + chunk_size].strip()
            if chunk:
                chunks.append(chunk)
        return chunks

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9À-ÿ]+", text.lower())

    def _score_chunk(self, chunk_tokens: List[str], query_tokens: List[str]) -> float:
        if not query_tokens:
            return 0.0

        chunk_counter = defaultdict(int)
        for token in chunk_tokens:
            chunk_counter[token] += 1

        score = 0.0
        for token in query_tokens:
            if token in chunk_counter:
                score += chunk_counter[token]
                score += 0.25
        score += 0.5 * len(set(query_tokens) & set(chunk_tokens))
        return score


def bytes_content(content: bytes):
    from io import BytesIO
    return BytesIO(content)


document_corpus_service = DocumentCorpusService()
