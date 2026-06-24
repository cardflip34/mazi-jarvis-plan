# MAZI Jarvis Full Wiring Plan

## Current State

Jarvis/Hermes is installed locally and wired to MAZI through a single read-only MCP tool: `mazi_voice_request`.

Latest HUD audit update: 2026-06-22 8:04 PM Pacific.

Live checks passed:

- M4 SSH access works.
- Mini SSH access works.
- Hermes MCP sees one MAZI tool and connects successfully.
- The local HUD is running at `http://127.0.0.1:8765/`.
- The MAZI voice API answers: "which sellers are now live and capturing?"
- The HUD now has a read-only `/api/snapshot` endpoint with a 15 second cache.
- The HUD now auto-refreshes every 30 seconds and populates telemetry without requiring a first manual command.
- HUD controls now run approved read-only MAZI probes instead of only filling the command box.

Observed from the latest read-only probe:

- M4 sports: 6 active sellers under cap 6.
- Mini Pokemon: 1 active seller.
- Current seller list: `alldaycollectibles`, `dashlive`, `kkcardvault`, `kkconsignment`, `ksocards`, `sacramentocards`, `stellarcollectiblz`.
- Logged sales signal: about 53,330 rows from the current live append artifacts.
- M4 is at 6/6 bots and currently shows a high remote load watch item.
- Gemini reads are now located through the Phase 3 source registry.

Hermes voice dependencies are installed, including microphone access libraries and `faster-whisper`. Nous Portal login is complete and the MAZI MCP is configured. Browser HUD speech output is available through local macOS `say`; Hermes terminal voice mode remains push-to-talk with `Ctrl+B`.

## Phase 0: Keep The Boundary Read-Only

Status: done for the first bridge and reinforced in the HUD.

Rules:

- Jarvis can read MAZI files, process counts, SSH snapshots, and local HUD/API data.
- Jarvis cannot mutate trusted records, review state, databases, cookies, browser state, seller registries, git, or production processes.
- Any future action tool must start as a proposal/draft, not direct execution.

## Phase 1: Voice Launch

Goal: make Hermes the speaking/listening front end.

Status: done for push-to-talk Hermes voice; always-listening remains intentionally off.

Work:

- Hermes provider login is complete through Nous Portal.
- Start the HUD with `scripts/hermes/start_mazi_hud.sh`.
- Start Hermes with `scripts/hermes/start_mazi_hermes.sh`.
- Inside Hermes, enable voice with `/voice on`, then use `Ctrl+B` push-to-talk.
- Keep always-listening off until wake-word/noise behavior is proven.

Acceptance:

- Spoken: "MAZI, which sellers are now live and capturing?"
- Jarvis answers from M4/Mini source files with source timestamps.

## Phase 2: Remote Collector Coverage

Goal: one fast read-only snapshot for every major MAZI surface.

Status: in progress. The first unified read-only snapshot is live and covers M4/Mini bot health, load, seller roster, logged sales, front/proof image count, connector state, source gaps, and HUD freshness.

Add collectors for:

- M4 load, bot count, Chrome count, seller roster, logged sales, and front/proof image scan.
- Mini load, Pokemon bot count, Chrome count, seller roster, logged sales, and front/proof image scan.
- `8504` admin workbench status.
- `8765` ops dashboard status.
- `9008` internal triage status.
- `9009` public confirmed-card surface status.
- image proxy/fallback health.
- Gemini queue/read/throughput health.

Acceptance:

- "Check all analytics" returns a single coherent snapshot with no duplicate probing and no expensive full-file scans.

## Phase 3: MAZI Source Registry

Goal: stop guessing where metrics live.

Status: implemented locally.

Implemented registry artifacts:

- active bot registry per machine.
- current capture append log.
- Gemini/OCR read ledger.
- front/proof image evidence directories.
- per-service health files.

Known live Gemini sources now include:

- `ops/gemini_identity_updates.jsonl`
- `ops/gemini_cost_telemetry.jsonl`

Acceptance:

- Jarvis explains every number with source path, freshness, and confidence.

## Phase 4: Machine Split And Coordination

Goal: model M4 and Mini as separate local managers.

Status: partially implemented for read-only observability. The snapshot reports M4 and Mini separately and does not treat Mini Pokemon as an M4 sports issue.

Architecture:

- M4 manager owns sports capture, hard cap 6, accounts primary and `diamandpapi`.
- Mini manager owns Pokemon capture, small local cap, intended account `jloke`.
- No single M4 manager should control Mini by SSH until a real remote-agent layer exists.
- Coordination should happen through policy/lane ownership and read-only registries first.

Acceptance:

- Jarvis reports M4 and Mini separately and never describes a Mini Pokemon issue as an M4 sports issue.

## Phase 5: Conversational MAZI Intelligence

Goal: Jarvis should talk like an operator, not just print JSON.

Status: in progress. The router now handles live sellers, all analytics, machine split, bot health, bottlenecks, load/RAM, sales, fronts, and Gemini read count. More operator-style "what changed" and productivity/staleness intents remain.

Add intent coverage for:

- "Are we bottlenecked?"
- "Which sellers are productive?"
- "Which bots are stale but productive?"
- "Who is capturing zero output?"
- "What changed in the last hour?"
- "What did Gemini read per hour?"
- "Are fronts backing up?"
- "What should I look at next?"

Acceptance:

- Jarvis answers in a short spoken summary, then offers source-backed detail on the HUD.

## Phase 6: Approval-Gated Actions

Goal: add control without making voice dangerous.

Allowed first:

- draft a manager-safe launch command.
- draft a restart/reap recommendation.
- draft a bottleneck triage packet.
- draft a GitHub/ops issue summary.

Still blocked from direct voice execution:

- trusted/Mazified promotion.
- public release.
- production DB mutation.
- review mutation.
- git commit/push.
- cookies/browser state.
- seller registry mutation.
- secrets.
- destructive filesystem action.

Acceptance:

- Jarvis can propose, but a separate operator approval step executes.

## Phase 7: Hardening

Goal: make this durable enough to live on the desktop.

Status: partially implemented. Snapshot cache, freshness display, request audit logging, redaction, and bounded SSH probes are in place.

Work:

- add a local snapshot cache and freshness badges.
- add audit logs for every voice/MCP request.
- redact secrets and cookies from all displays.
- add timeout budgets per collector.
- add tests for M4/Mini remote probes.
- add launchd services for HUD and optional Hermes gateway.
- add a runbook for restoring SSH aliases and Hermes config.

Acceptance:

- The desktop can run all day without wedging, leaking secrets, or slowing capture machines.
