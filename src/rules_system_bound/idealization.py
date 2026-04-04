"""Idealized forms and their co-constitutive relationship with real systems."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IdealizationType(Enum):
    """Types of idealized forms."""

    PLATONIC = "platonic"
    WEBERIAN = "weberian"
    NORMALIZED = "normalized"


@dataclass
class IdealizedForm:
    """
    An idealized representation of a system.

    Three types:
    - PLATONIC: Perfect archetype
    - WEBERIAN: Essential function captured
    - NORMALIZED: Representation of real instances
    """

    id: str
    type: IdealizationType
    name: str
    description: str = ""

    # Relationship to real system
    reflects: bool = False  # Mirrors the real
    refracts: bool = False  # Bends/distorts
    projects: bool = False  # Maps between levels
    approximates: bool = False

    # The actual system this idealizes
    real_system: Any = None

    # Properties specific to the idealization
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class IdealizationRelation:
    """Relationship between idealized forms and real systems."""

    ideal: IdealizedForm
    real: Any

    # Relationship type
    is_reflect: bool = False
    is_refract: bool = False
    is_project: bool = False
    is_approximate: bool = False
    is_co_constitutive: bool = False


class IdealizationManager:
    """
    Manages idealized forms and their relations to real systems.

    Key principle: Ideal and real are CO-CONSTITUTIVE
    - They don't just mirror each other
    - They create each other
    """

    def __init__(self):
        self.forms: dict[str, IdealizedForm] = {}
        self.relations: list[IdealizationRelation] = []

    def create_form(
        self,
        form_id: str,
        form_type: IdealizationType,
        name: str,
        real_system: Any = None,
        **options,
    ) -> IdealizedForm:
        """Create a new idealized form."""
        form = IdealizedForm(
            id=form_id, type=form_type, name=name, real_system=real_system, **options
        )
        self.forms[form_id] = form
        return form

    def relate(
        self, ideal: IdealizedForm, real: Any, relation_type: str = "co_constitutive"
    ) -> IdealizationRelation:
        """Establish relationship between ideal and real."""
        relation = IdealizationRelation(
            ideal=ideal,
            real=real,
            is_co_constitutive=relation_type == "co_constitutive",
            is_reflect=relation_type == "reflect",
            is_refract=relation_type == "refract",
            is_project=relation_type == "project",
            is_approximate=relation_type == "approximate",
        )
        self.relations.append(relation)
        return relation

    def get_forms_for(self, real: Any) -> list[IdealizedForm]:
        """Get all idealized forms for a real system."""
        return [r.ideal for r in self.relations if r.real == real]

    def get_real_for(self, ideal: IdealizedForm) -> Any:
        """Get the real system for an idealized form."""
        for r in self.relations:
            if r.ideal.id == ideal.id:
                return r.real
        return None


def reflect(ideal: IdealizedForm, real: Any) -> IdealizationRelation:
    """Create a reflection relation (mirror)."""
    return IdealizationRelation(
        ideal=ideal,
        real=real,
        is_reflect=True,
        is_co_constitutive=False,
    )


def refract(ideal: IdealizedForm, real: Any) -> IdealizationRelation:
    """Create a refraction relation (bend/distort)."""
    return IdealizationRelation(
        ideal=ideal,
        real=real,
        is_refract=True,
        is_co_constitutive=False,
    )


def project(ideal: IdealizedForm, real: Any) -> IdealizationRelation:
    """Create a projection relation (map between levels)."""
    return IdealizationRelation(
        ideal=ideal,
        real=real,
        is_project=True,
        is_co_constitutive=False,
    )


def approximate(ideal: IdealizedForm, real: Any) -> IdealizationRelation:
    """Create an approximation relation."""
    return IdealizationRelation(
        ideal=ideal,
        real=real,
        is_approximate=True,
        is_co_constitutive=False,
    )


def co_constitute(ideal: IdealizedForm, real: Any) -> IdealizationRelation:
    """Create a co-constitutive relation (ideal and real create each other)."""
    return IdealizationRelation(
        ideal=ideal,
        real=real,
        is_co_constitutive=True,
    )
