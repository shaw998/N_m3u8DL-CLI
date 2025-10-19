from __future__ import annotations

from collections import deque
from datetime import date, timedelta
from typing import Dict, List

from .models import Person, Schedule
from .input import parse_people


class SchedulingError(Exception):
    pass


def _round_robin_candidates(people: List[Person], role: str) -> deque[Person]:
    candidates = [p for p in people if role in p.roles]
    if not candidates:
        raise SchedulingError(f"No candidates available for role '{role}'")
    # Sort deterministically by name to ensure stable output
    candidates.sort(key=lambda p: (p.name.lower(), p.weight))
    # Weighting by duplicating entries in the rotation
    weighted: List[Person] = []
    for p in candidates:
        weighted.extend([p] * max(1, p.weight))
    return deque(weighted)


def build_schedule(people_def: Dict[str, object], start: date, days: int) -> Schedule:
    if days <= 0:
        raise ValueError("days must be > 0")

    roles, people = parse_people(people_def)  # validates structure

    rotations: Dict[str, deque[Person]] = {r: _round_robin_candidates(people, r) for r in roles}

    sched = Schedule(roles=roles)

    for i in range(days):
        day = start + timedelta(days=i)
        sched.days[day] = {}
        used_today: set[str] = set()
        for role in roles:
            rotation = rotations[role]
            # Pick next person not yet used today for a different role (prevent double booking on same day)
            person = None
            for _ in range(len(rotation)):
                candidate = rotation[0]
                rotation.rotate(-1)
                if candidate.name not in used_today:
                    person = candidate
                    break
            if person is None:
                # fallback: allow double booking if unavoidable
                person = rotation[0]
                rotation.rotate(-1)
            used_today.add(person.name)
            sched.days[day][role] = person.name

    return sched
