"""Core container model for hierarchical system containment."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Container:
    """
    A bounded region that can contain other systems.

    Every container defines:
    - FUNCTION: What it enables/produces
    - PURPOSE: Why it exists
    - LIMITS: What it cannot do (by design)
    - BOUNDARY: Permeability type
    """

    id: str
    function: str
    purpose: str
    limits: set[str] = field(default_factory=set)
    boundary: str = "semi_permeable"  # porous, semi_permeable, sealed

    # Structural relationships
    parent: Optional[Container] = None
    children: list[Container] = field(default_factory=list)

    # Contents - actual systems contained
    contains: list[Any] = field(default_factory=list)

    # Metadata
    properties: dict[str, Any] = field(default_factory=dict)

    def can_contain(self, other: Container, rules: ContainmentRules) -> bool:
        """Check if this container can contain another container."""
        return rules.check_containment(self, other)

    def envelops(self, other: Container) -> bool:
        """Check if this container envelops another."""
        return other in self.children

    def enveloped_by(self) -> Optional[Container]:
        """Get the container that envelops this one."""
        return self.parent

    def add_child(self, child: Container) -> None:
        """Add a child container."""
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: Container) -> None:
        """Remove a child container."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def get_lineage(self) -> list[Container]:
        """Get the full lineage from this container to the top."""
        lineage = [self]
        current = self.parent
        while current:
            lineage.append(current)
            current = current.parent
        return lineage

    def get_descendants(self) -> list[Container]:
        """Get all descendants recursively."""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants


@dataclass
class ContainmentRules:
    """
    Rules for determining containment relationships.

    Multi-factor containment:
    - Function compatibility
    - Scale relation
    - Boundary permeability
    """

    function_weight: float = 0.4
    scale_weight: float = 0.3
    boundary_weight: float = 0.3
    precedence: str = "context_dependent"  # function_first, scale_first, boundary_first, context_dependent

    def check_containment(self, container: Container, contained: Container) -> bool:
        """
        Check if container can contain contained system.

        All three factors must pass (AND logic).
        """
        func_compat = self._check_function_compatibility(container, contained) > 0.0
        scale_compat = self._check_scale_relation(container, contained)
        boundary_perm = self._check_boundary_permeability(container, contained)

        return func_compat and scale_compat and boundary_perm

    def _check_function_compatibility(
        self, container: Container, contained: Container
    ) -> float:
        """Check if functions are compatible using Jaccard similarity over tokens."""
        c_tokens = set(container.function.lower().split())
        cont_tokens = set(contained.function.lower().split())

        if not c_tokens and not cont_tokens:
            return 1.0

        intersection = c_tokens.intersection(cont_tokens)
        union = c_tokens.union(cont_tokens)

        if not union:
            return 0.0

        return len(intersection) / len(union)

    def _check_scale_relation(self, container: Container, contained: Container) -> bool:
        """Check if scale relationship allows containment."""
        container_scale = container.properties.get("scale_range", (0, float("inf")))
        contained_scale = contained.properties.get("scale", 0)
        min_scale, max_scale = container_scale
        return min_scale <= contained_scale <= max_scale

    def _check_boundary_permeability(
        self, container: Container, contained: Container
    ) -> bool:
        """Check if boundary permeability allows containment."""
        boundary_perm = {
            "porous": ["porous", "semi_permeable", "sealed"],
            "semi_permeable": ["semi_permeable", "sealed"],
            "sealed": ["sealed"],
        }
        allowed = boundary_perm.get(container.boundary, [])
        return contained.boundary in allowed

    def compute_containment_score(
        self, container: Container, contained: Container
    ) -> float:
        """Compute a score for containment compatibility (0-1)."""
        func_score = self._check_function_compatibility(container, contained)
        scale_score = 1.0 if self._check_scale_relation(container, contained) else 0.0
        boundary_score = (
            1.0 if self._check_boundary_permeability(container, contained) else 0.0
        )

        return (
            func_score * self.function_weight
            + scale_score * self.scale_weight
            + boundary_score * self.boundary_weight
        )
