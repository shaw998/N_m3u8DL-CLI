from __future__ import annotations

from pathlib import Path
from typing import List

from .models import Schedule


def to_console_table(schedule: Schedule) -> str:
    # Build a simple table string with headers: Date | role1 | role2 | ...
    roles = schedule.roles
    dates = sorted(schedule.days.keys())

    headers = ["Date", *roles]
    col_widths = [max(len("Date"), 10)] + [max(len(r), 8) for r in roles]

    # Compute row data and adjust column widths
    rows: List[List[str]] = []
    for d in dates:
        row = [d.isoformat()]
        for i, r in enumerate(roles):
            person = schedule.days[d].get(r, "")
            row.append(person)
            col_widths[i + 1] = max(col_widths[i + 1], len(person))
        col_widths[0] = max(col_widths[0], len(row[0]))
        rows.append(row)

    # Build the table string
    def fmt_row(values: List[str]) -> str:
        parts = []
        for i, v in enumerate(values):
            parts.append(v.ljust(col_widths[i]))
        return " | ".join(parts)

    sep = "-+-".join("-" * w for w in col_widths)

    lines = [fmt_row(headers), sep]
    for row in rows:
        lines.append(fmt_row(row))
    return "\n".join(lines)


def to_csv(schedule: Schedule, path: Path) -> None:
    import csv

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "role", "person"]) 
        writer.writeheader()
        for row in schedule.as_rows():
            writer.writerow(row)
