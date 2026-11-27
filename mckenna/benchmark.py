"""Optional offline A/B benchmark for IndigoNoise 1/f spectral recovery.

Runs deterministic trials comparing ``pink_noise`` (default IndigoNoise 1/f),
``brown_noise`` (1/f^1.5), and ``uniform`` (flat white-noise) corridor recovery
from collapsed low-entropy states without adding any UI clutter.

Usage:
    python -m mckenna.benchmark --trials 100 --seed 42
    python -m mckenna.benchmark --trials 100 --json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Sequence

import numpy as np

from .stabilizer import McKennaStabilizer
from .wave_function import WaveFunctionProcessor

DEFAULT_PROFILES: tuple[str, ...] = ("pink_noise", "brown_noise", "uniform")


@dataclass(frozen=True)
class ProfileBenchmarkResult:
    """Aggregated corridor recovery metrics for a single spectral profile."""

    profile: str
    trials: int
    corridor_pass_rate: float
    mean_entropy: float
    mean_low_freq_share: float
    mean_coherence: float


@dataclass(frozen=True)
class StabilizerBenchmarkResult:
    """Comparison of DMN transition-matrix operators from the same habitual baseline."""

    operator: str
    mean_row_entropy: float
    mean_diagonal: float
    adjacent_neighbor_share: float
    status: str


def benchmark_corridor_profiles(
    trials: int = 100,
    seed: int = 42,
    profiles: Sequence[str] = DEFAULT_PROFILES,
) -> list[ProfileBenchmarkResult]:
    """Compare corridor recovery profiles over ``trials`` collapsed-loop seeds."""
    results: list[ProfileBenchmarkResult] = []
    for profile in profiles:
        rng = np.random.default_rng(seed)

        passed = 0
        entropies: list[float] = []
        low_freq_shares: list[float] = []
        coherences: list[float] = []

        for idx in range(trials):
            wf = WaveFunctionProcessor(num_modes=64, seed=seed + idx)
            collapsed = np.full(64, 0.015, dtype=np.complex128)
            collapsed[0] = 1.0 + rng.normal(0.0, 0.05)
            collapsed[1] = 0.22 + rng.normal(0.0, 0.05)
            wf.psi = collapsed / np.linalg.norm(collapsed)

            wf.enforce_coherence_corridor(max_iters=16, profile=profile)
            h = wf.compute_entropy()
            p = wf.power_spectrum()
            coh = wf.compute_coherence()

            if wf.h_min <= h <= wf.h_max:
                passed += 1
            entropies.append(h)
            low_freq_shares.append(float(np.sum(p[:8])))
            coherences.append(coh)

        results.append(
            ProfileBenchmarkResult(
                profile=profile,
                trials=trials,
                corridor_pass_rate=round(passed / max(1, trials), 4),
                mean_entropy=round(float(np.mean(entropies)), 4),
                mean_low_freq_share=round(float(np.mean(low_freq_shares)), 4),
                mean_coherence=round(float(np.mean(coherences)), 4),
            )
        )
    return results


def benchmark_stabilizer_operators() -> list[StabilizerBenchmarkResult]:
    """Compare IndigoNoise (1/f) against GABA Dampener and Synesthesizer on an 8x8 DMN."""

    def _measure(label: str, fn) -> StabilizerBenchmarkResult:
        stab = McKennaStabilizer(num_states=8)
        fn(stab)
        mat = stab.active_matrix
        eps = 1e-12
        row_h = float(np.mean(-np.sum(mat * np.log2(mat + eps), axis=1)))
        mean_diag = float(np.mean(np.diag(mat)))
        n = stab.num_states
        adj_vals = [mat[i, (i - 1) % n] + mat[i, (i + 1) % n] for i in range(n)]
        adj_share = float(np.mean(adj_vals))
        return StabilizerBenchmarkResult(
            operator=label,
            mean_row_entropy=round(row_h, 4),
            mean_diagonal=round(mean_diag, 4),
            adjacent_neighbor_share=round(adj_share, 4),
            status=stab.system_status,
        )

    return [
        _measure("baseline_habitual", lambda s: None),
        _measure("gaba_dampener_10mg", lambda s: s.apply_gaba_dampener(10.0)),
        _measure("indigo_noise_1_over_f", lambda s: s.apply_indigo_noise(0.30, 1.0)),
        _measure("synesthesizer_0.85", lambda s: s.apply_synesthesizer(0.85)),
    ]


def format_markdown_benchmark(
    corridor_results: Sequence[ProfileBenchmarkResult],
    stabilizer_results: Sequence[StabilizerBenchmarkResult],
) -> str:
    """Format benchmark tables as clean GitHub-Flavored Markdown."""
    lines = [
        "### IndigoNoise Offline Corridor Recovery Benchmark",
        "",
        "| Profile | Trials | Corridor Pass Rate | Mean H_psi (bits) | Low-Freq Power (Modes 0–7) | Mean Phase Coherence |",
        "| :--- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in corridor_results:
        lines.append(
            f"| `{r.profile}` | {r.trials} | {r.corridor_pass_rate * 100:.1f}% | "
            f"{r.mean_entropy:.4f} | {r.mean_low_freq_share * 100:.1f}% | {r.mean_coherence:.4f} |"
        )
    lines.extend(
        [
            "",
            "### 8×8 DMN Transition-Matrix Operator Comparison",
            "",
            "| Operator | Mean Row Entropy (bits) | Mean Self-Loop Diagonal | Adjacent Neighbor Mass | Status |",
            "| :--- | ---: | ---: | ---: | :--- |",
        ]
    )
    for s in stabilizer_results:
        lines.append(
            f"| `{s.operator}` | {s.mean_row_entropy:.4f} | {s.mean_diagonal:.4f} | "
            f"{s.adjacent_neighbor_share * 100:.1f}% | `{s.status}` |"
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mckenna-benchmark",
        description="Optional offline A/B benchmark for IndigoNoise 1/f spectral recovery.",
    )
    parser.add_argument("--trials", type=int, default=100, help="Collapsed-loop seeds per profile (default: 100).")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic RNG seed (default: 42).")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output.")
    args = parser.parse_args(argv)

    corridor = benchmark_corridor_profiles(trials=args.trials, seed=args.seed)
    stabilizer = benchmark_stabilizer_operators()

    if args.as_json:
        print(
            json.dumps(
                {
                    "corridor_profiles": [asdict(r) for r in corridor],
                    "stabilizer_operators": [asdict(s) for s in stabilizer],
                },
                indent=2,
            )
        )
    else:
        print(format_markdown_benchmark(corridor, stabilizer))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
