# Changelog

Notable changes to this guide. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This is a documentation project, so "changed" usually means a claim changed, and the reason
matters more than the diff. Where a claim was **wrong**, this log says so plainly rather than
describing the correction as an improvement.

## [1.2.0] — 2026-08-26

### Changed

- Every one of the 25 requirements in the freshness register re-verified against its first-party
  source. All 25 claims confirmed correct; `Last Verified` advanced to 2026-08-26.
- Time-sensitive claims rewritten to survive their own deadline. Five places said "API 35 now,
  API 36 from 2026-08-31", which becomes false on that date; they now state the requirement and
  that Google raises the floor annually.
- One source URL updated after Apple moved the page (`/help/account/register-devices/...` now
  `/help/account/devices/...`).

### Fixed

- **Corrected a wrong statement about Google Play closed testing.** The guide said closed testing
  requires production access. It does not — closed testing is the route *to* production access
  (12 testers, opted in continuously for 14 days). Only **open** testing requires production
  access first.
- Repaired Markdown tables that did not render. A line-ending fault had put a blank line between
  each table header and its separator row, so several tables showed as raw pipes on GitHub.
- Repaired bold markers left broken by the emoji removal below.

### Added

- The API level 36 deadline can be extended to 2026-11-01 through Play Console. The guide now
  says so.

### Removed

- All decorative emoji. A partially applied convention is worse than none, and this one had
  drifted more than once. The ballot box in the checklist tables stays: it is functional, because
  task-list syntax does not render inside a table cell.

## [1.1.0] — 2026-08-25

### Added

- Release checklists rebuilt as tables: step, phase, action, what it depends on, expected result,
  how to verify, and a tick box.
- Five Mermaid diagrams: channel selection, release lifecycle, Apple signing relationships,
  Android key handling, and the guide's own navigation path.
- Both platform hubs now carry the signing model, common prerequisites, build warnings, release
  management and shared troubleshooting their channels were each repeating.

### Changed

- `start-here/` groups by platform: shared material at the top, the two release checklists under
  `apple/` and `android/`.
- Root `README.md` rebuilt as a landing page and table of contents.

### Removed

- Markdown frontmatter, from every file. GitHub renders it as a metadata table above the first
  heading, so a reader's first sight was internal metadata rather than the page. Version history
  lives in git.
- The repository's own verification tooling and governance configuration. What is published here
  is the verified result; the machinery that verifies it is maintained separately.

## [1.0.0] — 2026-08-24

### Added

- All ten distribution channels documented: four Apple (App Store public release, TestFlight, ad
  hoc, Business Manager and enterprise) and six Android (Google Play public release, internal,
  closed and open testing, managed Google Play, direct APK).
- Every channel follows the same fixed twenty-section contract.
- Channel catalogue, controlled terminology, completeness matrix and freshness register.

### Fixed

- Two build claims that were wrong, both found by execution rather than by reading:
  - `dotnet publish -f net10.0-ios -c Release` **writes no `.ipa`** while printing that it did and
    exiting 0. The SDK emits that message whenever `BuildIpa` is set, without ever creating the
    package.
  - `dotnet publish -f net10.0-android -c Release` **fails from a clean tree** with `XAGNM7009`.
    `-p:AndroidEnableMarshalMethods=false` makes it succeed.
