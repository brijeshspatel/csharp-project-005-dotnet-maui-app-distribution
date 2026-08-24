"""Grade the navigation documents no other checker in this repository reaches.

Two checkers grade Markdown here, and between them they miss most of it:

  mdgs_check.py       grades docs/**            -- 4 files
  pattern_docs_check  grades platforms/*/*/docs -- 10 files

That leaves 18 files graded by nothing at all: every channel README, both
platform hubs, the five start-here documents, and the root README. They were
governed on paper and examined by no tool, which is how nine stale claims
survived in them while every checker reported OK.

Two rules are deliberately NOT applied, and the reason matters:

  * the durable filename grammar ^[a-z0-9-]+-v\\d+\\.\\d+\\.\\d+\\.md$
  * the filename-to-frontmatter version coupling

These 18 files carry a version in their frontmatter and no version in their
names. mdgs_check enforces that coupling for docs/**, and applying it here
would fail all 17 frontmatter-bearing files immediately. Renaming them was
considered and rejected: it changes every inbound link for no reader benefit.

The root README is exempt from the frontmatter rule -- all four sibling
projects' root READMEs have none, and a renderer that displays frontmatter
would put a metadata table above the landing page's first line. It is graded by
the table-of-contents rule instead: every channel the catalogue lists as
documented must appear in it, with a link that resolves. That rule is what
stops the table of contents decaying the way the old README did.

Exit codes:
  0  every graded file satisfies every applicable rule
  1  at least one file does not
  2  nothing was graded, or the catalogue could not be read
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path.cwd()
CATALOGUE = pathlib.Path("docs/maui-distribution-channel-catalogue-v1.0.0.md")
ROOT_README = "README.md"

REQUIRED_KEYS = [
    "doc_id",
    "title",
    "type",
    "version",
    "status",
    "created",
    "updated",
    "owner",
]

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

POLICY = pathlib.Path("config/markdown-governance.policy.json")


def type_vocabulary() -> list[str]:
    """The permitted `type` values, read from this project's own policy.

    Read rather than hard-coded: a second copy of the vocabulary is a second
    thing to keep in step, and the one that drifts is always the copy.
    """
    if not POLICY.exists():
        print(f"CANNOT CHECK - policy not found at {POLICY}", file=sys.stderr)
        raise SystemExit(2)
    vocab = json.loads(POLICY.read_text(encoding="utf-8")).get("naming", {}).get(
        "type_vocabulary", []
    )
    if not vocab:
        print("CANNOT CHECK - policy declares no naming.type_vocabulary", file=sys.stderr)
        raise SystemExit(2)
    return vocab


def tracked_markdown() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.md"], capture_output=True, text=True, check=True
    ).stdout
    return [line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()]


def graded_elsewhere(rel: str) -> bool:
    return rel.startswith("docs/") or re.match(r"platforms/[^/]+/[^/]+/docs/", rel) is not None


def frontmatter(text: str) -> dict[str, str] | None:
    """Scalar frontmatter fields. Deliberately not a YAML parser.

    Every field this checker grades is a single-line scalar, and a real parser
    would be a dependency this repository does not otherwise need.
    """
    if not text.startswith("---"):
        return None
    _, _, rest = text.partition("---")
    block, sep, _ = rest.partition("\n---")
    if not sep:
        return None
    fields: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([a-z_]+): (.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def catalogue_channels() -> list[str]:
    """Channel names from the catalogue's documented table."""
    if not CATALOGUE.exists():
        print(f"CANNOT CHECK - catalogue not found at {CATALOGUE}", file=sys.stderr)
        raise SystemExit(2)
    text = CATALOGUE.read_text(encoding="utf-8")
    section = text.partition("## Documented channels")[2].partition("\n## ")[0]
    names: list[str] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("Channel", "") or set(cells[0]) <= {"-", ":"}:
            continue
        names.append(cells[0])
    if not names:
        print("CANNOT CHECK - no documented channels parsed from the catalogue", file=sys.stderr)
        raise SystemExit(2)
    return names


def main() -> int:
    files = [f for f in tracked_markdown() if not graded_elsewhere(f)]
    if not files:
        print(
            "CANNOT CHECK - no navigation document matched. Every checker here reads the "
            "git index, so a new file must be staged (git add -N) before it is graded.",
            file=sys.stderr,
        )
        return 2

    failures: list[str] = []
    vocabulary = type_vocabulary()

    for rel in sorted(files):
        text = (ROOT / rel).read_text(encoding="utf-8")

        if rel == ROOT_README:
            continue  # graded by the table-of-contents rule below

        fields = frontmatter(text)
        if fields is None:
            failures.append(f"{rel}: no parseable frontmatter block")
            continue
        for key in REQUIRED_KEYS:
            if key not in fields or not fields[key]:
                failures.append(f"{rel}: frontmatter is missing required key {key!r}")
        doc_type = fields.get("type", "")
        if doc_type and doc_type not in vocabulary:
            failures.append(
                f"{rel}: type {doc_type!r} is not in the policy's type vocabulary {vocabulary}"
            )
        version = fields.get("version", "")
        if version and not VERSION_RE.match(version):
            failures.append(f"{rel}: version {version!r} is not MAJOR.MINOR.PATCH")
        created, updated = fields.get("created", ""), fields.get("updated", "")
        for label, value in (("created", created), ("updated", updated)):
            if value and not DATE_RE.match(value):
                failures.append(f"{rel}: {label} {value!r} is not YYYY-MM-DD")
        if DATE_RE.match(created) and DATE_RE.match(updated) and updated < created:
            failures.append(f"{rel}: updated {updated} is earlier than created {created}")

    # --- the table-of-contents rule -----------------------------------------
    readme_path = ROOT / ROOT_README
    if ROOT_README not in files:
        failures.append(f"{ROOT_README}: not tracked, so the table of contents was not graded")
    else:
        readme = readme_path.read_text(encoding="utf-8")
        links = {m.group(1) for m in re.finditer(r"\]\(([^)\s]+\.md)\)", readme)}
        for channel in catalogue_channels():
            if channel not in readme:
                failures.append(
                    f"{ROOT_README}: catalogue channel {channel!r} is missing from the "
                    "table of contents"
                )
        for link in sorted(links):
            if not (readme_path.parent / link).exists():
                failures.append(f"{ROOT_README}: table-of-contents link does not resolve: {link}")

    if failures:
        print(f"FAIL - {len(failures)} violation(s) across {len(files)} file(s):", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1

    print(f"OK - {len(files)} file(s) checked, no violations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
