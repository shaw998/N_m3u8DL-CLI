"""Duty Scheduler package.

Provides a simple, dependency-free scaffolding for scheduling on-call/rotation duties
from a JSON definition of people and roles. Offers a CLI entry point via
`python -m duty_scheduler`.
"""

from .models import Person, Role, Assignment, Schedule
from .input import load_people
from .scheduler import build_schedule
from .export import to_console_table, to_csv

__all__ = [
    "Person",
    "Role",
    "Assignment",
    "Schedule",
    "load_people",
    "build_schedule",
    "to_console_table",
    "to_csv",
]

__version__ = "0.1.0"
