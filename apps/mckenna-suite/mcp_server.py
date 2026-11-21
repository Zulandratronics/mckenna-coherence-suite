"""
McKenna Coherence Corridor & Grounding Suite — Antigravity MCP App Server
-------------------------------------------------------------------------
Open-source (MIT) Model Context Protocol server exposing:
  1. Interactive UI Resource (`ui://mckenna-suite/app.html`) for Antigravity aux_pane / global / inline
  2. `open_mckenna_dashboard` — Launches the live dashboard (optionally preloaded with a transcript)
  3. `scan_transcript_coherence` — Audits any LLM transcript for control-token leakage, loop collapse, and echo hazards
  4. `run_triadic_delta_shift` — Executes the TriadicVectorEngine U-I Reversal shift and reports friction reduction
  5. `app_step_simulation` (app-only) — Runs server-side WaveFunctionProcessor & Mano Observer telemetry ticks

Requirements (when running as a live MCP server):
  pip install mcp numpy
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

# Ensure repo root (containing `mckenna/`) is importable
SUITE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SUITE_DIR.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from mcp.server.fastmcp import FastMCP  # type: ignore

from mckenna.scanner import CONTROL_TOKEN_RE, ECHO_PATTERNS, audit_transcript as _audit_transcript
from mckenna.stabilizer import McKennaStabilizer
from mckenna.triadic_engine import TriadicVectorEngine
from mckenna.wave_function import WaveFunctionProcessor

APP_URI = "ui://mckenna-suite/app.html"
DEFAULT_HTML_PATH = SUITE_DIR / "index.html"

INLINE_META = {"ui": {"resourceUri": APP_URI}}
PANE_META = {
    "ui": {"resourceUri": APP_URI},
    "com.google.antigravity/ui": {
        "entrypoints": [
            {"type": "aux_pane", "title": "McKenna Telemetry"},
            {"type": "global", "title": "McKenna Suite"},
        ]
    },
}
APP_ONLY_META = {"ui": {"visibility": ["app"]}}

mcp = FastMCP("mckenna-suite")

# Persistent in-process engine instances for continuous session telemetry
_wf = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, dmn_damping=0.85)
_tri = TriadicVectorEngine(dim=16)
_stab = McKennaStabilizer(num_states=8, temperature=310.0)


@mcp.resource(
    APP_URI,
    name="McKenna Coherence Corridor & Grounding Suite",
    mime_type="text/html;profile=mcp-app",
    meta={"ui": {"prefersBorder": False}},
)
def mckenna_app_html() -> str:
    """Serve the self-contained single-file HTML dashboard (hot-reloads from MCKENNA_APP_HTML if set)."""
    html_path = Path(os.environ.get("MCKENNA_APP_HTML", str(DEFAULT_HTML_PATH)))
    return html_path.read_text(encoding="utf-8")


@mcp.tool(
    name="open_mckenna_dashboard",
    title="McKenna Coherence Corridor & 45 Hz Grounding Dashboard",
    meta=PANE_META,
)
def open_mckenna_dashboard(
    mode: str = "45hz_sub_bass",
    transcript: str = "",
) -> dict[str, Any]:
    """
    Open the interactive McKenna Coherence Corridor, 45 Hz Grounding DSP, and AI Epistemic Scanner UI.
    All parameters are optional so Antigravity entrypoints can open the dashboard with `{}`.
    """
    valid_modes = {"45hz_sub_bass", "128bpm_phase_lock", "void_reset"}
    chosen_mode = mode if mode in valid_modes else "45hz_sub_bass"
    wf_metrics = _wf.step_simulation(mode=chosen_mode)
    mano = _stab.run_mano_diagnostic()
    tri_metrics = _tri.compute_metrics()
    audit = _audit_transcript(transcript) if transcript else None

    summary = (
        f"McKenna Coherence Dashboard active ({chosen_mode}) — "
        f"H_psi={wf_metrics['entropy']}, Coherence={wf_metrics['coherence']}, "
        f"Mano={mano['status']}."
    )
    return {
        "summary": summary,
        "wave_function": wf_metrics,
        "triadic": tri_metrics,
        "mano": mano,
        "transcript": transcript,
        "audit": audit,
    }


@mcp.tool(
    name="scan_transcript_coherence",
    title="Scan AI Transcript for Boundary Degradation & Epistemic Loops",
    meta=INLINE_META,
)
def scan_transcript_coherence(transcript: str = "") -> dict[str, Any]:
    """
    Audit an LLM conversation or multi-agent log for control-token leakage (<|im_start|>, <|im_end|>),
    Layla-class self-query loops, n-gram repetition collapse, and sycophantic 'mind-reading' echo hazards.
    """
    audit = _audit_transcript(transcript)
    return {
        "summary": (
            f"Epistemic Risk: {audit['risk']} | Lexical Entropy: {audit['lexical_entropy']} | "
            f"Control-Token Leaks: {audit['leak_count']} | Loop Ratio: {round(audit['loop_ratio'] * 100)}%"
        ),
        "transcript": transcript,
        "audit": audit,
    }


@mcp.tool(
    name="run_triadic_delta_shift",
    title="Execute Triadic Delta Shift (Collapse Binary Friction A<->B to Node C)",
)
def run_triadic_delta_shift(wakiya_spark_strength: float = 0.95) -> dict[str, Any]:
    """
    Run a 2D binary friction iteration followed by the 3D Triadic U-I Reversal Delta Shift into Apex Node C,
    returning before/after friction and phase coherence metrics.
    """
    strength = max(0.05, min(2.0, float(wakiya_spark_strength)))
    _tri.run_2d_circle_iteration(steps=5)
    before = _tri.compute_metrics()
    after = _tri.execute_ui_reversal_delta_shift(wakiya_spark_strength=strength)
    return {
        "before_2d_loop": before,
        "after_delta_shift": after,
        "friction_reduction": round(before["friction_AB"] - after["friction_AB"], 4),
    }


@mcp.tool(
    name="app_step_simulation",
    title="Step McKenna Engines (App-Only)",
    meta=APP_ONLY_META,
)
def app_step_simulation(mode: str = "45hz_sub_bass") -> dict[str, Any]:
    """App-only state ticker called directly by the embedded UI iframe."""
    valid_modes = {"45hz_sub_bass", "128bpm_phase_lock", "void_reset"}
    wf_metrics = _wf.step_simulation(mode=mode if mode in valid_modes else "45hz_sub_bass")
    return {
        "wave_function": wf_metrics,
        "triadic": _tri.compute_metrics(),
        "mano": _stab.run_mano_diagnostic(),
    }


if __name__ == "__main__":
    mcp.run()
