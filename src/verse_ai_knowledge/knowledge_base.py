from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .api_index import load_symbols, lookup
from .claims import resolve_claim
from .evidence import get_symbol_evidence
from .policy import canonical_source_trust, canonical_validation, repo_root

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_./<>:-]+")


class KnowledgeBase:
    """Read-only SDK façade over the repository knowledge and evidence stores.

    The SDK never upgrades an unsupported exact API claim. Missing exact evidence is
    represented by ``TODO(API VERIFY)`` through :meth:`resolve_claim`.
    """

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root).resolve() if root else repo_root()

    def lookup_api(self, symbol: str) -> dict[str, Any] | None:
        return lookup(symbol, self.root)[0]

    def resolve_claim(self, symbol: str, field: str = "presence") -> dict[str, Any]:
        return resolve_claim(symbol, field, root=self.root)

    def get_evidence(self, symbol: str) -> dict[str, Any] | None:
        return get_symbol_evidence(symbol, self.root)

    def get_coverage(self) -> dict[str, Any]:
        return self._json("knowledge/api/coverage.json")

    def get_verification_queue(self, limit: int = 30) -> dict[str, Any]:
        data = self._json("knowledge/api/verification_queue.json")
        entries = list(data.get("entries") or data.get("queue") or [])[: max(0, limit)]
        return {"entries": entries, "count": len(entries)}

    def get_status(self) -> dict[str, Any]:
        manifest = self._json("manifest.json")
        return {
            "release": manifest.get("release", {}).get("version"),
            "schema": manifest.get("schema_version"),
            "api_snapshot": manifest.get("verse_api_version"),
            "uefn_compile": "NOT TESTED unless matching verification evidence exists",
            "runtime": "NOT TESTED unless matching runtime evidence exists",
            "multiplayer": "NOT TESTED unless matching multiplayer evidence exists",
        }

    def get_routing(self) -> str:
        return (self.root / "knowledge/ROUTING.md").read_text(encoding="utf-8")

    def search(self, query: str, limit: int = 12) -> list[dict[str, Any]]:
        """Search the deterministic local RAG index with a compact BM25 score.

        This is retrieval, not evidence promotion. Source authority and field-level
        claim resolution still decide whether an exact API claim may be emitted.
        """
        index = self._json("rag/index.json")
        config = self._json("rag/config.json")
        query_tokens = self._tokens(query)
        docs = index.get("documents", [])
        avgdl = index.get("avg_document_length") or 1.0
        n_docs = max(int(index.get("document_count") or len(docs)), 1)
        df = index.get("document_frequency", {})
        weights = config.get("weights", {})
        trust_scores = config.get("source_trust_scores", {})
        validation_scores = config.get("validation_scores", {})

        rows: list[tuple[float, dict[str, Any]]] = []
        for doc in docs:
            tf = doc.get("term_freq", {})
            dl = max(int(doc.get("token_count") or 1), 1)
            score = 0.0
            for token in query_tokens:
                freq = int(tf.get(token, 0))
                if not freq:
                    continue
                seen = int(df.get(token, 0))
                idf = math.log(1 + (n_docs - seen + 0.5) / (seen + 0.5))
                score += idf * ((freq * 2.5) / (freq + 1.5 * (1 - 0.75 + 0.75 * dl / avgdl)))
            path = str(doc.get("path", "")).lower()
            title = str(doc.get("title", "")).lower()
            for token in query_tokens:
                if token in path:
                    score += float(weights.get("path_exact", 4.0)) * 0.35
                if token in title:
                    score += float(weights.get("title_exact", 4.0)) * 0.35
            trust = canonical_source_trust(doc.get("source_trust"))
            validation = canonical_validation(doc.get("validation"))
            score += float(trust_scores.get(trust, trust_scores.get("unknown", 0.35))) * float(
                weights.get("source_trust", 4.0)
            )
            score += float(validation_scores.get(validation, 0.25)) * float(weights.get("validation", 2.5))
            if score > 0:
                rows.append(
                    (
                        score,
                        {
                            "path": doc.get("path"),
                            "title": doc.get("title"),
                            "source_trust": trust,
                            "validation": validation,
                            "content_role": doc.get("content_role", "data"),
                        },
                    )
                )
        rows.sort(key=lambda item: (-item[0], str(item[1].get("path"))))
        return [{"score": round(score, 3), **row} for score, row in rows[: max(0, limit)]]

    def search_errors(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        path = self.root / "errors/error_memory.jsonl"
        if not path.exists():
            return []
        needles = self._tokens(query)
        matches: list[tuple[int, dict[str, Any]]] = []
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            hay = json.dumps(row, ensure_ascii=False).lower()
            score = sum(hay.count(token) for token in needles)
            if score:
                matches.append((score, row))
        matches.sort(key=lambda item: -item[0])
        return [row for _, row in matches[: max(0, limit)]]

    def get_project_context(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        registry = self.root / "projects/project_registry.json"
        if not registry.exists():
            return []
        data = json.loads(registry.read_text(encoding="utf-8"))
        rows = data.get("projects") if isinstance(data, dict) else data
        if not isinstance(rows, list):
            return []
        terms = self._tokens(query)
        ranked: list[tuple[int, dict[str, Any]]] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            hay = json.dumps(row, ensure_ascii=False).lower()
            score = sum(hay.count(term) for term in terms)
            if score:
                ranked.append((score, row))
        ranked.sort(key=lambda item: -item[0])
        return [row for _, row in ranked[: max(0, limit)]]

    def validate_generated_claims(self, claims: list[dict[str, str]]) -> dict[str, Any]:
        """Resolve explicit claims supplied by a caller.

        The caller supplies ``[{"symbol": ..., "field": ...}]``. This method does not
        guess which identifiers in arbitrary Verse are built-in APIs.
        """
        results = []
        for claim in claims:
            symbol = str(claim.get("symbol", "")).strip()
            field = str(claim.get("field", "presence")).strip() or "presence"
            if not symbol:
                results.append({"decision": "TODO(API VERIFY)", "reason": "Missing symbol."})
                continue
            results.append(self.resolve_claim(symbol, field))
        unresolved = sum(1 for row in results if row.get("decision") != "ALLOW")
        return {"results": results, "unresolved_count": unresolved}

    def known_symbols(self) -> list[dict[str, Any]]:
        return load_symbols(self.root)

    def _json(self, rel: str) -> dict[str, Any]:
        return json.loads((self.root / rel).read_text(encoding="utf-8"))

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return [token.lower() for token in _TOKEN_RE.findall(text)]
