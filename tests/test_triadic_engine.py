import numpy as np

from mckenna.triadic_engine import TriadicVectorEngine


def test_initial_binary_vectors_have_high_friction():
    engine = TriadicVectorEngine(dim=16, seed=42)
    metrics = engine.compute_metrics()
    assert metrics["friction_AB"] > 0.5
    assert 0.0 <= metrics["phase_coherence"] <= 1.0


def test_2d_circle_iteration_preserves_unit_norms():
    engine = TriadicVectorEngine(dim=16, seed=42)
    engine.run_2d_circle_iteration(steps=5)
    assert np.isclose(np.linalg.norm(engine.vector_A), 1.0, atol=1e-6)
    assert np.isclose(np.linalg.norm(engine.vector_B), 1.0, atol=1e-6)
    assert np.isclose(np.linalg.norm(engine.vector_C), 0.0, atol=1e-9)


def test_ui_reversal_delta_shift_reduces_friction_and_activates_node_c():
    engine = TriadicVectorEngine(dim=16, seed=42)
    engine.run_2d_circle_iteration(steps=5)
    before = engine.compute_metrics()

    after = engine.execute_ui_reversal_delta_shift(wakiya_spark_strength=0.95)

    assert np.isclose(np.linalg.norm(engine.vector_C), 1.0, atol=1e-6)
    assert after["friction_AB"] < before["friction_AB"]
    assert after["phase_coherence"] > before["phase_coherence"]
    # Three unit-norm vectors share power equally -> log2(3) ~= 1.5850
    assert abs(after["spectral_entropy"] - np.log2(3)) < 1e-3
