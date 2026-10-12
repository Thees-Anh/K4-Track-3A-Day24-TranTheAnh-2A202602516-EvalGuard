"""Fast deterministic reranker used when a cross-encoder is unavailable."""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class RerankedResult:
    text: str
    score: float
    metadata: dict


class CrossEncoderReranker:
    def rerank(self, question: str, docs: list[dict], top_k: int = 3):
        query = set(re.findall(r"\w+", question.lower(), re.UNICODE))
        rows = []
        for doc in docs:
            terms = set(re.findall(r"\w+", doc["text"].lower(), re.UNICODE))
            overlap = len(query & terms) / max(1, len(query))
            score = .7 * overlap + .3 * float(doc.get("score", 0))
            rows.append(RerankedResult(doc["text"], score, dict(doc.get("metadata", {}))))
        return sorted(rows, key=lambda row: row.score, reverse=True)[:top_k]
