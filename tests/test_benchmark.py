"""Unit tests for the optional IndigoNoise offline A/B benchmark."""

from __future__ import annotations

import json
from io import StringIO
from unittest.mock import patch

from mckenna.benchmark import (
    benchmark_corridor_profiles,
    benchmark_stabilizer_operators,
    format_markdown_benchmark,
    main,
)


def test_corridor_benchmark_profiles_all_recover_and_pink_preserves_low_freq_tilt():
    results = {r.profile: r for r in benchmark_corridor_profiles(trials=20, seed=42)}
    assert set(results.keys()) == {"pink_noise", "brown_noise", "uniform"}

    for r in results.values():
        assert r.corridor_pass_rate == 1.0
        assert 2.0 <= r.mean_entropy <= 4.5

    assert results["pink_noise"].mean_low_freq_share > results["uniform"].mean_low_freq_share


def test_stabilizer_benchmark_places_indigo_noise_between_gaba_and_synesthesizer():
    ops = {s.operator: s for s in benchmark_stabilizer_operators()}
    assert ops["gaba_dampener_10mg"].mean_row_entropy < ops["indigo_noise_1_over_f"].mean_row_entropy
    assert ops["indigo_noise_1_over_f"].mean_row_entropy < ops["synesthesizer_0.85"].mean_row_entropy
    assert ops["indigo_noise_1_over_f"].status == "INDIGO (1/f_MASKED)"


def test_benchmark_cli_markdown_and_json():
    corridor = benchmark_corridor_profiles(trials=5, seed=7)
    stabilizer = benchmark_stabilizer_operators()
    md = format_markdown_benchmark(corridor, stabilizer)
    assert "IndigoNoise Offline Corridor Recovery Benchmark" in md
    assert "`pink_noise`" in md

    with patch("sys.stdout", new_callable=StringIO) as out:
        code = main(["--trials", "5", "--seed", "7", "--json"])
        assert code == 0
        payload = json.loads(out.getvalue())
        assert len(payload["corridor_profiles"]) == 3
        assert len(payload["stabilizer_operators"]) == 4
