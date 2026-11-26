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


@pytest.mark.parametrize("profile", ["pink_noise", "brown_noise", "uniform"])
def test_corridor_recovers_collapsed_low_entropy_state(profile):
    wf = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, seed=42)
    wf.psi = np.zeros(64, dtype=complex)
    wf.psi[0] = 1.0 + 0.0j
    assert wf.compute_entropy() < 0.01

    wf.enforce_coherence_corridor(profile=profile)
    h = wf.compute_entropy()
    assert 2.0 <= h <= 4.5
    assert np.isclose(np.linalg.norm(wf.psi), 1.0, atol=1e-6)


def test_default_pink_noise_recovery_preserves_low_frequency_tilt():
    wf_pink = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, seed=42)
    wf_uni = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, seed=42)
    for wf in (wf_pink, wf_uni):
        wf.psi = np.zeros(64, dtype=complex)
        wf.psi[0] = 1.0 + 0.0j

    wf_pink.enforce_coherence_corridor()  # default: pink_noise (IndigoNoise)
    wf_uni.enforce_coherence_corridor(profile="uniform")

    # Pink-noise recovery puts higher share of redistributed energy into low modes (1..15)
    # than flat white noise, avoiding harsh high-frequency scatter.
    pink_low_share = float(np.sum(wf_pink.power_spectrum()[1:16]))
    uni_low_share = float(np.sum(wf_uni.power_spectrum()[1:16]))
    assert pink_low_share > uni_low_share


def test_invalid_corridor_profile_raises():
    wf = WaveFunctionProcessor(num_modes=64, seed=42)
    with pytest.raises(ValueError, match="Unknown corridor profile"):
        wf.enforce_coherence_corridor(profile="neon_noise")


def test_dmn_gaba_dampener_reduces_dmn_power_and_preserves_norm():
    wf = WaveFunctionProcessor(num_modes=64, dmn_damping=0.85, seed=7)
    before_dmn = float(np.sum(wf.power_spectrum()[:4]))
    wf.apply_dmn_gaba_dampener()
    after_dmn = float(np.sum(wf.power_spectrum()[:4]))
    assert after_dmn < before_dmn * 0.1
    assert np.isclose(np.linalg.norm(wf.psi), 1.0, atol=1e-6)


@pytest.mark.parametrize("mode", ["45hz_sub_bass", "128bpm_phase_lock", "indigo_rain", "void_reset"])
def test_step_simulation_all_modes_stay_inside_corridor(mode):
    wf = WaveFunctionProcessor(num_modes=64, h_min=2.0, h_max=4.5, seed=123)
    metrics = wf.step_simulation(mode=mode)
    assert 2.0 <= metrics["entropy"] <= 4.5
    assert 0.0 <= metrics["coherence"] <= 1.0
    assert metrics["spectral_norm"] == pytest.approx(1.0, abs=1e-3)
    assert metrics["profile"] == "pink_noise"


def test_void_reset_aligns_all_phases():
    wf = WaveFunctionProcessor(num_modes=64, seed=1)
    wf.apply_sonic_modulation(mode="void_reset")
    assert wf.compute_coherence() == pytest.approx(1.0, abs=1e-6)
