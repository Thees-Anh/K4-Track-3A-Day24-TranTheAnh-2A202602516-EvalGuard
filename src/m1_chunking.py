"""Corpus loading and dependency-light hierarchical chunking."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from config import DATA_DIR, HIERARCHICAL_CHILD_SIZE, HIERARCHICAL_PARENT_SIZE


@dataclass
class Chunk:
    text: str
    metadata: dict
    parent_id: str


def load_documents() -> list[dict]:
    documents = []
    for path in sorted(Path(DATA_DIR).glob("*")):
        if path.suffix.lower() == ".md":
            text = path.read_text(encoding="utf-8")
        elif path.suffix.lower() == ".pdf":
            try:
                from pypdf import PdfReader
                text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
            except Exception:
                continue
        else:
            continue
        if text.strip():
            documents.append({"text": text, "metadata": {"source": path.name}})
    return documents


def _windows(text: str, size: int, overlap: int) -> list[str]:
    words = re.findall(r"\S+", text)
    if not words:
        return []
    step = max(1, size - overlap)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step)]


def chunk_hierarchical(text: str, metadata: dict | None = None):
    metadata = dict(metadata or {})
    parent_words = max(100, HIERARCHICAL_PARENT_SIZE // 4)
    child_words = max(50, HIERARCHICAL_CHILD_SIZE // 2)
    parents, children = [], []
    for p_index, parent_text in enumerate(_windows(text, parent_words, 40)):
        parent_id = f"{metadata.get('source', 'document')}::p{p_index}"
        parents.append(Chunk(parent_text, metadata, parent_id))
        for child_text in _windows(parent_text, child_words, 20):
            children.append(Chunk(child_text, metadata, parent_id))
    return parents, children
