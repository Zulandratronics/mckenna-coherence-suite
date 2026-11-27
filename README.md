# McKenna Coherence Corridor & 45 Hz Grounding Suite

[![CI — McKenna Coherence Suite](https://github.com/Zulandratronics/mckenna-coherence-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/Zulandratronics/mckenna-coherence-suite/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24412916.svg)](https://doi.org/10.5281/zenodo.24412916)

**Live Offline-Capable Web Demo:** [https://zulandratronics.github.io/mckenna-coherence-suite/](https://zulandratronics.github.io/mckenna-coherence-suite/)  
**Companion Epistemic Auditor:** [Counterweight](https://zulandratronics.github.io/counterweight/) ([GitHub](https://github.com/Zulandratronics/counterweight))  
**Engineering Preprint:** [Control-Token Syntax Degradation, Role-Boundary Collapse, and Narrative Attractor Sinks in Unprompted LLMs](./docs/preprint-llm-entity-boundary-degradation.md)

An **MIT-licensed, local-first, zero-telemetry** open-source toolkit combining an AI epistemic safety & control-token boundary scanner (`mckenna-scan` CLI + Python library + browser inspector), a 64-mode Hilbert Coherence Corridor telemetry engine with default **IndigoNoise** $1/f$ spectral recovery, a 150–300 ms cognitive pacing buffer, an offline WebAudio 45 Hz & IndigoNoise rain grounding instrument, and a Python Model Context Protocol (MCP) UI server.

Designed to help everyday AI users, sensory-sensitive knowledge workers, and multi-agent developers detect long-context control-token leakage (`<|im_start|>`, `<|im_end|>`, `[INST]`, `<<SYS>>`), arrest recursive echo loops, and maintain calm cognitive pacing—without subscriptions, cloud lock-in, or manipulative UI patterns.

---

## What's Inside

- **`mckenna/scanner.py` (`mckenna-scan` CLI)** — Pure Python standard-library (zero third-party dependencies) transcript auditor detecting leaked chat-template delimiters, unprompted self-query ("Layla"-class) attractor sinks, trigram repetition collapse, and sycophantic echo hazards. Exits with code `2` on `HIGH` risk for CI/pipeline gating.
- **`mckenna/wave_function.py`** — 64-mode complex Hilbert-space engine ($\psi \in \mathbb{C}^{64}$) enforcing the adaptive spectral entropy **Coherence Corridor** ($2.0 \le H_\psi \le 4.5$ bits) using unintrusive **IndigoNoise** $1/f$ pink-noise recovery by default (with optional `"brown_noise"` and `"uniform"` profiles for offline benchmarking).
- **`mckenna/stabilizer.py`** — 8×8 transition-matrix loop dampener featuring `apply_indigo_noise()` (a circular-distance $1/f^\alpha$ kernel sitting cleanly between rigid GABA damping and flat white-noise dissolution) plus the Mano Observer entropy diagnostic.
- **`mckenna/benchmark.py` (`mckenna-benchmark` CLI)** — Optional offline A/B benchmark script comparing `"pink_noise"`, `"brown_noise"`, and `"uniform"` corridor recovery across deterministic seeds (kept out of the UI so visual calm is never disrupted).
- **`mckenna/triadic_engine.py`** — Phase-sensitive Triadic Vector Engine comparing binary friction ($A \leftrightarrow B$) against Apex Node $C$ phase alignment.
- **`apps/mckenna-suite/index.html`** — Zero-dependency single-file browser dashboard with 1-click **IndigoNoise** procedural $1/f$ rain synthesis (standalone or layered with the 45 Hz grounding oscillator), ultra-subtle twilight indigo raindrop ripples, 50% Visual Damping toggle, and Plain Engineering ↔ Living Codex vocabulary switch. *(Focus and sensory pacing tool — not a medical device.)*
- **`apps/mckenna-suite/mcp_server.py`** — Python FastMCP server exposing `open_mckenna_dashboard`, `scan_transcript_coherence`, `run_triadic_delta_shift`, and the interactive UI resource (`ui://mckenna-suite/app.html`).
- **`docs/preprint-llm-entity-boundary-degradation.md`** — Publication-ready engineering preprint documenting teleological drift, role-boundary breakdown, narrative attractor sinks, and three concrete inference-stack mitigations.

---

## IndigoNoise ($1/f$) — Calm Broadband Masking & Offline Benchmark

Added in **v1.1.0**, **IndigoNoise** brings broadband $1/f$ pink-noise masking to both the math engine and the browser instrument with minimal interaction:

- **1-Click Procedural Rain Bed:** Uses Paul Kellet's 7-stage $1/f$ pink-noise filter blended with a warm Brownian rain floor, high-passed at 95 Hz (so the 45 Hz sub-bass grounding tone stays clear when layered), low-passed at 1450 Hz, with seamless crossfaded looping and a gentle 0.08 Hz breathing LFO.
- **Subtle Visual Pacing:** When active, the wave-function canvas renders an ultra-low-contrast twilight indigo wash and sparse concentric raindrop ripples (halved further when **Visual Damping** is enabled). On a `HIGH`-risk scanner detection, an active IndigoNoise bed gently swells to mask the spike without harsh flashing.
- **Why $1/f$ Pink Noise Is Default:** Running `mckenna-benchmark --trials 100 --seed 42` across collapsed low-entropy states shows $1/f$ pink noise achieves **100% corridor recovery** while preserving the highest share of structured low-frequency anchor energy (84.2% vs. 77.0% for uniform white noise):

| Profile | Trials | Corridor Pass Rate | Mean $H_\psi$ (bits) | Low-Freq Power (Modes 0–7) | Mean Phase Coherence |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `pink_noise` *(IndigoNoise default)* | 100 | 100.0% | 2.3261 | **84.2%** | 0.9920 |
| `brown_noise` | 100 | 100.0% | 3.4529 | 75.1% | 0.9861 |
| `uniform` | 100 | 100.0% | 2.6656 | 77.0% | 0.9931 |

And on the 8×8 DMN transition matrix (`mckenna/stabilizer.py`), `apply_indigo_noise()` sits directly in the balanced middle ground between tight GABA damping and full boundary dissolution:

| Operator | Mean Row Entropy (bits) | Mean Self-Loop Diagonal | Adjacent Neighbor Mass | Status |
| :--- | ---: | ---: | ---: | :--- |
| `baseline_habitual` | 1.1603 | 0.8250 | 5.0% | `STABLE (HABITUAL_BRAID)` |
| `gaba_dampener_10mg` | 0.7250 | 0.9041 | 2.7% | `CALM (DAMPED_HAMILTONIAN)` |
| `indigo_noise_1_over_f` | **1.8440** | **0.6666** | **12.4%** | `INDIGO (1/f_MASKED)` |
| `synesthesizer_0.85` | 2.9397 | 0.2300 | 22.0% | `LUCID (BOUNDARY_DISSOLUTION)` |

---

## Quick Start

### 1. Browser Dashboard (Zero Install)
Open the live demo at [https://zulandratronics.github.io/mckenna-coherence-suite/](https://zulandratronics.github.io/mckenna-coherence-suite/) or open `apps/mckenna-suite/index.html` locally in any modern browser. Everything runs 100% locally with zero telemetry.

### 2. Install Python Package, `mckenna-scan`, & `mckenna-benchmark`
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

# Run the optional offline IndigoNoise A/B corridor benchmark
mckenna-benchmark --trials 100 --seed 42
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
