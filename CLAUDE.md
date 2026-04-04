# rules-system-bound

A generalized system for organizing hierarchically nested containers where the hierarchy emerges from the contained systems themselves, not predetermined levels.

## Core Concept

The Living Container Framework provides rules for containment, interaction, and idealized form reflection/refraction. The hierarchy emerges from what's contained, not from predetermined structures.

## Key Principles

- **Containment**: Multi-factor (function + scale + boundary), context-dependent precedence
- **Primitives**: Unspecified - each instantiation defines its own smallest unit
- **Top boundary**: Self-defining
- **Idealized forms**: Co-constitutive with real systems
- **Interactions**: Emergent from specific system relations

## Development

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests -v

# Lint
ruff check src tests
```

## Structure

```
src/rules_system_bound/
├── container.py      # Core container model
├── containment.py    # Containment rules
├── idealization.py  # Idealized forms
├── interaction.py   # Interaction emergence
└── config.py        # Environment config
```
