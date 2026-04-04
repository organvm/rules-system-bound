"""Configuration loader for rules-system-bound."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

DEFAULT_CONFIG: dict[str, Any] = {
    "container_function": "function",
    "container_purpose": "purpose",
    "container_limits": "limits",
    "container_boundary": "boundary",
    "containment_function_weight": 0.4,
    "containment_scale_weight": 0.3,
    "containment_boundary_weight": 0.3,
    "containment_precedence": "context_dependent",
    "ideal_platonic": "platonic",
    "ideal_weberian": "weberian",
    "ideal_normalized": "normalized",
    "domain_family": "physical",
    "primitive_type": "unspecified",
    "level_names_emerge": True,
    "auto_containment_check": True,
}


@dataclass
class Config:
    """Configuration for the Living Container Framework."""

    container_function: str = "function"
    container_purpose: str = "purpose"
    container_limits: str = "limits"
    container_boundary: str = "boundary"

    containment_function_weight: float = 0.4
    containment_scale_weight: float = 0.3
    containment_boundary_weight: float = 0.3
    containment_precedence: str = "context_dependent"

    ideal_platonic: str = "platonic"
    ideal_weberian: str = "weberian"
    ideal_normalized: str = "normalized"

    domain_family: str = "physical"
    primitive_type: str = "unspecified"

    level_names_emerge: bool = True
    auto_containment_check: bool = True

    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> Config:
        """Load configuration from environment variables."""
        config = {}
        for key, default in DEFAULT_CONFIG.items():
            env_key = f"{key.upper()}"
            config[key] = os.getenv(env_key, default)
        return cls(**config)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Config:
        """Create config from dictionary."""
        known = {k: v for k, v in data.items() if k in DEFAULT_CONFIG}
        extras = {k: v for k, v in data.items() if k not in DEFAULT_CONFIG}
        known["extras"] = extras
        return cls(**known)


def get_config() -> Config:
    """Get the current configuration."""
    return Config.from_env()
