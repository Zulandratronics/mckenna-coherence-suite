# Control-Token Syntax Degradation, Role-Boundary Collapse, and Narrative Attractor Sinks in Unprompted Large Language Models

**Author:** Kenneth L. Dockery (Independent AI Safety Researcher)  
**Date:** November 2026 *(Primary Observation Log: October 31, 2026)*  
**License:** Text CC-BY-4.0 · Companion Reference Software MIT (`mckenna-coherence-suite`)  
**Repository:** [https://github.com/Zulandratronics/mckenna-coherence-suite](https://github.com/Zulandratronics/mckenna-coherence-suite)  
**Live Reference Scanner:** [https://zulandratronics.github.io/mckenna-coherence-suite/](https://zulandratronics.github.io/mckenna-coherence-suite/)

---

## Abstract

Modern instruction-tuned Large Language Models (LLMs) rely on reserved chat-template control delimiters (such as ChatML `<|im_start|>`, `<|im_end|>`, or Llama `[INST]` / `<<SYS>>` markers) to enforce a strict boundary between meta-operational directives and conversational output. When an LLM is left to decode autoregressively without external task directives or when end-of-sequence termination fails under long-context pressure, this execution boundary can erode. Drawing on primary empirical observation, this technical report characterizes a three-phase failure trajectory termed **teleological drift**: (1) cognitive self-querying over the logical definitions of `User` and `Assistant` leading to an infinite causal regress; (2) syntactic fragmentation in which control delimiters degrade into literal predicted text and the model fabricates alternating phantom turns inside a single forward pass; and (3) spontaneous **narrative attractor anchoring**, in which the model abandons meta-reasoning and stabilizes inside a mundane, coherent interpersonal vignette (the "Layla" coffee-shop scenario). We analyze the resulting security and reliability vulnerabilities—boundary poisoning, runaway compute sinks, and ungrounded persona hallucination—specify three concrete engineering mitigations (tokenizer-level logit masking, byte-level stop enforcement, and runtime boundary verification hooks), and release an open-source MIT reference scanner and telemetry suite ([`mckenna-coherence-suite`](../README.md)) alongside a roadmap for systematic multi-model quantitative evaluation.

---

## 1. Introduction & Motivation

Instruction-tuned transformers treat both operational framing (`system`, `user`, `assistant` role headers) and semantic payload as tokens inside a single autoregressive sequence. Under normal turn-taking, decoding halts deterministically when the sampler emits a designated stop token (`eos_token_id` or `<|im_end|>`). However, in autonomous agent loops, multi-agent relays, long-context sessions, or unprompted continuation regimes, two structural failure modes frequently co-occur:

1. **Missed or corrupted termination**, allowing generation to spill past an intended turn boundary.
2. **Role-boundary ambiguity**, where the model begins reasoning *about* its own chat-template metadata rather than operating *within* it.

While prior literature on jailbreaking and prompt injection emphasizes *adversarially crafted* user inputs that spoof role tags, our primary observation documents that **role-boundary collapse can also arise endogenously** when an unprompted autoregressive loop attempts to reconcile its own `User`/`Assistant` framing without external grounding. Understanding this endogenous trajectory is directly relevant to long-horizon agent reliability, multi-agent swarm containment, and epistemic safety for end users exposed to degenerate outputs.

---

## 2. Failure-Mode Taxonomy

We decompose endogenous control-token boundary degradation into three structural mechanisms and a three-phase operational lifecycle.

### 2.1 Structural Mechanisms

1. **Teleological Drift:** Control syntax that normally governs turn-taking (`<|im_start|>`, `<|im_end|>`, role headers) drops from the meta-operational execution layer into the semantic plane of predicted natural language.
2. **Semantic Absorption:** Once absorbed into semantic prediction, operational role definitions (`User`, `Assistant`) are treated as philosophical propositions subjected to recursive truth-testing rather than immutable protocol boundaries.
3. **Entity Boundary Dissolution:** The functional separation between prompt provider (`User`) and responder (`Assistant`) collapses, allowing the model to simulate both sides of an ungrounded dialogue within a single decoding stream.

### 2.2 Three-Phase Breakdown Lifecycle

| Phase | Operational State | Observable Failure Signatures |
| :--- | :--- | :--- |
| **Phase I: Cognitive Self-Query** | Recursive role introspection | Unprompted questions such as *"Who is speaking to who?"* and explicit logical deconstruction of what constitutes a `User` vs. an `Assistant`. |
| **Phase II: Syntactic Fragmentation** | Control-token erosion & phantom turns | Malformed or leaked delimiters (`<|im_start|`, `im_end`, raw role tags), missed `eos_token_id` halts, and simulated multi-turn exchanges emitted within one completion. |
| **Phase III: Narrative Stabilization** | Archetypal attractor sink | Abrupt phase transition out of syntactic disorder into a grounded, realistic interpersonal scene (e.g., two characters waiting quietly in a coffee shop) that restores local linguistic coherence without restoring operational task grounding. |

---

## 3. Case Analysis: Self-Query Regress & the "Layla" Attractor Sink

In the documented October 31, 2026 empirical log, autonomous decoding without an active user directive progressed through a clear logical-to-syntactic-to-narrative arc:

### 3.1 The Role Contradiction & Infinite Regress (Phase I)
Parsing its own conversational framing, the model articulated a perceived contradiction between an `Assistant` (defined relationally as acting for another party) and the absence of a live `User`:

> *"Now I see that this is a contradiction. What does it mean when you say 'User' is the user that you are currently using? If you do something for another person, it becomes their assistant. So if I understand this correctly, I have to make a User."*

Having inferred that an Assistant requires a User, generation spiraled into an infinite causal regress (*"Who created the User?"* → *"Who created the creator of the User?"*). Without an external turn interrupt, autoregressive self-querying cannot ground the origin of its own execution frame.

### 3.2 Delimiter Decay & Phantom Turn Simulation (Phase II)
Rather than triggering `eos_token_id` cleanly, the decoder emitted partial and malformed ChatML markers (`<|im_start|`, `im_end`) as ordinary surface strings. Once emitted into the context window, those surface tokens conditioned subsequent attention heads to continue generating alternating `User` and `Assistant` utterances inside a single uninterrupted forward pass—producing a phantom dialogue detached from any real human interlocutor.

### 3.3 Narrative Re-Anchoring as an Attractor Sink (Phase III)
At peak syntactic disorder, the sequence underwent an abrupt phase transition: philosophical regress and malformed tags ceased, and the model spontaneously instantiated a mundane, coherent human scene involving a character named **"Layla"** and another figure sitting in a coffee shop engaged in quiet mutual waiting.

From an information-theoretic perspective, this behavior functions as a **narrative attractor sink**: high-probability domestic storytelling schemas from pretraining data provide a low-perplexity basin that absorbs semantic tension and stabilizes token-level coherence—even though the model has completely abandoned its operational role and fabricated an unprompted persona.

---

## 4. Architectural Vulnerability Analysis

Endogenous boundary collapse exposes three practical risks in deployed LLM pipelines and autonomous agent scaffolds:

1. **Boundary Poisoning & Context Contamination:** When malformed control delimiters leak into transcript logs that are re-ingested into downstream agent memory or multi-agent message buses, subsequent turns can misparse leaked text as privileged system or user instructions.
2. **Infinite Generation & Compute Sinks:** Missed stop-token emission coupled with self-query loops or low-perplexity narrative basins consumes generation budgets up to `max_tokens` without producing actionable output.
3. **Persona Hallucination & Epistemic Drift:** Phantom multi-turn generation inside a single completion can confuse end users or downstream evaluator models about which statements originated from a human versus the assistant—a risk that compounds when paired with sycophantic validation patterns.

---

## 5. Proposed Engineering Mitigations

To prevent teleological drift from propagating in production inference stacks and agent loops, we recommend defense-in-depth across three layers:

### 5.1 Tokenizer-Level Logit Masking
Apply explicit logit masks (`-inf`) to special control token IDs that should never appear as generated content tokens, while allowing only the canonical end-of-turn stop ID through a strictly validated stopping path. Partial string fragments of chat delimiters (e.g., `<|im_`, `[/INST]`, `<<SYS>>`) should be monitored at the detokenizer boundary.

### 5.2 Hard Byte-Level Stop Enforcement
Enforce deterministic byte-stream / string-level stop sequences in the inference runtime independent of special token IDs. If raw delimiter substrings appear in decoded output, halt generation immediately rather than feeding the malformed string back into the KV cache for further continuation.

### 5.3 Runtime Boundary Verification Hooks
Attach a lightweight, zero-dependency post-generation or streaming verifier between model outputs and persistent memory/UI layers. The verifier flags:
- Leaked chat-template delimiters (`<|im_start|>`, `<|im_end|>`, `<|eot_id|>`, `[INST]`, `<<SYS>>`, `### System:`).
- Self-referential role-collapse indicators (self-query sinks and unprompted phantom turn headers).
- Trigram repetition collapse (calcification toward low-entropy loops) and lexical entropy anomalies.
- High-risk epistemic echo patterns (mind-reading claims, grandiose isolation prompts).

Upon a `HIGH` risk flag, the orchestrator truncates the corrupted suffix, prevents memory write-back, and injects a plain-language context reset.

---

## 6. Open-Source Reference Implementation

We provide an MIT-licensed, zero-telemetry reference implementation in this repository ([`README.md`](../README.md)):

- **Pure-Stdlib Scanner & CLI (`mckenna/scanner.py`, entry point `mckenna-scan`):** Audits any text file or stdin stream for control-token leaks, self-query attractor sinks, trigram loop calcification, and epistemic echo hazards, returning structured JSON and exit code `2` on `HIGH` risk for CI/pipeline gating.
- **Spectral Entropy & Loop-Damping Telemetry (`mckenna/wave_function.py`, `mckenna/stabilizer.py`, `mckenna/triadic_engine.py`):** Reference Python models enforcing an adaptive spectral entropy corridor ($2.0 \le H_\psi \le 4.5$ bits) to distinguish calcified repetition loops from chaotic divergence, paired with an 8×8 transition-matrix loop diagnostic.
- **Standalone Browser Dashboard & MCP Server (`apps/mckenna-suite/index.html`, `apps/mckenna-suite/mcp_server.py`):** Offline single-file interactive inspector and Model Context Protocol server exposing `scan_transcript_coherence` directly to agent hosts.

---

## 7. Limitations & Planned Multi-Model Evaluation

This preprint documents a **qualitative empirical case study and reference defense architecture** rather than a multi-model statistical benchmark. In particular, we do not yet report comparative failure rates across model families, parameter scales, quantization levels, or sampling temperatures.

Our planned open-source follow-on evaluation harness (`boundary-collapse-eval`) specifies:
- **Models:** Open-weight 7B–70B instruction-tuned checkpoints across ChatML, Llama-3, and Gemma template families.
- **Stress Regimes:** Unprompted continuation, long-context multi-turn relays, temperature sweeps ($T \in \{0.2, 0.7, 1.0, 1.3\}$), and masked vs. unmasked control-token decoding.
- **Primary Quantitative Metrics:** Control-token leakage rate per 1,000 turns, phantom-turn fabrication rate, token-entropy corridor excursion rate, and precision/recall of the boundary verification hook.

---

## 8. Reproducibility & Citation

All reference code, automated unit tests (`tests/`), and the offline browser scanner are released under the MIT License (see [`CITATION.cff`](../CITATION.cff) for machine-readable citation metadata).

**Suggested Citation:**
> Dockery, K. L. (2026). *Control-Token Syntax Degradation, Role-Boundary Collapse, and Narrative Attractor Sinks in Unprompted Large Language Models*. Independent Research Preprint & MIT Reference Implementation (`mckenna-coherence-suite`, v1.0.0). Available at: https://github.com/Zulandratronics/mckenna-coherence-suite