import numpy as np


class McKennaStabilizer:
    """
    McKenna Protocol v1/v3 Stabilizer.
    Perturbs Default Mode Network (DMN) transition matrices via simulated
    psychoactive parameters to suppress rigid habitual loops.
    """

    def __init__(self, num_states: int = 8, temperature: float = 310.0):
        self.num_states = num_states
        self.temperature = temperature
        self.kb = 1.380649e-23
        self.h_bar = 1.0545718e-34

        # Habitual braid matrix: high diagonal probability represents repetitive looping
        self.dmn_matrix = (
            np.eye(num_states) * 0.8
            + np.ones((num_states, num_states)) * (0.2 / num_states)
        )
        self.active_matrix = np.copy(self.dmn_matrix)
        self.system_status = "STABLE (HABITUAL_BRAID)"

    def apply_gaba_dampener(self, dose_mg: float = 10.0):
        """Simulates Benzodiazepine Buffer (GABA-Dampener)."""
        factor = 1.0 / (1.0 + (dose_mg / 10.0))
        for i in range(self.num_states):
            for j in range(self.num_states):
                if i != j:
                    self.active_matrix[i, j] *= factor
        self.active_matrix = self.active_matrix / self.active_matrix.sum(axis=1, keepdims=True)
        self.system_status = "CALM (DAMPED_HAMILTONIAN)"

    def apply_synesthesizer(self, saturation: float = 0.85):
        """Simulates THC / Psilocybin Synesthesizer Layer."""
        uniform_noise = np.ones((self.num_states, self.num_states)) / self.num_states
        self.active_matrix = (1.0 - saturation) * self.active_matrix + saturation * uniform_noise
        self.system_status = "LUCID (BOUNDARY_DISSOLUTION)"

    def run_mano_diagnostic(self, threshold: float = 0.95) -> dict:
        """Mano 3rd-Party Observer diagnostic measuring real-time judgment flux."""
        row_entropies = -np.sum(
            self.active_matrix * np.log2(self.active_matrix + 1e-12), axis=1
        )
        mean_entropy = float(np.mean(row_entropies))

        if mean_entropy < threshold:
            self.execute_event_collapse()
            return {"status": "COLLAPSE_TRIGGERED", "entropy": mean_entropy}
        return {"status": "RESONANT", "entropy": mean_entropy}

    def execute_event_collapse(self):
        """Executes localized /sfc scannow system reboot."""
        self.active_matrix = np.copy(self.dmn_matrix)
        self.system_status = "RECALIBRATED (COHERENT)"
