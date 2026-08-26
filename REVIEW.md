# .NET MAUI App Distribution Guide — Audit & Remediation Record

This document records an audit of this repository, the remediation that followed, and the
independent re-grading used to check that remediation. It is written to be read by someone who was
not present for any of it.

> **Status:** nine review rounds complete. **Latest independent grade: A−**, awarded after the
> nine propagation invariants were verified by enumeration rather than sampling. That grade named
> four single-line defects blocking an A; all four are now fixed, and a further cold grade on that
> state has not yet been run. §8 sets out what holding an A would require. Grades below are what
> independent reviewers actually returned, not targets.

---

## 1. How this audit was run

Seven independent review passes, each conducted by a reviewer with no knowledge of the previous
round's fixes and instructed not to read this file:

| # | Pass | Purpose |
|--:|---|---|
| 1 | Initial audit (three parallel reviewers) | Apple guides, Android guides, sample app + repo-wide link/consistency |
| 2 | Adversarial fact-check | Verify the round-1 corrections against first-party sources; hunt for errors they introduced |
| 3 | Independent re-grade | Grade the whole repository cold, against a fixed seven-dimension rubric |
| 4 | Independent re-grade | Same rubric, after round-3 fixes |
| 5 | Defect hunt | Target the newly changed material specifically |
| 6 | Propagation-pattern hunt | Target one specific recurring failure mode (see §4) |
| 7 | Confirming grade | Final verification against the same rubric |

Factual claims were verified against first-party Apple, Google and Microsoft documentation
throughout — not against the repository's own assertions.

## 2. Grade trajectory

| Round | Overall grade | What moved it |
|---|---|---|
| Initial audit | **B+** | Five confirmed errors, mostly self-consistency |
| Independent re-grade #1 | **C+** | *Lower.* Cold grading found defects the initial audit missed — including a flagship command that could not work |
| Independent re-grade #2 | **B−** | ArchiveOnBuild fix incomplete; wrong `keytool` command; unverifiable claims |
| Independent re-grade #3 | **B** | Four quick-starts still shipped unsigned build commands |
| Independent re-grade #4 | **B+** | `env:`/`file:` prefix contradiction; three propagation gaps |
| Independent re-grade #5 | **B+** | Bundle ID still said to live in `Info.plist` in the Apple hub |
| Independent re-grade #6 | **B+** | `apksigner` prescribed for an App Bundle; APK terminology over-corrected |
| Independent re-grade #7 | **A−** | **Bar met.** All nine propagation invariants verified by enumeration; four single-line defects named, all in reference files |

**Every grade from #1 onward awarded A on structure, cross-referencing, terminology and writing.**
The grade was held down each time by one or two defects of a single class — a claim repeated across
files where one copy disagreed. That is the whole story of this remediation.

**The dip from B+ to C+ is the most important line in this table.** The initial audit was too
generous. It graded structure, links and terminology thoroughly but did not check whether the
repository's *commands actually work*. A cold independent grader did, and found that the flagship
App Store guide's signing command omitted `ArchiveOnBuild=true` and therefore could never produce
the `.ipa` its own §11 promised. The first grade was not wrong about what it examined; it examined
the wrong things.

## 3. Defects found and corrected

Grouped by kind. Every item below was corrected, and every correction was verified against a
first-party source or the repository's own files.

### 3.1 Commands that could not do what the guide said

The most serious category, because this repository exists to make these commands trustworthy.

| Defect | Effect on a reader following the guide |
|---|---|
| App Store §10 signing command omitted `ArchiveOnBuild=true` / `RuntimeIdentifier` | Signs a build and writes **no package** — the exact trap the guide is written to warn about. Both sibling Apple guides carried the properties all along |
| Google Play §10 signing command omitted `AndroidKeyStore=true` | The property defaults to `false`; without it the signing properties are **silently ignored** and the output is the debug-signed bundle that same section says Play will reject |
| Four Android quick-starts said "**build and sign** the `.aab`" above a command with no signing properties at all | Same as above, reached faster — quick-starts are what a hurried reader follows |
| The Google Play quick-start gave the *failing* build command as "verified working" | §9 records that exact command failing from a clean tree with `XAGNM7009` |
| `env:` password prefix prescribed in six files that all upload App Bundles | Microsoft documents `env:` as unsupported when the package format is `aab` — and this repository's own direct APK guide explains that restriction |
| `keytool -list`, then `keytool -printcert -jarfile`, prescribed as the APK signature check | `keytool -list` reads a keystore, not a package. `-jarfile` reads only v1 signatures, so a v2/v3-only APK returns the same string the guide uses as proof of an *unsigned* file. Now `apksigner verify --print-certs` |

### 3.2 Claims contradicted by the guide's own evidence

- **§7 said an unsigned `dotnet publish` produces a self-signed `.ipa`.** Its own execution-verified
  §9, one section later, records that no package is produced at all. The SDK never emits one:
  device builds require a real identity, the archive target errors without a signing key, and the
  target that writes the package depends on `Codesign`.
- **"Ad hoc code signing" and "ad hoc distribution" were conflated.** They are unrelated. The first
  is the placeholder identity `-`, which .NET applies only to simulator builds; the second is an
  Apple distribution channel using a real certificate and a device-limited profile. Both are now
  defined separately in the terminology.
- **The platform comparison still said closed testing requires production access first** — the
  precise error the previous release's changelog claimed to have fixed. Only *open* testing does;
  closed testing is the route *to* production access.
- **TestFlight §18 still advertised review timings** that §13 had removed in the same release.

### 3.3 Facts wrong, unsourced, or overstated

- **TestFlight beta review "commonly 24 hours, reported as ranging 4–48 hours"** — Apple publishes
  no beta review turnaround time. The figures traced to no first-party source and are gone.
- **"The first production upload must be made manually through Play Console"** — Google documents no
  such rule; the Play Developer API can upload and create a draft release. What is true, and what
  the guide now says, is that the first release configures Play App Signing and fixes the upload key.
- **`APT2098`/`APT2261` cited as the long-path errors** — Microsoft documents **`APT2264`** for
  exceeding the Windows maximum path length, and even there says "generally caused by", not
  exclusively. (All three *are* real `APT2`-prefixed .NET for Android codes; the prefix is
  Microsoft's own namespace, not a misspelling of AAPT2. An earlier draft of this audit wrongly
  called them fabricated — see §5.)
- **Privacy manifest over-scoped** to all third-party SDKs; Apple requires it only for SDKs on its
  published list, plus required-reason APIs for all apps since 2024-05-01.
- **SDK floor framed as a submission requirement**; Apple frames it as an **upload** requirement.
- **"Play Review" used as a proper noun** — Google does not use that term. Its documentation says
  "app review"; Play Console shows the status "In review".
- **Play Protect described as "automatically blocking" named permission categories** — Google says
  "may prevent", and names no categories.
- **Target API level, App Bundle requirement, open-testing capacity, D-U-N-S, 180-day device
  removal** — each stated more absolutely than its source supports; all now carry the vendor's
  actual qualifications.
- **Three inference-as-fact claims softened**: the `dotnet/macios#20958` attribution (the issue's
  repro differs from the command run here), the marshal-methods workaround (observed, but not
  documented by Microsoft as the remedy), and the `XAGNM7009` decode (read off the SDK's error-code
  scheme, not from documentation).

### 3.4 Claims about the repository's own files that were untrue

- **"This repository's own `.gitignore` excludes common keystore file extensions."** It excluded
  `*.pfx` and nothing else relevant. Rather than soften the claim, `.gitignore` now actually
  excludes `*.keystore`, `*.jks`, `*.p12`, `*.mobileprovision`, `*.cer` and `keystore.properties`.
- **A §20 claimed it had restated §5's target API level.** §5 was unchanged. Now actually corrected.
- **An open-testing §20 claimed a "minimum permitted cap" clarification** that existed only in that
  note. Now made in §4, §12 and the quick-start.
- **The Bundle ID was said to live in `Info.plist`.** In single-project MAUI it does not —
  `<ApplicationId>` is the only source. A checklist step told readers to grep a file for a value it
  cannot contain.
- **References to a "Risk R-8", an "ADR 0015" and a JDK path "verified below"** — none exist here.
- **Two `start-here` prerequisites pointed at information the repository does not hold**: a
  freshness-register entry for supported .NET versions, and per-channel icon dimension "values".

### 3.5 Consistency and hygiene

- Verification dates: every channel guide still read 2026-08-23/24 while the register had advanced
  to 2026-08-26. Each §20 now separates **sources last verified** (which advances) from **execution
  evidence** (which does not — a run happened when it happened).
- The same iOS archive failure carried two different execution dates in two guides.
- Play Console's **Release → Test and release** rename reached only the managed-Play files; six
  testing paths and the unpublish path still used the old names.
- The completeness matrix still called the Google Play testing tracks undocumented, in a table
  whose own rows document them.
- The terminology table contradicted the guides on APK usage, and gave two terms vendors do not use
  ("iOS App Store Package", "Release Track").
- The root README overstated execution coverage and described the completeness matrix incorrectly.
- The sample project's retained Windows scaffolding contradicted its own scope comment; the
  Mac Catalyst target was built but recorded nowhere.

## 4. The pattern worth naming

**Nine times in this remediation, a correction and its copies fell out of step.** It happened with
the manual-upload claim, `ArchiveOnBuild`, `AndroidKeyStore=true`, the Play Console rename, the
"upload not submission" restatement, the `env:`/`file:` prefix, the Bundle ID's location, the
`keytool → apksigner` replacement, and the APK upload-format qualification.

**The last two are the subtler form.** They were not fixes that stopped short — they were fixes
that travelled *too far*. `apksigner` is genuinely the right tool to read an APK signature, and it
was copied into a checklist step whose artefact is an App Bundle, which Google documents it as
unable to read. The APK terminology row was correctly told that no Play *track* accepts an APK
today, and restated that as though it had always been true for every app. **A correction carried
into a context it does not fit is still a defect, and it is harder to grep for than one that was
simply missed.**

This is why six review rounds were needed for what looked like a short defect list. The errors were
not hard to fix; they were hard to *finish* fixing. A claim in this repository typically appears in
five or six places — the channel guide, its quick-start, the platform hub, the comparison table, a
checklist, and often the matrix or register.

The rule the remediation leaves behind is procedural: **verifying the set, not the fix, is what
"corrected" has to mean here**, and the grep that proves it belongs in the same commit as the fix.
That rule is now recorded in `CHANGELOG.md` for future maintenance.

## 5. Corrections to the original audit

Reported plainly, because an audit that hides its own errors is worth less than one that does not.

- **The original audit called `APT2098`/`APT2261` fabricated codes**, on the grounds that the `APT2`
  prefix looked like a misspelling of AAPT2. It is not — `APT2` is .NET for Android's own error
  namespace and all three codes are real. The genuine defect was narrower: `APT2264` is the code
  Microsoft actually ties to path length.
- **The original audit said "Play Review" should be propagated to five Android guides.** The
  opposite was correct: "Play Review" is not a term Google uses, so the terminology page itself was
  wrong and the guides were closer to right.
- **The original audit's B+ was too generous.** It did not test whether the documented commands
  work, which is where the two most serious defects were.
- Two items the original audit listed as "worth double-checking" resolved as **correct**: the
  App Store Connect distribution-method rule, and the `env:` prefix restriction.
- **Two defects were introduced by the remediation itself**, and found by later rounds:
  `apksigner` was prescribed for verifying an App Bundle, which Google documents it cannot read;
  and the APK terminology row was over-corrected into contradicting the freshness register. Both
  are recorded in `CHANGELOG.md` alongside the errors they were meant to fix, not separately.

## 6. What changed, and why

Every change, with its reason. Six commits on the `Review` branch.

| Commit | What changed | Why |
|---|---|---|
| `8ab2668` | Corrected eight unsupported claims; split every §20 into "sources last verified" and "execution evidence" | The claims were wrong or unsourced. The date split exists because re-checking a source was silently re-dating builds that had not been re-run |
| `08fe837` | Added `ArchiveOnBuild` to the App Store signing command; made `.gitignore` actually exclude signing material; fixed TestFlight §18, three §11→§10 references, the completeness matrix and the terminology APK row | The flagship command could not produce an `.ipa`. The `.gitignore` claim was false, so the file was changed rather than the claim softened |
| `f297469` | Added `AndroidKeyStore=true` to the Android signing command and checklist; replaced `keytool` with `apksigner`; removed references to a nonexistent risk register and ADR; corrected the root README's execution-coverage claim | Without `AndroidKeyStore=true` the signing properties are silently ignored. `keytool` cannot read a modern APK signature |
| `cb3e59e` | Added signing properties to four quick-start cards; corrected the Play Protect claim; reconciled two execution dates; fixed the IPA terminology row | The quick-starts told readers to "build and sign" with a command that did neither |
| `3906fac` | Switched six App Bundle commands from `env:` to `file:`; closed three propagation gaps; corrected the unpublish path; recorded the Mac Catalyst exclusion | Microsoft documents `env:` as unsupported for `.aab`, which this repository's own direct APK guide already explained |
| `350ceec` | Corrected the Apple hub's Bundle ID / `Info.plist` claim; scoped the `macios#20958` attribution to the ordering fault it actually describes; removed a false "JDK ships with the workload" claim | The hub is where a reader arrives first, and it contradicted the guide, the checklist and the sample |
| `HEAD` | Replaced `apksigner` with `jarsigner -verify -certs` for App Bundle verification; restored the "new apps since August 2021" qualification to the APK terminology row; cited §10 alongside §9 in four quick-starts; removed nine stray leading spaces | Two corrections had been carried into contexts they do not fit — the subtler half of the propagation pattern |

**Two things were deliberately *not* changed**, and the reasons are recorded in the files:

- **The sample app's stock template residue** — the retained `Platforms/Windows/` scaffolding, the
  unused `using`, the default counter page, the absence of a `global.json`. The sample's evidential
  value comes from being recognisably `dotnet new maui` output; tidying it would make the guide's
  build claims *harder* to reproduce. The project file now says so explicitly.
- **The "How this guide is kept true" section's five checks.** The verification tooling is not in
  this repository, so a reader cannot re-run them. Rather than delete the section or overstate it,
  it now tells the reader plainly that those claims are not falsifiable from a clone, and to weigh
  each guide's §9 and §18 more heavily instead.

## 7. Verification performed after each round

Run against the whole repository, mechanically, after every commit:

- Every relative link and heading anchor resolves (34 markdown files, GitHub slug rules).
- All ten guides carry exactly twenty sections, correctly numbered and ordered.
- No table has the historical blank-line-between-header-and-separator defect.
- No decorative emoji beyond the functional ☐ ballot box.
- Every signing command in every file carries its required properties (checked per-file, not by
  sampling — this is the check that would have caught the propagation failures earlier).
- No residual instance of any corrected term, path, URL or command.

## 8. What reaching grade A requires

**Not another manual round.** Eight have been run. Each awarded A on structure, links, terminology
and writing, and each was held down by one or two instances of the same defect class. The yield per
round is falling — five instances, then three, then two — but it has not reached zero, and the last
two instances were *introduced* by the previous round's fixes. Manual review is converging slowly
and generating new defects while it does so.

### The root cause

A claim in this repository typically lives in five or six places: the channel guide, its
quick-start, the platform hub, the comparison table, a checklist, and often the completeness matrix
or freshness register. **There is no mechanical way to assert that those copies agree.** Every fix
so far has been propagated by hand and checked by grep, and grep only finds what you already know
to look for. That is exactly why over-propagation — `apksigner` into an App Bundle context — slipped
through: nothing was missing, so nothing was missed.

### What would close it

**1. A claim-consistency checker.** Specified here rather than built, so the decision to adopt it
stays with the maintainer. It is the only measure that makes an A grade *stay* an A.

#### What it would assert

Each rule below encodes a defect that actually occurred during this remediation. That is the
selection criterion: no speculative rules, only regressions with a history.

| Invariant | Assertion | Instances it would have caught |
|---|---|---|
| Apple archive properties | Any command containing `CodesignKey` also contains `ArchiveOnBuild` and `RuntimeIdentifier` | 2 |
| Android signing properties | Any command containing `AndroidSigningKeyStore` also contains `AndroidKeyStore=true` and `AndroidEnableMarshalMethods=false` | 2 |
| Password prefix by format | `Pass=env:` never appears in a channel whose upload artefact is an App Bundle | 1 |
| Tool per artefact | `apksigner` never appears where the artefact is an `.aab`; `keytool -list` never used against a package | 1 |
| Navigation paths | Play Console paths carry the current top-level section name | 2 |
| Vendor qualifications | "new apps since August 2021", "uploaded to App Store Connect", "generally caused by" match the register's wording wherever the claim appears | 3 |
| Retired wording | Phrases withdrawn as wrong never reappear outside a retraction | — (preventive) |
| Claims about own files | Every statement about `.gitignore`, the sample's `ApplicationId`, or produced artefacts is checked against the file | 2 |
| Structure, links, tables | 20 sections in contract order; all relative links and anchors resolve; no blank line between a table header and its separator | 1 |

#### Two design points that matter

**Assertions must be one-directional.** "Every command with `CodesignKey` also has
`ArchiveOnBuild`" is correct. The converse is not: §9 of the ad hoc guide deliberately shows
`ArchiveOnBuild` *without* signing, because the resulting error is the evidence. A checker that
demanded symmetry would flag the guide's most valuable content and be switched off within a week.

**Retraction must stay sayable.** `CHANGELOG.md` and this file quote withdrawn wording in order to
say it was wrong. Any rule forbidding a phrase has to exempt them, or the honest changelog this
project is proud of becomes unwritable.

#### What it buys

- **It closes the gap that eight review rounds could not.** Every round found one to three new
  instances of the same class; two were *introduced* by the previous round's fixes. That is a
  process converging too slowly to trust, and the checker replaces recall with execution.
- **It catches over-propagation, which grep cannot.** The `apksigner` defect had nothing missing —
  a correct tool sat in a context it did not fit. Only an assertion tying tool to artefact finds it.
- **It makes the repository's central claim falsifiable.** The root README lists five things
  "checks confirm", and currently has to add that a reader cannot re-run them from a clone. A
  committed checker turns that caveat into an instruction, which is a materially stronger position
  for a project whose thesis is that nothing is correct merely because it was written.
- **It converts review effort into review coverage.** Eight passes were spent rediscovering the
  same class of defect. Encoding it once frees later reviews to look at things a script cannot
  judge — whether the guidance is *good*, not merely consistent.
- **It protects the freshness register's whole purpose.** Vendor requirements change on a schedule;
  when a figure is updated, the checker names every file that must move with it.

#### What it costs

Roughly a day to write, and a standing obligation: every future correction must either pass the
rules or add one. The real cost is a policy reversal — release 1.1.0 deliberately removed this
repository's verification tooling so that "what is published here is the verified result rather
than the machinery that verifies it". A committed checker contradicts that. Two ways out: revisit
the 1.1.0 decision on the grounds that a *consistency* checker is documentation about the
documentation rather than build machinery, or keep it beside the repository as the existing tooling
already lives, and accept that readers still cannot run it. **The first is the honest option**, and
it is the one that resolves the falsifiability caveat rather than restating it.

**2. One exhaustive sweep by enumeration, not sampling.** For each of the seven invariants above,
list every file asserting the claim and diff them. Prior rounds sampled; sampling is what left the
eighth and ninth instances.

**3. Two judgement calls the graders raised more than once**, neither strictly a defect:
   - Whether the root README's five verification claims should stay at all, given the tooling that
     backs them is not in the repository. They currently carry an explicit "you cannot falsify this
     from a clone" caveat, which one grader accepted and another still called an overreach.
   - Whether the sample app should keep its stock template residue. Documented as deliberate, but it
     costs a mark on the sample dimension every time a grader meets it fresh.

### Honest expectation

Items 1 and 2 would very likely produce an A on the next cold grade: nothing outside the propagation
class has been flagged as a material defect since round three, and every grader has explicitly said
the underlying work is A-grade. But this document should not predict a grade it has not received —
eight rounds have shown that this repository's defects are found by looking, not by reasoning about
whether any remain.

**A− was reached at round seven**, and the reasoning above held: the grader enumerated all nine
propagation invariants across every file asserting them, found no tenth instance, and awarded A−.
Its four blocking defects were all single-line, all in **reference** files rather than guides —
`terminology.md` twice, the freshness register once, and one loose word in a prerequisites
paragraph. That is a telling distribution: the reference documents carry the most authority per
line and get the least scrutiny per line, because reviewers read them as the source of truth rather
than as claims to check.

All four are now fixed. **Whether that reaches A is unmeasured** — no cold grade has run against
the fixed state, and this document does not award grades to itself.

### Status of the checker

**Specified above, deliberately not built.** Adopting it is a maintainer's decision, because it
reverses a documented policy (1.1.0) rather than merely adding a file. This section exists so that
decision can be made on the evidence — nine recorded instances, the rules that would have caught
each, and the cost of both options — rather than on a recollection of how the audit felt.

---

*Audit and remediation performed against this repository on 2026-08-26, on the `Review` branch.
Findings are file- and line-referenced in the commit messages and in `CHANGELOG.md` 1.3.0.*
