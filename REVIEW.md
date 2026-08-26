# .NET MAUI App Distribution Guide — Audit

**Overall grade: B+**

## What this project is

A documentation-only repository that walks a .NET MAUI developer through ten
distribution channels — four on Apple (App Store public release, TestFlight,
ad hoc, Business Manager/Enterprise) and six on Android (Google Play public
release, internal/closed/open testing, managed Google Play, direct APK).
Every channel guide follows the same fixed twenty-section contract, backed by
a channel catalogue, a controlled-terminology glossary, a completeness
matrix, and a dated requirements-freshness register. A minimal sample MAUI
app exists to back two specific, unusually concrete claims: that
`dotnet publish -f net10.0-ios` reports success while writing no `.ipa`, and
that `dotnet publish -f net10.0-android` fails on a clean tree without
`-p:AndroidEnableMarshalMethods=false`.

The project's stated discipline is unusual for documentation: claims are
labelled by whether they were execution-verified or sourced, a changelog
records corrected mistakes as mistakes rather than "improvements," and a
register tracks exactly when each time-sensitive figure was last checked.
That discipline is also the yardstick this audit holds it to — most of the
findings below are places where the guide didn't quite live up to its own
stated standard, not places where it invented facts.

## Grade by dimension

| Dimension | Grade | Why |
|---|---|---|
| Structural contract (20-section rule) | A | All 10 guides carry all 20 sections, correctly numbered and ordered, matching the catalogue exactly. No exceptions found. |
| Cross-referencing & link integrity | A | Every relative link and heading anchor across the whole repository resolves, including awkward slugs like the double-hyphen anchor for "§16. Revoke / Withdraw / Retire." |
| Technical accuracy | B | Fees, limits, and dates check out almost everywhere against the freshness register — but one channel guide directly contradicts its own execution-verified findings, and a real tool's error code is misspelled in two places. |
| Self-consistency of the "verified" claim | B- | The changelog asserts a repo-wide re-verification that the individual channel guides' own dates and one of their own source links don't actually reflect. |
| Terminology discipline | B- | The controlled-terminology page is followed almost everywhere, but the mandated term for Google's review process is missing from five of six Android guides. |
| Sample app & supporting code | A- | A coherent, standard, buildable MAUI template that doesn't contradict any claim made about it. One inert leftover (Windows platform scaffolding in an explicitly non-Windows project). |
| Writing, navigation & honesty of framing | A | Exceptionally well organised: consistent voice, mermaid diagrams that earn their place, checklists with real dependency columns, and forthright "documented, not demonstrated" labelling. |

## Confirmed errors

Verified directly against the repository's own files — not inferred, not a
matter of interpretation.

### 1. A core claim about ad-hoc signing contradicts the guide's own tested result

**File:** `platforms/apple/app-store-public-release/README.md` — §7 vs §9,
propagated into its quick-start and into
`platforms/apple/ad-hoc-distribution/README.md` §7

§7 (Security Model) says running `dotnet publish` without a real
distribution certificate "produces a package .NET signs itself, for local
verification only" — describing an actual, installable, ad-hoc-signed
`.ipa`. But §9 (Build), the guide's own execution-verified section run
against this repo's sample app, proves the *same command* writes no package
at all: an empty publish folder, on a Windows host. One section of the
document contradicts a claim the very next section disproves by execution.
The quick-start and the ad-hoc-distribution guide's own §7 repeat the same
framing.

**Fix:** rewrite §7 to match §9 — plain `dotnet publish` on Windows with no
`CodesignKey`/`CodesignProvision` produces **no** package, ad hoc-signed or
otherwise. If "ad hoc signing" (per the terminology page) genuinely does
produce a local `.ipa` on a Mac host, say that explicitly and stop implying
it applies to the tested Windows path.

### 2. A real tool's error code is misspelled — twice

**File:** `platforms/android/google-play-public-release/README.md:71` vs
`:181`, and `platforms/android/README.md:74`

Line 71 correctly names the tool **AAPT2**. But the troubleshooting table
two headings later, and the Android platform hub, both cite the failure
code as `APT2098`/`APT2261` — missing the tool's own leading "A". `APT2…`
isn't a real AAPT2 code prefix, which makes it read as a transcription error
at best and a fabricated code at worst — exactly the kind of unverifiable
specific the rest of this guide is careful to avoid.

**Fix:** correct both to `AAPT2098`/`AAPT2261`, and confirm the exact codes
against a real failing build before publishing them as evidence.

### 3. The guide's own controlled term for Google's review is missing from five of six Android guides

**File:** `docs/reference/terminology.md:20` vs closed-testing,
open-testing, internal-testing, managed-google-play-enterprise,
direct-apk-distribution READMEs

The terminology page mandates **"Play Review"** as the one term for
Google's review of a submitted app, and states "every guide in this
repository uses these terms consistently." The Android platform hub uses it
correctly. Five of the six channel guides instead say "policy review" or
"standard Play policy review" — a paraphrase the terminology page exists
specifically to rule out.

**Fix:** replace "policy review" with "Play Review" throughout, or — if the
two terms are meant to describe genuinely different things — add "Policy
Review" to the terminology page as its own defined concept.

### 4. A "corrected" source URL was only corrected in the register, not in the guide that also cites it

**File:** `CHANGELOG.md:18-19` vs
`platforms/apple/ad-hoc-distribution/README.md:294-295`

CHANGELOG v1.2.0 states a source URL was updated after Apple moved the page,
from `/help/account/register-devices/…` to `/help/account/devices/…`. The
freshness register does use the new path. But the ad-hoc-distribution
guide's own §19 Official Sources still links the old, superseded
`register-devices` URLs in two places — the exact page the changelog claims
was fixed.

**Fix:** update both links in `ad-hoc-distribution/README.md` §19 to the
`/help/account/devices/…` path.

### 5. Channel guides' own "Last Verified" dates weren't advanced with the register

**File:** `CHANGELOG.md:13-14` vs every `platforms/*/README.md` §20 (and
inline dates in §4)

The changelog says all 25 freshness-register requirements were re-verified
and their date "advanced to 2026-08-26" — and the register itself does show
2026-08-26 throughout. But every individual channel guide's own §20 Last
Verified section (and inline dates such as the Eligibility section's "Last
verified: 2026-08-23") still reads 2026-08-23 or 2026-08-24. The register
and the guides that depend on it are now out of step by two or three days,
on a project whose entire premise is that a verification date means
something.

**Fix:** either advance each guide's own §20 (and any inline verification
date) to match the register, or narrow the changelog's wording so it's
clearly scoped to the register alone.

## Worth double-checking

Plausible and not contradicted by anything else in the repo, but not
independently confirmed against a primary source in this pass — worth a
source check before treating as settled.

- **A quick-start link's label promises more than its target.**
  `platforms/apple/testflight/docs/quick-start.md` — the "§4–§11" link spans
  §4 through §11 in its label, but the anchor only resolves to §4
  (Eligibility). Not broken, just misleading. *Fix:* split into two links,
  or narrow the label to "§4".

- **The "public → unlisted only" post-approval rule is stated very
  precisely.** `platforms/apple/business-manager-and-enterprise/README.md` —
  §12 and §17. Plausible and matches the general shape of Apple's Custom
  Apps rules, but wasn't independently re-verified word-for-word against the
  cited Apple Support page in this pass.

- **A narrow claim about the `env:` keystore-password prefix and `.aab`.**
  `platforms/android/direct-apk-distribution/README.md:184` states the
  `env:` prefix for signing passwords isn't supported when the package
  format is `.aab`. Specific and plausible, but not independently confirmed
  against Microsoft's signing-task source in this pass.

- **An exact Play Console navigation path may drift.**
  `platforms/android/managed-google-play-enterprise/README.md:114` —
  "Release > Setup > Advanced settings" as the path to the Managed Google
  Play tab is the kind of UI detail Google reshuffles without notice. Worth
  a click-through re-confirmation before each release.

## Repository hygiene

**Windows platform scaffolding survives in an explicitly non-Windows
project.** `sample/DistributionSample/Platforms/Windows/*` vs
`DistributionSample.csproj:4-7`. The `.csproj` targets only
`net10.0-android`, and conditionally `net10.0-ios`/`net10.0-maccatalyst`,
with a comment stating Windows is "deliberately omitted" for this phase.
`Platforms/Windows/` still contains a full set of template files, including
a `Package.appxmanifest` with unfilled `$placeholder$` values. Harmless —
MSBuild won't compile an untargeted platform folder — but it's dead weight
that contradicts the project's own stated scope line.

**Fix:** delete `Platforms/Windows/`, or add a one-line note saying it's
kept intentionally for a future in-scope phase.

## What holds up

- All ten channel guides contain exactly the twenty required sections,
  correctly numbered and in the mandated order — no gaps, no reordering, no
  duplicates.
- Every relative link and heading anchor in the repository resolves
  correctly under GitHub's actual slugging rules, including the
  double-hyphen anchor produced by "§16. Revoke / Withdraw / Retire."
- The historical "blank line between a table's header and separator row"
  rendering bug, named in the changelog as fixed, does not recur anywhere in
  the current files.
- Decorative emoji are genuinely gone; the ☐ ballot-box glyph is the sole,
  deliberate survivor, exactly as the changelog describes.
- Fees, tester limits, API-level floors, closed-testing quotas and
  organisation caps are consistent everywhere they're cited against the
  freshness register — this was checked figure-by-figure, not spot-checked.
- The sample MAUI app is a coherent, standard, buildable single-project
  template with no internal contradictions, and nothing in it undercuts the
  specific build-warning claims the guide's credibility rests on.
- The project is candid about its own limits: most channels are labelled
  "documented, not demonstrated," and only two build paths carry an
  execution-verified artefact on disk.

## Overall assessment

This is unusually rigorous documentation for what it is — a project that
runs the commands it describes, keeps a dated register of exactly when
every time-sensitive figure was last checked, and writes its own changelog
in terms of "this was wrong" rather than "this improved." That rigor is
visible in the structure (a genuinely enforced twenty-section contract
across ten guides) and in the writing (honest labelling of what was
executed versus sourced).

The grade sits at **B+** rather than higher because the errors found are not
random noise — they cluster exactly where the project's own standard is
hardest to meet: keeping a global "everything re-verified" claim true across
every file that depends on it, and keeping a section's prose in step with
the guide's own execution results one section later. A misspelled tool
error code and a missing controlled term round out a short but concrete
list. None of it is severe on its own; together it's a reminder that the
last-mile propagation of a fix — from register to guide, from build log to
prose — needs the same checklist discipline the project already applies to
everything else.

> "Nothing here is reported as correct because it was written." — README.md.
> The standard the project sets for itself is the right one; five findings
> above are places it didn't quite clear its own bar.

---

*Audit performed against this repository as of 2026-08-26. Findings are
file- and line-referenced above; re-check each against the current working
tree before acting, in case the repository has changed since.*
