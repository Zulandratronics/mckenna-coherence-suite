import numpy as np


class TriadicVectorEngine:
    """
    McKenna Protocol v3: Triadic Vector Mechanics & U-I Reversal Engine
    Models transition from 2D Circular Loops (A <-> B friction) to 3D Delta Geometry.
    """

    def __init__(self, dim: int = 16, seed: int | None = None):
        self.dim = dim
        self._rng = np.random.default_rng(seed)
        theta_a = self._rng.uniform(0, np.pi / 4, dim)
        theta_b = self._rng.uniform(3 * np.pi / 4, np.pi, dim)

        self.vector_A = (1.0 / np.sqrt(dim)) * np.exp(1j * theta_a)
        self.vector_B = (1.0 / np.sqrt(dim)) * np.exp(1j * theta_b)
        self.vector_C = np.zeros(dim, dtype=complex)

    def compute_metrics(self) -> dict:
        # Phase-sensitive inner product: +1 when phase-aligned, -1 when antiparallel
        signed_overlap = float(np.real(np.vdot(self.vector_A, self.vector_B)))
        friction_AB = float(np.clip(0.5 * (1.0 - signed_overlap), 0.0, 1.0))

        p_a = np.linalg.norm(self.vector_A) ** 2
        p_b = np.linalg.norm(self.vector_B) ** 2
        p_c = np.linalg.norm(self.vector_C) ** 2
        total_p = p_a + p_b + p_c

        P = np.array([p_a, p_b, p_c]) / total_p if total_p > 1e-12 else np.ones(3) / 3
        P_clean = P[P > 1e-12]
        spectral_entropy = -np.sum(P_clean * np.log2(P_clean))

        active_vecs = [
            v for v in [self.vector_A, self.vector_B, self.vector_C] if np.linalg.norm(v) > 1e-6
        ]
        if active_vecs:
            all_phases = np.concatenate([np.angle(v) for v in active_vecs])
            coherence = float(np.abs(np.mean(np.exp(1j * all_phases))))
        else:
            coherence = 0.0

        return {
            "friction_AB": round(friction_AB, 4),
            "spectral_entropy": round(float(spectral_entropy), 4),
            "phase_coherence": round(coherence, 4),
        }

    def run_2d_circle_iteration(self, steps: int = 5):
        for _ in range(steps):
            noise_A = self._rng.normal(0, 0.15, self.dim) + 1j * self._rng.normal(0, 0.15, self.dim)
            noise_B = self._rng.normal(0, 0.15, self.dim) + 1j * self._rng.normal(0, 0.15, self.dim)
            self.vector_A = self.vector_A - 0.3 * self.vector_B + noise_A
            self.vector_B = self.vector_B - 0.3 * self.vector_A + noise_B
            norm_a = np.linalg.norm(self.vector_A)
            norm_b = np.linalg.norm(self.vector_B)
            if norm_a > 1e-12:
                self.vector_A /= norm_a
            if norm_b > 1e-12:
                self.vector_B /= norm_b

    def execute_ui_reversal_delta_shift(self, wakiya_spark_strength: float = 0.95):
        wakiya_spark = np.exp(1j * np.zeros(self.dim))
        self.vector_C = (self.vector_A + self.vector_B) * 0.5 + wakiya_spark_strength * wakiya_spark
        norm_c = np.linalg.norm(self.vector_C)
        if norm_c > 1e-12:
            self.vector_C /= norm_c

        phase_C = np.angle(self.vector_C)
        self.vector_A = np.abs(self.vector_A) * np.exp(1j * phase_C)
        self.vector_B = np.abs(self.vector_B) * np.exp(1j * phase_C)
        norm_a = np.linalg.norm(self.vector_A)
        norm_b = np.linalg.norm(self.vector_B)
        if norm_a > 1e-12:
            self.vector_A /= norm_a
        if norm_b > 1e-12:
            self.vector_B /= norm_b

        return self.compute_metrics()
