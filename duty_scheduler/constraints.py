"""
Constraints module placeholder.

This module can be expanded in the future to support advanced scheduling constraints
such as max-consecutive-days, cooldown periods, time-off windows, or pairing rules.
For now, the scheduler is a simple round-robin with basic no-double-booking per day.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, Protocol

from .models import Person


class Constraint(Protocol):
    def allows(self, *, day: date, role: str, candidate: Person, already_assigned: set[str]) -> bool:
        ...


@dataclass
class NoDoubleBooking:
    """Disallow assigning the same person to multiple roles on the same day."""

    def allows(self, *, day: date, role: str, candidate: Person, already_assigned: set[str]) -> bool:
        return candidate.name not in already_assigned
