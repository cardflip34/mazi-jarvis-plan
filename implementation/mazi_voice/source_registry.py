from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .contracts import utc_now

SOURCE_REGISTRY: dict[str, dict[str, list[str]]] = {
    "active_bots": {
        "description": "Active bot registry per machine.",
        "paths": ["ops/active_bots.json", "active_bots.json", "ops/fleet_status.json", "fleet_status.json"],
    },
    "live_append": {
        "description": "Current capture append log / logged sales stream.",
        "paths": [
            "ops/whatnot_auctions_live_append.jsonl",
            "whatnot_auctions_live_append.jsonl",
            "ops/whatnot_auctions.json",
            "whatnot_auctions.json",
        ],
    },
    "gemini_ocr_ledger": {
        "description": "Gemini/OCR read ledger and throughput signal.",
        "paths": [
            "ops/gemini_identity_updates.jsonl",
            "ops/gemini_cost_telemetry.jsonl",
            "reports/gemini_usage_by_source.jsonl",
            "ops/gemini_status.json",
            "ops/gemini_backlog.json",
            "ops/gemini_reads.json",
            "gemini_status.json",
            "gemini_backlog.json",
            "gemini_reads.json",
        ],
    },
    "front_proof_evidence": {
        "description": "Front/proof image evidence directories.",
        "paths": [
            "ops/frame_evidence",
            "ops/review_assets",
            "ops/captures",
            "captures",
            "card_evidence",
            "review_assets",
        ],
    },
    "service_health": {
        "description": "Per-service health files and fleet status.",
        "paths": ["ops/fleet_health.json", "ops/load_status.json", "ops/bot_team_status.json", "fleet_status.json"],
    },
}

BLOCKED_PARTS = {".env", "cookies", "browser_state", "browser-state", "secrets"}


@dataclass(frozen=True)
class RegistryRoot:
    machine: str
    root: Path
    via: str = "local"


def _safe_path(path: Path) -> bool:
    return not ({part.lower() for part in path.parts} & BLOCKED_PARTS)


def _format_mtime(path: Path) -> tuple[str | None, int | None]:
    try:
        modified = path.stat().st_mtime
    except OSError:
        return None, None
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(modified)), int(max(0, time.time() - modified))


def _confidence(path: Path, age_seconds: int | None) -> str:
    if age_seconds is None:
        return "missing"
    if path.suffix == ".jsonl" and age_seconds <= 15 * 60:
        return "high"
    if age_seconds <= 60 * 60:
        return "high"
    if age_seconds <= 24 * 60 * 60:
        return "medium"
    return "low"


def build_source_registry(roots: list[RegistryRoot]) -> dict[str, Any]:
    artifacts: dict[str, dict[str, Any]] = {}
    gaps: list[str] = []
    observed_at = utc_now()

    for artifact, spec in SOURCE_REGISTRY.items():
        rows: list[dict[str, Any]] = []
        for item in roots:
            for rel in spec["paths"]:
                path = item.root / rel
                if not _safe_path(path):
                    continue
                exists = path.exists()
                modified_at, age_seconds = _format_mtime(path) if exists else (None, None)
                rows.append(
                    {
                        "machine": item.machine,
                        "via": item.via,
                        "root": str(item.root),
                        "relative_path": rel,
                        "path": str(path),
                        "exists": exists,
                        "kind": "directory" if exists and path.is_dir() else "file",
                        "modified_at": modified_at,
                        "age_seconds": age_seconds,
                        "confidence": _confidence(path, age_seconds),
                    }
                )
        observed = [row for row in rows if row["exists"]]
        if not observed:
            gaps.append(f"{artifact} source not located")
        artifacts[artifact] = {
            "description": spec["description"],
            "status": "observed" if observed else "missing",
            "observed": observed,
            "candidates": rows,
        }

    return {
        "status": "observed" if not gaps else "partial",
        "artifacts": artifacts,
        "source_gaps": gaps,
        "observed_at": observed_at,
    }


def local_registry_roots(root_paths: list[Path], machine: str = "local") -> list[RegistryRoot]:
    return [RegistryRoot(machine=machine, root=path, via="local") for path in root_paths if path.is_dir()]


def remote_registry_rows(machine: str, roots: list[str]) -> list[dict[str, Any]]:
    return [
        {"machine": machine, "root": os.path.expanduser(root), "via": "ssh"}
        for root in roots
        if root
    ]
