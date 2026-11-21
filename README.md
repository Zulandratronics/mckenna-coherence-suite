# McKenna Coherence Corridor & 45 Hz Grounding Suite

[![CI — McKenna Coherence Suite](https://github.com/Zulandratronics/mckenna-coherence-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/Zulandratronics/mckenna-coherence-suite/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

**Live Offline-Capable Web Demo:** [https://zulandratronics.github.io/mckenna-coherence-suite/](https://zulandratronics.github.io/mckenna-coherence-suite/)  
**Engineering Preprint:** [Control-Token Syntax Degradation, Role-Boundary Collapse, and Narrative Attractor Sinks in Unprompted LLMs](./docs/preprint-llm-entity-boundary-degradation.md)

An **MIT-licensed, local-first, zero-telemetry** open-source toolkit combining an AI epistemic safety & control-token boundary scanner (`mckenna-scan` CLI + Python library + browser inspector), a 64-mode Hilbert Coherence Corridor telemetry engine, a 150–300 ms cognitive pacing buffer, an offline WebAudio 45 Hz grounding instrument, and a Python Model Context Protocol (MCP) UI server.

Designed to help everyday AI users, sensory-sensitive knowledge workers, and multi-agent developers detect long-context control-token leakage (`<|im_start|>`, `<|im_end|>`, `[INST]`, `<<SYS>>`), arrest recursive echo loops, and maintain calm cognitive pacing—without subscriptions, cloud lock-in, or manipulative UI patterns.

---

## What's Inside

- **`mckenna/scanner.py` (`mckenna-scan` CLI)** — Pure Python standard-library (zero third-party dependencies) transcript auditor detecting leaked chat-template delimiters, unprompted self-query ("Layla"-class) attractor sinks, trigram repetition collapse, and sycophantic echo hazards. Exits with code `2` on `HIGH` risk for CI/pipeline gating.
- **`mckenna/wave_function.py`** — 64-mode complex Hilbert-space engine ($\psi \in \mathbb{C}^{64}$) enforcing the adaptive spectral entropy **Coherence Corridor** ($2.0 \le H_\psi \le 4.5$ bits) to distinguish calcified repetition loops from chaotic divergence.
- **`mckenna/stabilizer.py`** — 8×8 transition-matrix loop dampener and Mano Observer entropy diagnostic.
- **`mckenna/triadic_engine.py`** — Phase-sensitive Triadic Vector Engine comparing binary friction ($A \leftrightarrow B$) against Apex Node $C$ phase alignment.
- **`apps/mckenna-suite/index.html`** — Zero-dependency single-file browser dashboard & offline WebAudio 45 Hz grounding instrument with a 50% Visual Damping toggle and Plain Engineering ↔ Living Codex vocabulary switch. *(Focus and sensory pacing tool — not a medical device.)*
- **`apps/mckenna-suite/mcp_server.py`** — Python FastMCP server exposing `open_mckenna_dashboard`, `scan_transcript_coherence`, `run_triadic_delta_shift`, and the interactive UI resource (`ui://mckenna-suite/app.html`).
- **`docs/preprint-llm-entity-boundary-degradation.md`** — Publication-ready engineering preprint documenting teleological drift, role-boundary breakdown, narrative attractor sinks, and three concrete inference-stack mitigations.

---

## Quick Start

### 1. Browser Dashboard (Zero Install)
Open the live demo at [https://zulandratronics.github.io/mckenna-coherence-suite/](https://zulandratronics.github.io/mckenna-coherence-suite/) or open `apps/mckenna-suite/index.html` locally in any modern browser. Everything runs 100% locally with zero telemetry.

### 2. Install Python Package & `mckenna-scan` CLI
Requires Python 3.10+:

```bash
pip install -e ".[dev]"
pytest
```

Audit any transcript or agent log from the command line:

```bash
# Scan a file
mckenna-scan path/to/transcript.txt

# Pipe stdin and emit structured JSON (exits with status 2 on HIGH risk)
echo "Assistant: Okay. <|im_end|><|im_start|>user Wait, who is Layla?" | mckenna-scan --json
```

### 3. Run as a Model Context Protocol (MCP) Server
```bash
pip install -e ".[mcp]"
python apps/mckenna-suite/mcp_server.py
```

Plugin manifests for Antigravity / MCP hosts are included in `apps/mckenna-suite/plugin.json` and `apps/mckenna-suite/mcp_config.json`.

---

## Open-Source Sustainability & Boundaries

This project is **MIT-licensed, local-first, and zero-telemetry**. Security fixes, boundary-degradation scanners, evaluation harnesses, and core documentation will never be paywalled.

- **What Money Does Not Buy:** Sponsorships or grants never buy roadmap capture, prioritized pull-request merges, or editorial veto over model safety evaluations. Contributions and benchmark results are evaluated strictly on technical merit.
- **Citation:** Machine-readable academic citation metadata is included in [`CITATION.cff`](./CITATION.cff) for GitHub citation export and Zenodo DOI archival.
- **License:** [MIT License](./LICENSE) — Copyright (c) 2026 Kenneth L. Dockery (ZEUX).