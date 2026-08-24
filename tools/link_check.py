"""Verify that external links in this repository's Markdown actually resolve.

This proves reachability only. A link that returns 200 is not proof that its
content is still current or authoritative -- that judgement belongs in the
Requirements & Freshness Register, not here. See docs/reference/terminology-v1.0.1.md
and the specification's own §3.4 for why the two checks are kept separate.

Exit codes:
  0  every checked link resolves (2xx final status), uses HTTPS, and did not
     redirect to a different host
  1  at least one link failed
"""

from __future__ import annotations

import argparse
import glob
import re
import ssl
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

LINK_RE = re.compile(r"\bhttps?://[^\s)>\]\"']+")
TIMEOUT_SECONDS = 10

def _build_ssl_context() -> ssl.SSLContext:
    """Build a context trusting the same roots curl/the OS already trust.

    On a machine behind a TLS-inspecting local proxy, neither Python's
    bundled OpenSSL store nor certifi's bundle contains the proxy's injected
    root certificate, so every HTTPS request fails verification even for a
    genuinely live site -- confirmed here by fault-planting a known-good URL
    (developer.apple.com) and observing the same verify failure a broken
    domain produces, while `curl` (which uses the OS store) succeeds.
    Loading the Windows ROOT/CA stores, which do trust it, is what makes this
    checker's failures mean what they say rather than reporting the local
    environment's own certificate gap as every link being broken.
    """
    context = ssl.create_default_context()
    if sys.platform == "win32":
        for store in ("ROOT", "CA"):
            for cert, encoding, _trust in ssl.enum_certificates(store):
                try:
                    context.load_verify_locations(cadata=ssl.DER_cert_to_PEM_cert(cert))
                except ssl.SSLError:
                    continue
    return context


_SSL_CONTEXT = _build_ssl_context()


def find_links(path: str) -> list[tuple[str, int, str]]:
    found = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            for match in LINK_RE.finditer(line):
                found.append((path, lineno, match.group(0).rstrip(".,")))
    return found


def check_link(url: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return False, "not HTTPS"

    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "link-check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS, context=_SSL_CONTEXT) as response:
            final_host = urlparse(response.geturl()).hostname
            if final_host != parsed.hostname:
                return False, f"redirected to a different host ({parsed.hostname} -> {final_host})"
            return True, f"{response.status}"
    except urllib.error.HTTPError as head_error:
        if head_error.code == 405:
            # Some servers reject HEAD outright; fall back to GET.
            get_request = urllib.request.Request(url, method="GET", headers={"User-Agent": "link-check/1.0"})
            try:
                with urllib.request.urlopen(get_request, timeout=TIMEOUT_SECONDS, context=_SSL_CONTEXT) as response:
                    final_host = urlparse(response.geturl()).hostname
                    if final_host != parsed.hostname:
                        return False, f"redirected to a different host ({parsed.hostname} -> {final_host})"
                    return True, f"{response.status}"
            except (urllib.error.HTTPError, urllib.error.URLError) as get_error:
                return False, str(get_error)
        return False, f"HTTP {head_error.code}"
    except urllib.error.URLError as error:
        return False, str(error)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("glob_pattern", help="glob of Markdown files to scan, e.g. 'channels/**/*.md'")
    args = parser.parse_args()

    files = sorted(glob.glob(args.glob_pattern, recursive=True))
    if not files:
        print(f"CANNOT CHECK - no files matched {args.glob_pattern!r}", file=sys.stderr)
        return 1

    links: list[tuple[str, int, str]] = []
    for path in files:
        links.extend(find_links(path))

    if not links:
        print(f"OK - 0 link(s) found across {len(files)} file(s)")
        return 0

    failures = 0
    print(f"{'RESULT':<6} {'FILE:LINE':<60} URL")
    for path, lineno, url in links:
        ok, detail = check_link(url)
        status = "OK" if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"{status:<6} {path}:{lineno:<50} {url}  ({detail})")

    if failures:
        print(f"\nFAIL - {failures}/{len(links)} link(s) did not resolve cleanly", file=sys.stderr)
        return 1

    print(f"\nOK - {len(links)} link(s) checked across {len(files)} file(s), all resolved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
