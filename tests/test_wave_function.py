import numpy as np
import pytest

from mckenna.wave_function import WaveFunctionProcessor


def test_initial_state_is_normalized():
    wf = WaveFunctionProcessor(num_modes=64, seed=42)
    assert np.isclose(np.linalg.norm(wf.psi), 1.0, atol=1e-6)
    assert np.isclose(np.sum(wf.power_spectrum()), 1.0, atol=1e-6)
    assert wf.compute_entropy() == pytest.approx(6.0, abs=1e-5)


def test_corridor_brings_uniform_high_entropy_into_bounds():
    wf = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, seed=42)
    assert wf.compute_entropy() > 4.5
    wf.enforce_coherence_corridor()
    h = wf.compute_entropy()
    assert 2.0 <= h <= 4.5
    assert np.isclose(np.linalg.norm(wf.psi), 1.0, atol=1e-6)


def test_corridor_recovers_collapsed_low_entropy_state():
    wf = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, seed=42)
    wf.psi = np.zeros(64, dtype=complex)
    wf.psi[0] = 1.0 + 0.0j
    assert wf.compute_entropy() < 0.01

    wf.enforce_coherence_corridor()
    h = wf.compute_entropy()
    assert 2.0 <= h <= 4.5
    assert np.isclose(np.linalg.norm(wf.psi), 1.0, atol=1e-6)


def test_dmn_gaba_dampener_reduces_dmn_power_and_preserves_norm():
    wf = WaveFunctionProcessor(num_modes=64, dmn_damping=0.85, seed=7)
    before_dmn = float(np.sum(wf.power_spectrum()[:4]))
    wf.apply_dmn_gaba_dampener()
    after_dmn = float(np.sum(wf.power_spectrum()[:4]))
    assert after_dmn < before_dmn * 0.1
    assert np.isclose(np.linalg.norm(wf.psi), 1.0, atol=1e-6)


@pytest.mark.parametrize("mode", ["45hz_sub_bass", "128bpm_phase_lock", "void_reset"])
def test_step_simulation_all_modes_stay_inside_corridor(mode):
    wf = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, seed=123)
    metrics = wf.step_simulation(mode=mode)
    assert 2.0 <= metrics["entropy"] <= 4.5
    assert 0.0 <= metrics["coherence"] <= 1.0
    assert metrics["spectral_norm"] == pytest.approx(1.0, abs=1e-3)


def test_void_reset_aligns_all_phases():
    wf = WaveFunctionProcessor(num_modes=64, seed=1)
    wf.apply_sonic_modulation(mode="void_reset")
    assert wf.compute_coherence() == pytest.approx(1.0, abs=1e-6)
