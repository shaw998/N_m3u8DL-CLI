import argparse
from datetime import date
from pathlib import Path
from typing import Optional

from .input import load_people
from .scheduler import build_schedule
from .export import to_console_table, to_csv


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}': {e}")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="duty_scheduler",
        description="Simple duty scheduler with JSON input and CSV/console output.",
    )
    p.add_argument(
        "--people",
        "-p",
        type=Path,
        required=True,
        help="Path to people JSON file (see examples/people.json)",
    )
    p.add_argument(
        "--start",
        "-s",
        type=_parse_date,
        required=True,
        help="Start date in YYYY-MM-DD format.",
    )
    p.add_argument(
        "--days",
        "-d",
        type=int,
        default=7,
        help="Number of days to schedule (default: 7)",
    )
    p.add_argument(
        "--csv",
        "-o",
        type=Path,
        required=False,
        help="Optional path to write CSV output. If omitted, only a console table is printed.",
    )
    p.add_argument(
        "--no-table",
        action="store_true",
        help="Do not print the console table (useful when only CSV is desired).",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    people_def = load_people(args.people)
    sched = build_schedule(people_def, start=args.start, days=args.days)

    # CSV export if requested
    if args.csv:
        to_csv(sched, args.csv)

    if not args.no_table:
        print(to_console_table(sched))

    return 0
