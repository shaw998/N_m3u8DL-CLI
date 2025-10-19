Duty Scheduler (Python)

A minimal, dependency-free CLI for generating simple duty rotation schedules from a JSON
file. Designed as scaffolding for future expansion.

Quick start

- Inspect the example input: examples/people.json
- Run the CLI with module execution:

  python -m duty_scheduler -p examples/people.json -s 2025-01-01 -d 7 -o schedule.csv

- Omit -o to only print a console table. Add --no-table to suppress console output and only write CSV.

Input JSON format

{
  "roles": ["primary", "secondary"],
  "people": [
    { "name": "Alice", "roles": ["primary", "secondary"], "weight": 1 },
    { "name": "Bob", "roles": ["primary"] }
  ]
}

Notes

- roles: list of role names to be scheduled each day.
- people: list where each entry has:
  - name: unique string
  - roles: subset of roles the person can cover
  - weight: optional positive integer indicating rotation frequency weight

Behavior

- Round-robin per role with deterministic ordering by name.
- Basic no-double-booking constraint: the same person won't be assigned to two roles on the same day if avoidable.
- Outputs both a console table and CSV (if -o provided).

Development

- No external dependencies beyond the Python standard library.
- Run basic smoke tests with pytest or the Python test runner that discovers tests/ directory.
