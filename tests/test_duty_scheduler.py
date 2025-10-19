from __future__ import annotations

import unittest
from datetime import date
from pathlib import Path

from duty_scheduler.input import load_people, parse_people
from duty_scheduler.scheduler import build_schedule
from duty_scheduler.export import to_console_table, to_csv


ROOT = Path(__file__).resolve().parents[1]


class TestDutyScheduler(unittest.TestCase):
    def test_load_and_parse_people(self):
        people_path = ROOT / "examples" / "people.json"
        data = load_people(people_path)
        roles, people = parse_people(data)

        self.assertEqual(set(roles), {"primary", "secondary"})
        self.assertEqual({p.name for p in people}, {"Alice", "Bob", "Carol"})

    def test_build_schedule_and_export(self):
        people_path = ROOT / "examples" / "people.json"
        data = load_people(people_path)

        sched = build_schedule(data, start=date(2025, 1, 1), days=3)

        # Expect 3 days * 2 roles assignments
        rows = sched.as_rows()
        self.assertEqual(len(rows), 6)

        # Console table returns a string containing header and a date
        table = to_console_table(sched)
        self.assertIn("Date", table)
        self.assertIn("2025-01-01", table)

        # CSV export writes file and has a header with 3 columns
        tmp_dir = Path(self._get_temp_dir())
        csv_path = tmp_dir / "schedule.csv"
        to_csv(sched, csv_path)
        content = csv_path.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(content[0].strip(), "date,role,person")
        self.assertEqual(len(content), 1 + len(rows))

    def _get_temp_dir(self) -> str:
        # unittest provides a helper in newer versions, but to keep it simple,
        # create a temp folder under the test directory.
        tmp = ROOT / ".tmp-test-output"
        tmp.mkdir(parents=True, exist_ok=True)
        return str(tmp)


if __name__ == "__main__":
    unittest.main()
