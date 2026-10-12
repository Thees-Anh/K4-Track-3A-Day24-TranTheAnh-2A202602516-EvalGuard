"""In-memory hybrid-style lexical retriever implementing the lab interface."""
from __future__ import annotations

from dataclasses import dataclass
import math
import re

from config import HYBRID_TOP_K


def _tokens(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


@dataclass
class SearchResult:
    text: str
    score: float
    metadata: dict


class HybridSearch:
    def __init__(self):
        self.chunks: list[dict] = []
        self.doc_freq: dict[str, int] = {}

    def index(self, chunks: list[dict]):
        self.chunks = list(chunks)
        self.doc_freq = {}
        for chunk in self.chunks:
            for token in set(_tokens(chunk["text"])):
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1

    def search(self, question: str) -> list[SearchResult]:
        query = set(_tokens(question))
        total = max(1, len(self.chunks))
        scored = []
        for chunk in self.chunks:
            terms = set(_tokens(chunk["text"]))
            score = sum(math.log((total + 1) / (self.doc_freq.get(t, 0) + 1)) + 1
                        for t in query & terms)
            score /= math.sqrt(max(1, len(terms)))
            scored.append(SearchResult(chunk["text"], float(score), dict(chunk.get("metadata", {}))))
        return sorted(scored, key=lambda row: row.score, reverse=True)[:HYBRID_TOP_K]
