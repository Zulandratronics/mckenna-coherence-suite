import numpy as np

from mckenna.stabilizer import McKennaStabilizer


def test_initial_dmn_matrix_is_row_stochastic():
    stab = McKennaStabilizer(num_states=8)
    row_sums = stab.active_matrix.sum(axis=1)
    assert np.allclose(row_sums, 1.0, atol=1e-9)
    assert stab.system_status == "STABLE (HABITUAL_BRAID)"


def test_gaba_dampener_preserves_stochasticity_and_lowers_entropy():
    stab = McKennaStabilizer(num_states=8)
    before = stab.run_mano_diagnostic(threshold=0.0)["entropy"]

    stab.apply_gaba_dampener(dose_mg=20.0)
    assert np.allclose(stab.active_matrix.sum(axis=1), 1.0, atol=1e-9)
    assert stab.system_status == "CALM (DAMPED_HAMILTONIAN)"

    after = stab.run_mano_diagnostic(threshold=0.0)["entropy"]
    assert after < before


def test_indigo_noise_loosens_habitual_loops_while_preserving_local_structure():
    stab = McKennaStabilizer(num_states=8)
    before_diag = float(np.mean(np.diag(stab.active_matrix)))
    before_entropy = stab.run_mano_diagnostic(threshold=0.0)["entropy"]

    stab.apply_indigo_noise(blend=0.35, alpha=1.0)
    after_diag = float(np.mean(np.diag(stab.active_matrix)))
    after_entropy = stab.run_mano_diagnostic(threshold=0.0)["entropy"]

    assert np.allclose(stab.active_matrix.sum(axis=1), 1.0, atol=1e-9)
    assert stab.system_status == "INDIGO (1/f_MASKED)"
    assert after_diag < before_diag
    assert after_entropy > before_entropy
    # Local 1/f structure: adjacent neighbor (d=1) stays stronger than opposite state (d=4)
    assert stab.active_matrix[0, 1] > stab.active_matrix[0, 4]


def test_synesthesizer_dissolves_habitual_diagonal():
    stab = McKennaStabilizer(num_states=8)
    before_diag = float(np.mean(np.diag(stab.active_matrix)))
    stab.apply_synesthesizer(saturation=0.85)
    after_diag = float(np.mean(np.diag(stab.active_matrix)))

    assert after_diag < before_diag
    assert np.allclose(stab.active_matrix.sum(axis=1), 1.0, atol=1e-9)
    assert stab.system_status == "LUCID (BOUNDARY_DISSOLUTION)"


def test_mano_diagnostic_triggers_collapse_below_threshold():
    stab = McKennaStabilizer(num_states=8)
    stab.apply_gaba_dampener(dose_mg=25.0)

    report = stab.run_mano_diagnostic(threshold=0.95)
    assert report["status"] == "COLLAPSE_TRIGGERED"
    assert stab.system_status == "RECALIBRATED (COHERENT)"
    assert np.allclose(stab.active_matrix, stab.dmn_matrix)


def test_mano_diagnostic_respects_custom_threshold():
    stab = McKennaStabilizer(num_states=8)
    # Baseline 8-state habitual matrix has row entropy ~1.16 bits
    res_low = stab.run_mano_diagnostic(threshold=0.95)
    assert res_low["status"] == "RESONANT"

    res_high = stab.run_mano_diagnostic(threshold=2.0)
    assert res_high["status"] == "COLLAPSE_TRIGGERED"
