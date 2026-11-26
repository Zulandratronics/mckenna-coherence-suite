import numpy as np


class WaveFunctionProcessor:
    """
    McKenna Protocol v1/v3: Wave-Function Processing Engine
    Simulates complex-valued cognitive state vector dynamics in Hilbert space,
    phase coherence, adaptive entropy bounds (Coherence Corridor), and sonic operators.
    """

    def __init__(
        self,
        num_modes: int = 64,
        h_min: float = 2.0,
        h_max: float = 4.5,
        dmn_damping: float = 0.85,
        seed: int | None = None,
    ):
        self.num_modes = num_modes
        self.h_min = h_min
        self.h_max = h_max
        self.dmn_damping = dmn_damping
        self._rng = np.random.default_rng(seed)

        angles = self._rng.uniform(0, 2 * np.pi, num_modes)
        self.psi = (1.0 / np.sqrt(num_modes)) * np.exp(1j * angles)

    def power_spectrum(self) -> np.ndarray:
        mags_sq = np.abs(self.psi) ** 2
        total_power = np.sum(mags_sq)
        if total_power < 1e-12:
            return np.ones(self.num_modes) / self.num_modes
        return mags_sq / total_power

    def compute_entropy(self) -> float:
        P = self.power_spectrum()
        P_clean = P[P > 1e-12]
        return float(-np.sum(P_clean * np.log2(P_clean)))

    def compute_coherence(self) -> float:
        phases = np.angle(self.psi)
        mean_vector = np.mean(np.exp(1j * phases))
        return float(np.abs(mean_vector))

    def _spectral_profile_magnitudes(self, profile: str = "pink_noise") -> np.ndarray:
        """
        Return a unit-norm magnitude envelope for low-entropy corridor recovery:
          - 'pink_noise' (default / IndigoNoise): 1/f power spectrum (|w_k| ~ (k+1)^-0.5)
          - 'brown_noise': warmer low-frequency rolloff (|w_k| ~ (k+2)^-0.75)
          - 'uniform': flat white-noise spectrum (optional baseline for A/B testing)
        """
        k = np.arange(self.num_modes, dtype=float)
        if profile == "pink_noise":
            w = 1.0 / np.sqrt(k + 1.0)
        elif profile == "brown_noise":
            w = 1.0 / ((k + 2.0) ** 0.75)
        elif profile == "uniform":
            w = np.ones(self.num_modes, dtype=float)
        else:
            raise ValueError(
                f"Unknown corridor profile '{profile}'. Expected 'pink_noise', 'brown_noise', or 'uniform'."
            )
        return w / np.linalg.norm(w)

    def apply_dmn_gaba_dampener(self, dmn_indices=None):
        if dmn_indices is None:
            dmn_indices = [0, 1, 2, 3]
        for idx in dmn_indices:
            if 0 <= idx < self.num_modes:
                self.psi[idx] *= (1.0 - self.dmn_damping)
        norm = np.linalg.norm(self.psi)
        if norm > 1e-12:
            self.psi /= norm

    def apply_sonic_modulation(self, mode: str = "128bpm_phase_lock", freq_hz: float = 45.0):
        if mode == "45hz_sub_bass":
            target_phase = (2 * np.pi * freq_hz / 1000.0) % (2 * np.pi)
            limit = min(8, self.num_modes)
            self.psi[:limit] = np.abs(self.psi[:limit]) * np.exp(1j * target_phase)
        elif mode == "128bpm_phase_lock":
            harmonic_phase = np.linspace(0, 4 * np.pi, self.num_modes)
            self.psi = np.abs(self.psi) * np.exp(1j * harmonic_phase)
        elif mode == "indigo_rain":
            pink_mag = self._spectral_profile_magnitudes("pink_noise")
            blended_mag = 0.65 * np.abs(self.psi) + 0.35 * pink_mag
            gentle_phase = np.angle(self.psi) + self._rng.normal(0, 0.08, self.num_modes)
            self.psi = blended_mag * np.exp(1j * gentle_phase)
        elif mode == "void_reset":
            self.psi = (1.0 / np.sqrt(self.num_modes)) * np.exp(1j * 0.0)

        norm = np.linalg.norm(self.psi)
        if norm > 1e-12:
            self.psi /= norm

    def enforce_coherence_corridor(self, max_iters: int = 16, profile: str = "pink_noise"):
        """
        Keep spectral entropy H_psi inside [h_min, h_max]:
          - If H_psi > h_max (divergent/flat spectrum), sharpen magnitudes with a gentle
            spectral focusing taper so even uniform states converge into the corridor.
          - If H_psi < h_min (calcified/looping spectrum), blend magnitudes with the
            IndigoNoise 1/f pink-noise profile by default (or optional 'brown_noise' /
            'uniform' profile) alongside gentle phase jitter so power redistributes out
            of the collapsed attractor without flat white-noise disruption.
        """
        taper = np.exp(-0.05 * np.arange(self.num_modes))
        recovery_mag = self._spectral_profile_magnitudes(profile)

        for _ in range(max_iters):
            entropy = self.compute_entropy()
            if entropy > self.h_max:
                mags = (np.abs(self.psi) ** 1.15) * taper
                phases = np.angle(self.psi)
                self.psi = mags * np.exp(1j * phases)
            elif entropy < self.h_min:
                mags = 0.72 * (np.abs(self.psi) ** 0.82) + 0.28 * recovery_mag
                jitter = self._rng.normal(0, 0.12, self.num_modes)
                phases = np.angle(self.psi) + jitter
                self.psi = mags * np.exp(1j * phases)
            else:
                break
            norm = np.linalg.norm(self.psi)
            if norm > 1e-12:
                self.psi /= norm

    def step_simulation(self, mode: str = "128bpm_phase_lock", profile: str = "pink_noise"):
        self.apply_dmn_gaba_dampener()
        self.apply_sonic_modulation(mode=mode)
        self.enforce_coherence_corridor(profile=profile)

        return {
            "entropy": round(self.compute_entropy(), 4),
            "coherence": round(self.compute_coherence(), 4),
            "spectral_norm": round(float(np.linalg.norm(self.psi)), 4),
            "profile": profile,
        }
