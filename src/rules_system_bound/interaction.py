"""Interaction emergence between systems."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Interaction:
    """
    An interaction between two systems.

    Interactions emerge from specific system relations,
    not from predefined categories.
    """

    id: str
    source: Any
    target: Any

    # Interaction type (emergent, not preset)
    interaction_type: str = ""

    # Description of the interaction
    description: str = ""

    # Properties
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class System:
    """
    A system with functions that can interact with other systems.

    Key principle: Interactions emerge from what the systems ARE,
    not from predefined interaction categories.
    """

    id: str
    function: str
    purpose: str

    # Boundary characteristics
    boundary: str = "semi_permeable"

    # Scale (for containment rules)
    scale: float = 1.0

    # What this system contains
    contains: list[Any] = field(default_factory=list)

    # Metadata
    properties: dict[str, Any] = field(default_factory=dict)

    def can_interact_with(self, other: System) -> list[Interaction]:
        """
        Determine what interactions can emerge with another system.

        Returns list of possible interactions (emergent, not preset).
        """
        interactions = []

        # Function-based interactions
        if self._function_compatible(other):
            interactions.append(
                Interaction(
                    id=f"{self.id}_func_{other.id}",
                    source=self,
                    target=other,
                    interaction_type="function_coupling",
                    description=f"{self.function} couples with {other.function}",
                )
            )

        # Boundary-based interactions
        if self._boundary_allows(other):
            interactions.append(
                Interaction(
                    id=f"{self.id}_boundary_{other.id}",
                    source=self,
                    target=other,
                    interaction_type="boundary_exchange",
                    description="Boundary-mediated exchange",
                )
            )

        # Scale-based interactions
        if self._scale_permits(other):
            interactions.append(
                Interaction(
                    id=f"{self.id}_scale_{other.id}",
                    source=self,
                    target=other,
                    interaction_type="scale_resonance",
                    description="Scale-based resonance",
                )
            )

        return interactions

    def _function_compatible(self, other: System) -> bool:
        """Check if functions are compatible for interaction."""
        # Domain-specific logic
        return True

    def _boundary_allows(self, other: System) -> bool:
        """Check if boundaries allow interaction."""
        permeability = {
            "porous": 3,
            "semi_permeable": 2,
            "sealed": 1,
        }
        return permeability.get(self.boundary, 0) > 0

    def _scale_permits(self, other: System) -> bool:
        """Check if scale permits interaction."""
        # Simple proximity check
        return abs(self.scale - other.scale) < 10


class InteractionEmergence:
    """
    Manages interaction emergence between systems.

    Key principle: All interactions are possible implementations,
    but context filters which emerge.
    """

    def __init__(self):
        self.systems: dict[str, System] = {}
        self.interactions: list[Interaction] = []

    def register_system(self, system: System) -> None:
        """Register a system."""
        self.systems[system.id] = system

    def discover_interactions(self, system_a: System, system_b: System) -> list[Interaction]:
        """Discover emergent interactions between two systems."""
        interactions = system_a.can_interact_with(system_b)
        self.interactions.extend(interactions)
        return interactions

    def discover_all_interactions(self) -> list[Interaction]:
        """Discover all possible interactions between all registered systems."""
        all_interactions = []
        system_list = list(self.systems.values())

        for i, sys_a in enumerate(system_list):
            for sys_b in system_list[i + 1 :]:
                all_interactions.extend(self.discover_interactions(sys_a, sys_b))

        return all_interactions
