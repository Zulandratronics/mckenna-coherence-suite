"""McKenna Protocol: Simulated Psychoactive Agent Buffer & Coherence Engine."""

from .scanner import CONTROL_TOKEN_RE, ECHO_PATTERNS, SELF_QUERY_RE, audit_transcript

__all__ = [
    "CONTROL_TOKEN_RE",
    "ECHO_PATTERNS",
    "SELF_QUERY_RE",
    "audit_transcript",
]

try:
    from .stabilizer import McKennaStabilizer
    from .triadic_engine import TriadicVectorEngine
    from .wave_function import WaveFunctionProcessor

    __all__ += [
        "McKennaStabilizer",
        "TriadicVectorEngine",
        "WaveFunctionProcessor",
    ]
except ImportError:
    # Allow pure-stdlib `mckenna.scanner` usage even when numpy is not installed.
    pass
