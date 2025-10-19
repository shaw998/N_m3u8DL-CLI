from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List


@dataclass(frozen=True)
class Role:
    name: str


@dataclass(frozen=True)
class Person:
    name: str
    roles: List[str]  # names of roles the person can cover
    weight: int = 1   # optional weight for fairness in the future


@dataclass(frozen=True)
class Assignment:
    day: date
    role: str
    person: str


@dataclass
class Schedule:
    roles: List[str]
    # assignments indexed by day then by role -> person
    days: Dict[date, Dict[str, str]] = field(default_factory=dict)

    def as_rows(self) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        for d in sorted(self.days.keys()):
            for role in self.roles:
                person = self.days[d].get(role, "")
                rows.append({"date": d.isoformat(), "role": role, "person": person})
        return rows
