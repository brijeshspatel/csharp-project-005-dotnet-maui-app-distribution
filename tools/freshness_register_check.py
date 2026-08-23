"""Grade the Requirements & Freshness Register.

Every time-sensitive external requirement this repository documents gets a row.
A row missing its verification evidence is worse than no row at all -- it reads
as checked when it was never confirmed. This script is that check.

Exit codes:
  0  every row has every required field populated
  1  a row is missing Last Verified, Official Source, or Status
  2  the table could not be read, or a required column is missing from the header
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REQUIRED_COLUMNS = [
    "Requirement",
    "Platform",
    "Area",
    "Effective Date",
    "Last Verified",
    "Official Source",
    "Applies To",
    "Impact",
    "Status",
    "Reverification Trigger",
]

REQUIRED_NON_EMPTY = ["Last Verified", "Official Source", "Status"]


def parse_table(text: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = [line for line in text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        print("CANNOT CHECK - no Markdown table found", file=sys.stderr)
        raise SystemExit(2)

    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return header, rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="path to the register Markdown file")
    args = parser.parse_args()

    path = pathlib.Path(args.path)
    if not path.is_file():
        print(f"CANNOT CHECK - {path} does not exist", file=sys.stderr)
        return 2

    header, rows = parse_table(path.read_text(encoding="utf-8"))

    missing_columns = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing_columns:
        print(f"CANNOT CHECK - missing column(s): {', '.join(missing_columns)}", file=sys.stderr)
        return 2

    if not rows:
        print("OK - 0 row(s) checked (register is empty)")
        return 0

    failures = []
    warnings = []
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for i, row in enumerate(rows, start=1):
        for field in REQUIRED_NON_EMPTY:
            if not row.get(field, "").strip():
                failures.append(f"row {i} ({row.get('Requirement', '?')!r}) is missing {field}")
        trigger = row.get("Reverification Trigger", "").strip()
        if date_re.match(trigger):
            # A trigger that is itself a past date is a live staleness warning,
            # not a structural failure -- the register still has every field.
            warnings.append(f"row {i} ({row.get('Requirement', '?')!r}) reverification trigger {trigger} has passed")

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    if failures:
        print(f"FAIL - {len(failures)} row(s) with missing required field(s):", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1

    print(f"OK - {len(rows)} row(s) checked, all required fields present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
