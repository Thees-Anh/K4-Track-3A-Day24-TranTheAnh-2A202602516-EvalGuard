"""Local metadata enrichment that preserves chunk count and order."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnrichedChunk:
    enriched_text: str
    auto_metadata: dict


def enrich_chunks(chunks: list[dict]) -> list[EnrichedChunk]:
    rows = []
    for chunk in chunks:
        source = chunk.get("metadata", {}).get("source", "unknown")
        rows.append(EnrichedChunk(chunk["text"], {"source_type": source.rsplit(".", 1)[-1]}))
    return rows
