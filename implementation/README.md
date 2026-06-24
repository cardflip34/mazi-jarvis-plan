# Implementation Snapshot

This directory contains selected implementation files from the local Jarvis/Hermes bridge.

The full local bridge lives under the operator workspace, but this repo intentionally keeps only plan-safe implementation snapshots:

- `mazi_voice/source_registry.py`: the Phase 3 read-only source registry.
- `tests/test_source_registry.py`: unit coverage for registry path/freshness reporting.

Excluded on purpose:

- `mazi_voice_runtime/` request logs, outbox, and approval packets.
- `.hermes/` auth/config/runtime state.
- virtualenvs, caches, pyc files, and audio cache.
- MAZI production data, cookies, browser state, seller/operator data, logs, captures, and secrets.

Local verification after implementing Phase 3:

```text
Ran 42 tests in 1.683s
OK
```

Live read-only smoke check observed fresh Gemini ledger sources on M4 and reported `registry_status=observed` with no registry gaps.
