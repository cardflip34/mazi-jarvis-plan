# MAZI Jarvis / Hermes Wiring Plan

This repository captures the current MAZI Jarvis/Hermes wiring plan and implementation state.

Jarvis/Hermes is installed locally and wired to MAZI through a single read-only MCP tool:

- `mazi_voice_request`

The current bridge is intentionally read-only. Jarvis can inspect MAZI health, source snapshots, process state, and HUD/API data, but it must not mutate trusted records, databases, cookies, seller registries, git state, browser state, review state, or production processes.

## Current State

Latest HUD audit update: 2026-06-22 8:04 PM Pacific.

Live checks passed:

- M4 SSH access works.
- Mini SSH access works.
- Hermes MCP sees one MAZI tool and connects successfully.
- The local HUD is running at `http://127.0.0.1:8765/`.
- The MAZI voice API answers: "which sellers are now live and capturing?"
- The HUD has a read-only `/api/snapshot` endpoint with a 15 second cache.
- The HUD auto-refreshes every 30 seconds and populates telemetry without requiring a first manual command.
- HUD controls run approved read-only MAZI probes.

Observed from the latest read-only probe:

- M4 sports: 6 active sellers under cap 6.
- Mini Pokemon: 1 active seller.
- Current seller list: `alldaycollectibles`, `dashlive`, `kkcardvault`, `kkconsignment`, `ksocards`, `sacramentocards`, `stellarcollectiblz`.
- Logged sales signal: about 53,330 rows from current live append artifacts.
- M4 is at 6/6 bots and shows a high remote load watch item.
- Gemini reads are now located through the read-only source registry added in Phase 3.

Hermes voice dependencies are installed, including microphone access libraries and `faster-whisper`. Nous Portal login is complete and the MAZI MCP is configured. Browser HUD speech output is available through local macOS `say`; Hermes terminal voice mode remains push-to-talk with `Ctrl+B`.

## Phase Summary

| Phase | Name | Status |
| --- | --- | --- |
| 0 | Keep the boundary read-only | Done |
| 1 | Voice launch | Done for push-to-talk Hermes voice |
| 2 | Remote collector coverage | In progress |
| 3 | MAZI source registry | Implemented locally |
| 4 | Machine split and coordination | Partially implemented |
| 5 | Conversational MAZI intelligence | In progress |
| 6 | Approval-gated actions | Planned |
| 7 | Hardening | Partially implemented |

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for the full plan.

## Safety Principles

- Read-only comes first.
- Source-backed answers should include freshness, source path, and confidence.
- Voice must propose actions before anything executable exists.
- Future write/control tools require explicit operator approval.
- Secrets, cookies, browser state, seller registries, trusted records, review state, production DBs, and git operations remain blocked from direct voice execution.
