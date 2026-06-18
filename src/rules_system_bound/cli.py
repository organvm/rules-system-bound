"""Command line activation check for rules-system-bound."""

from __future__ import annotations

import argparse
import json
from typing import Any

from . import __version__
from .container import Container, ContainmentRules
from .interaction import InteractionEmergence, System


def build_activation_report() -> dict[str, Any]:
    """Run a small end-to-end package smoke check."""
    universe = Container(
        id="universe",
        function="all",
        purpose="contains everything",
        boundary="porous",
        properties={"scale_range": (0, 10)},
    )
    subsystem = Container(
        id="subsystem",
        function="organized",
        purpose="organized function",
        boundary="sealed",
        properties={"scale": 1},
    )

    containment_passed = universe.can_contain(subsystem, ContainmentRules())

    processor = System(id="processor", function="process", purpose="does work", scale=1.0)
    store = System(id="store", function="store", purpose="holds state", scale=1.0)
    emergence = InteractionEmergence()
    emergence.register_system(processor)
    emergence.register_system(store)
    interactions = emergence.discover_interactions(processor, store)

    interaction_types = [interaction.interaction_type for interaction in interactions]
    status = "ok" if containment_passed and interaction_types else "failed"

    return {
        "package": "rules-system-bound",
        "version": __version__,
        "status": status,
        "checks": {
            "containment": containment_passed,
            "interaction_count": len(interactions),
            "interaction_types": interaction_types,
        },
    }


def format_report(report: dict[str, Any]) -> str:
    """Format an activation report for humans."""
    checks = report["checks"]
    interaction_types = ", ".join(checks["interaction_types"])
    return "\n".join(
        [
            f"{report['package']} activation: {report['status']}",
            f"version: {report['version']}",
            f"containment: {'passed' if checks['containment'] else 'failed'}",
            f"interactions: {interaction_types}",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    """Run the command line activation check."""
    parser = argparse.ArgumentParser(
        prog="rules-system-bound",
        description="Run the rules-system-bound activation smoke check.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable activation evidence.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args(argv)

    report = build_activation_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_report(report))

    return 0 if report["status"] == "ok" else 1

