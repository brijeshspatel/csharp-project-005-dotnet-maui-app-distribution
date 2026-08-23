"""Grade the Channel Completeness Matrix.

One row per distribution channel, one column per required guide section. A
blank cell means nobody decided whether that section applies -- this script
refuses to let that pass as done. A cell reading exactly "N/A - <reason>" is
an explicit decision and is accepted.

A row must occupy one physical line. A hard-wrapped row is not a table row,
and it is reported as a failure rather than skipped -- silently skipping one is
how a channel can appear graded while being examined by nothing.

Exit codes:
  0  every declared channel's every column is filled or explicitly N/A
  1  a cell is blank, or a row's cell count does not match the header
  2  the table could not be read
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

NA_RE = re.compile(r"^N/A\s*[-—]\s*\S.*$")


def parse_table(text: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = [line for line in text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        print("CANNOT CHECK - no Markdown table found", file=sys.stderr)
        raise SystemExit(2)

    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    malformed: list[str] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(header):
            # A row whose cell count does not match the header is NOT skipped.
            # Skipping is how a hard-wrapped row -- which is not a table row at
            # all -- got graded by nothing while the matrix reported "OK".
            malformed.append(
                f"{cells[0][:40]!r} has {len(cells)} cell(s), header has {len(header)}"
            )
            continue
        rows.append(dict(zip(header, cells)))
    if malformed:
        print(
            f"FAIL - {len(malformed)} malformed row(s); a row must be one physical line:",
            file=sys.stderr,
        )
        for m in malformed:
            print(f"  {m}", file=sys.stderr)
        raise SystemExit(1)
    return header, rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="path to the completeness matrix Markdown file")
    args = parser.parse_args()

    path = pathlib.Path(args.path)
    if not path.is_file():
        print(f"CANNOT CHECK - {path} does not exist", file=sys.stderr)
        return 2

    header, rows = parse_table(path.read_text(encoding="utf-8"))
    if not header or header[0] != "Channel":
        print("CANNOT CHECK - first column must be 'Channel'", file=sys.stderr)
        return 2

    if not rows:
        print("OK - 0 channel(s) checked (matrix is empty)")
        return 0

    columns = header[1:]
    failures = []
    for row in rows:
        channel = row.get("Channel", "?")
        for col in columns:
            value = row.get(col, "").strip()
            if not value:
                failures.append(f"{channel!r} / {col!r} is blank")
            elif value.upper().startswith("N/A") and not NA_RE.match(value):
                failures.append(
                    f"{channel!r} / {col!r} is 'N/A' without a stated reason "
                    f"(expected 'N/A - <reason>', got {value!r})"
                )

    if failures:
        print(f"FAIL - {len(failures)} incomplete cell(s):", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1

    print(f"OK - {len(rows)} channel(s), {len(columns)} column(s) each, all complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
