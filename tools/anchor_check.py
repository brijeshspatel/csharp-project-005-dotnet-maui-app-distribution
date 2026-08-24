"""Resolve every in-repository Markdown heading anchor.

A link of the form `](guide.md#7-security-model)` makes two claims: the file
exists, and it contains a heading whose anchor is that fragment. Nothing in this
repository checked the second one. `mdgs_check.py` matches links that end at
`.md)`, so an anchored link never matches its pattern at all, and `link_check.py`
matches `https?://` only. 74 anchors were unresolved before this script existed.

The slug rule, which decides every verdict this script gives:

  lowercase; remove every character that is not a word character, whitespace or
  a hyphen; map each remaining space to one hyphen. Runs of whitespace are NOT
  collapsed.

That last clause is the whole difference. A removed character sitting between
two spaces leaves both spaces behind, so `## 16. Revoke / Withdraw / Retire`
yields `16-revoke--withdraw--retire` with a double hyphen -- which is exactly
what this repository's own authors wrote, and the evidence the rule is right.
A collapsing implementation reported four false failures on those links.

The rule is stated in --help and repeated in the failure output on purpose: it
is a recorded assumption rather than a verified fact (no renderer could be
observed here), so a reader who disagrees with the verdict needs to know which
rule produced it. See DEC-A6 in the increment A specification.

Exit codes:
  0  every anchor resolved
  1  at least one anchor did not resolve
  2  the glob matched no file -- "matched nothing" is never reported as a pass
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

SLUG_RULE = (
    "lowercase, drop every character that is not a word character, whitespace "
    "or hyphen, then map each remaining space to one hyphen. Runs of whitespace "
    "are NOT collapsed, so '16. Revoke / Withdraw / Retire' -> "
    "'16-revoke--withdraw--retire'."
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
# A link with a URI scheme is not a repository-relative path. Windows drive
# letters (C:/...) match the same shape and are equally not repo-relative.
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
LINK_RE = re.compile(r"\]\(([^)\s]*?\.md)#([^)\s]+)\)")
SELF_LINK_RE = re.compile(r"\]\(#([^)\s]+)\)")


def slugify(heading: str) -> str:
    """Anchor for a heading's text, per SLUG_RULE."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def headings(text: str) -> list[str]:
    """Heading texts, ignoring anything inside a fenced code block.

    A shell comment such as `# Generate the key` inside a ```bash fence matches
    the heading pattern and is not a heading. Counting it would invent an anchor
    that no renderer produces, which can only ever mask a real failure.
    """
    found: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            found.append(m.group(2).strip())
    return found


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Resolve in-repository Markdown heading anchors.",
        epilog="Slug rule: " + SLUG_RULE,
    )
    ap.add_argument("glob_pattern", help="glob of Markdown files, e.g. '**/*.md'")
    args = ap.parse_args()

    root = pathlib.Path.cwd()
    files = sorted(p for p in root.glob(args.glob_pattern) if p.is_file())
    if not files:
        print(
            f"CANNOT CHECK - glob {args.glob_pattern!r} matched no file. "
            "A check that matched nothing is not a pass.",
            file=sys.stderr,
        )
        return 2

    anchors: dict[pathlib.Path, set[str]] = {}
    texts: dict[pathlib.Path, str] = {}
    for p in files:
        texts[p] = p.read_text(encoding="utf-8")
        anchors[p] = {slugify(h) for h in headings(texts[p])}

    failures: list[str] = []
    resolved = 0

    for p in files:
        rel = p.relative_to(root).as_posix()
        for m in LINK_RE.finditer(texts[p]):
            target, frag = m.group(1), m.group(2).lower()
            if SCHEME_RE.match(target):
                continue
            tp = (p.parent / target).resolve()
            if tp not in anchors:
                if not tp.exists():
                    failures.append(f"{rel}: {target}#{frag} -> target file does not exist")
                    continue
                # In range of the glob's directory but not the glob itself.
                anchors[tp] = {slugify(h) for h in headings(tp.read_text(encoding="utf-8"))}
            if frag in anchors[tp]:
                resolved += 1
            else:
                near = sorted(
                    a for a in anchors[tp] if re.sub(r"-+", "-", a) == re.sub(r"-+", "-", frag)
                )
                hint = f" (did you mean #{near[0]}?)" if near else ""
                failures.append(f"{rel}: {target}#{frag} -> no such anchor{hint}")

        for m in SELF_LINK_RE.finditer(texts[p]):
            frag = m.group(1).lower()
            if frag in anchors[p]:
                resolved += 1
            else:
                failures.append(f"{rel}: #{frag} -> no such anchor in this file")

    if failures:
        print(f"FAIL - {len(failures)} unresolved anchor(s):", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        print(f"\nSlug rule applied: {SLUG_RULE}", file=sys.stderr)
        return 1

    print(f"OK - {resolved} anchor(s) resolved across {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
