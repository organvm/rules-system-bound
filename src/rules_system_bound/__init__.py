"""rules-system-bound: Living Container Framework."""

from .config import Config, get_config
from .container import Container, ContainmentRules
from .idealization import (
    IdealizationType,
    IdealizedForm,
    IdealizationManager,
    co_constitute,
    reflect,
    refract,
    project,
    approximate,
)
from .interaction import Interaction, System, InteractionEmergence

__version__ = "0.1.0"

__all__ = [
    "Config",
    "get_config",
    "Container",
    "ContainmentRules",
    "IdealizationType",
    "IdealizedForm",
    "IdealizationManager",
    "Interaction",
    "System",
    "InteractionEmergence",
    "co_constitute",
    "reflect",
    "refract",
    "project",
    "approximate",
]
