from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, TypedDict

from .models import Person


class PeopleDef(TypedDict):
    roles: List[str]
    people: List[Dict[str, Any]]


# Minimal internal schema declaration for validation (no external deps)
_REQUIRED_ROOT_KEYS = {"roles", "people"}


def _validate_people_data(data: Dict[str, Any]) -> PeopleDef:
    if not isinstance(data, dict):
        raise ValueError("People definition must be an object")

    missing = _REQUIRED_ROOT_KEYS - data.keys()
    if missing:
        raise ValueError(f"Missing required keys: {', '.join(sorted(missing))}")

    roles = data.get("roles")
    if not isinstance(roles, list) or not all(isinstance(r, str) and r.strip() for r in roles):
        raise ValueError("'roles' must be a non-empty list of non-empty strings")

    people = data.get("people")
    if not isinstance(people, list) or not people:
        raise ValueError("'people' must be a non-empty list")

    seen_names: set[str] = set()
    for idx, p in enumerate(people):
        if not isinstance(p, dict):
            raise ValueError(f"people[{idx}] must be an object")
        name = p.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"people[{idx}].name must be a non-empty string")
        if name in seen_names:
            raise ValueError(f"Duplicate person name: {name}")
        seen_names.add(name)
        proles = p.get("roles")
        if not isinstance(proles, list) or not all(isinstance(r, str) and r in roles for r in proles):
            raise ValueError(f"people[{idx}].roles must be a list of role names declared in 'roles'")
        weight = p.get("weight", 1)
        if not isinstance(weight, int) or weight <= 0:
            raise ValueError(f"people[{idx}].weight must be a positive integer if provided")

    # Type is structurally sound
    return data  # type: ignore[return-value]


def parse_people(data: Dict[str, Any]) -> tuple[list[str], list[Person]]:
    validated = _validate_people_data(data)
    roles = list(validated["roles"])  # copy
    people_models: list[Person] = []
    for p in validated["people"]:
        people_models.append(
            Person(name=p["name"], roles=list(p["roles"]), weight=int(p.get("weight", 1)))
        )
    return roles, people_models


def load_people(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    # Validate eagerly
    _ = _validate_people_data(raw)
    return raw
