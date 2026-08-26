# Changelog

Notable changes to this guide. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This is a documentation project, so "changed" usually means a claim changed, and the reason
matters more than the diff. Where a claim was **wrong**, this log says so plainly rather than
describing the correction as an improvement.

## [1.3.0] — 2026-08-26

Six successive audits — an external review, an adversarial fact-check of the resulting corrections,
two independent re-grades of the whole repository, and two dedicated defect hunts — found faults at
every stage, including many the earlier rounds had introduced or left behind. All are listed below
and named as errors, not as improvements.

**Each pass found what the previous one missed, and the pattern is the finding.** A correction
applied to five files but not the sixth is not a correction; it is a contradiction with better
coverage. That happened *six separate times* in this release: with the manual-upload claim,
`ArchiveOnBuild`, `AndroidKeyStore=true`, the Play Console **Test and release** rename, the
"upload, not submission" restatement, and the `env:`/`file:` password prefix. Every time the fix
itself was right and its propagation was not.

**So the rule this release leaves behind is procedural, not factual.** A claim in this repository
typically appears in five or six places — the channel guide, its quick start, the platform hub, the
comparison table, a checklist, and often the completeness matrix or freshness register. Correcting
the guide is the easy half. **Verifying the set is what "corrected" has to mean here**, and the
grep that proves it belongs in the same commit as the fix. Six rounds of review were needed to
learn that, which is itself worth recording: the errors were not hard to fix, they were hard to
*finish* fixing.

**Two findings deserve singling out, because both were commands this guide told readers to run
that could not do what the guide said they would.** The App Store guide's signing command omitted
`ArchiveOnBuild`, so it could never produce the `.ipa` its own §11 promised. The Google Play
guide's signing command omitted `AndroidKeyStore=true`, so it silently produced the debug-signed
package its own §10 warned would be rejected. Neither was a wrong fact about a vendor; both were
this repository failing at precisely the thing it claims to be for.

### Fixed

- **Corrected a claim this guide contradicted one section later.** The App Store guide's §7 said
  an unsigned `dotnet publish` "produces a package .NET signs itself, for local verification
  only". Its own §9, which was execution-verified, records that the same command produces **no
  package at all**. The SDK never emits a self-signed `.ipa`: device builds require a real
  identity, the archive target errors without a code-signing key, and the target that writes the
  package depends on `Codesign`. §7, the App Store quick start and the ad hoc guide's §7 all
  repeated the error and are all corrected.
- **Corrected a conflation of two unrelated Apple concepts.** *Ad hoc code signing* (`codesign -s
  -`, the placeholder identity, which .NET applies only to simulator builds) was being described
  as if it were *ad hoc distribution* (a real channel using a distribution certificate and a
  device-limited provisioning profile). The controlled terminology now defines both separately and
  says explicitly that they share an adjective and nothing else.
- **Removed a TestFlight beta review duration that had no first-party source.** §13 said beta
  review was "commonly 24 hours, reported as ranging 4-48 hours". Apple publishes no beta review
  turnaround time. The figures are gone rather than left standing, and Apple's own scoping — the
  first build added to a *group*, not each version — is now stated instead.
- **Corrected an error the previous release claimed to have already fixed.** Release 1.2.0 said
  the "closed testing requires production access" mistake had been repaired. The platform
  comparison table still carried it, saying closed and open testing "both require production
  access first". Only **open** testing does.
- **Corrected the AAPT2 long-path guidance.** The guide cited `APT2098`/`APT2261` as the long-path
  errors. Microsoft documents **`APT2264`** as the error caused by exceeding the Windows maximum
  path length; the other two are generic open/compile failures with many causes. All three are
  real `APT2`-prefixed .NET for Android codes — that prefix is the SDK's own namespace, not a
  misspelling of the tool name.
- **Corrected a Play Console navigation path.** Google renamed the top-level **Release** section to
  **Test and release**; the managed Google Play guide and its quick start both used the old name.
- **Corrected a quick start that gave the failing build command.** The Google Play quick start
  presented `dotnet publish -f net10.0-android -c Release` as "verified working", when §9 records
  that exact command failing with `XAGNM7009` from a clean tree.
- **Withdrew an unsupported claim about the first upload.** The guide said the first production
  upload "must be made manually through Play Console". Google documents no such rule — the Play
  Developer API can upload and create a draft release. What is true, and is now what the guide
  says, is that the first release configures Play App Signing and fixes your upload key.
- **Found by the adversarial pass: that withdrawal initially missed §13** — the very section every
  other page cited as its authority. Five files said Google documents no manual-only rule while
  the section they all linked to still said the upload "must be uploaded manually". Now corrected.
- **Found by the adversarial pass: a `Last Verified` note described an edit that had not been
  made.** The Google Play guide's §20 claimed the verification pass had restated §5's target API
  level. §5 still carried the old wording. §5 is now actually corrected, rather than merely
  reported as corrected — a failure mode this project is specifically supposed to guard against.
- **Found by the adversarial pass: two freshness-register rows cited the wrong source.** The
  12-tester production-access rule was cited to Google's registration-fee page, and the
  open-testing production-access rule to a page that does not contain the phrase. Both now cite
  Google's app-testing-requirements page, which does.
- **Found by the adversarial pass: three new claims were overstated** and have been pulled back to
  what the sources support — the missing-`.ipa` defect now says it *matches the mechanism* of
  dotnet/macios#20958 rather than *is* that report (the issue's reproduction differs); the
  marshal-methods default is attributed to Microsoft's .NET 10 release notes without the
  unsourced "on the MonoVM runtime" qualifier; and the `XAGNM7009` decode is presented as a decode,
  dropping two universal negatives that could not be established.

- **Found by the independent re-grade: the App Store guide's signing command could not produce an
  `.ipa`.** §10 gave `dotnet publish` with `CodesignKey` and `CodesignProvision` but **without**
  `ArchiveOnBuild=true` and `RuntimeIdentifier`, while §11 stated that command produces the package
  uploaded to App Store Connect. Microsoft documents `ArchiveOnBuild` as the property that produces
  the `.ipa`, and this repository's own ad hoc and enterprise guides had carried it all along. A
  reader following the flagship guide would have run a command that signs a build and writes no
  artefact — the exact trap the guide is written to warn about. Corrected in §10, §11 and the
  quick start.
- **Found by the independent re-grade: a false statement about this repository's own files.** The
  Google Play guide said this repository's `.gitignore` "excludes common keystore file extensions".
  It excluded `*.pfx` and nothing else relevant. Rather than soften the claim, `.gitignore` now
  actually excludes `*.keystore`, `*.jks`, `*.p12`, `*.mobileprovision`, `*.cer` and
  `keystore.properties`, and the guide now names them and adds that keeping signing material
  outside the repository is the real control.
- **Found by the independent re-grade: TestFlight's §18 still advertised the removed review
  timings**, contradicting the §13 correction made earlier in this same release.
- **Found by the independent re-grade: three section cross-references pointed at the wrong
  section.** The App Store guide sent readers to §11 (*Package*) for certificate and profile
  creation, which happens in §10 (*Sign*).
- **Found by the independent re-grade: the completeness matrix still said the Google Play testing
  tracks were undocumented**, in a table whose own rows document all three.
- **Found by the independent re-grade: the terminology table contradicted the guides.** It said the
  APK is used for "direct install and internal testing"; internal testing takes an App Bundle, as
  every Play track does.
- **Found by the independent re-grade: an evidence figure that the documented command would not
  produce.** The direct APK guide reported its verification certificate as `SHA384withRSA`, but the
  `keytool` command it prescribes generates a 2048-bit RSA key, which signs with `SHA256withRSA` on
  current JDKs. The guide no longer presents any one algorithm as *the expected result* — it now
  explains that the value follows the key size, because the useful check is that the certificate is
  yours, not which digest it names.
- **Found by a fourth pass: the Android signing command had the same defect as the iOS one.** §10
  gave the `AndroidSigningKeyStore` properties **without `-p:AndroidKeyStore=true`**, which defaults
  to `false`. Without it the signing properties are not rejected — they are silently ignored, and
  the output is the debug-signed package that same section opens by warning Google Play will
  reject. The direct APK guide had stated this rule correctly all along. Corrected in §10 and the
  Android release checklist.
- **Found by a fourth pass: four more places where an earlier fix in this release stopped short.**
  The `ArchiveOnBuild` correction had not reached the iOS release checklist, the App Store guide's
  own §17 troubleshooting row, the Apple hub, or the TestFlight guide's build note — all four still
  described signing as sufficient on its own. The "upload, not submission" correction had not
  reached the freshness register, the Apple hub, or the App Store quick start. The TestFlight
  "first build added to a *group*" correction had not reached the iOS checklist. The open testing
  "minimum permitted cap" clarification existed only in a §20 note claiming it had been made.
- **Found by a fourth pass: three references to things that do not exist in this repository** — a
  "Risk R-8", an "ADR 0015", and a JDK path said to be "verified below" where nothing below
  verified it. All three removed or replaced with what is actually true.
- **Found by a fourth pass: the root README overstated execution coverage**, saying only two
  channels had execution-verified build paths. Four builds were executed; two produced artefacts
  and two produced recorded failures. It now says which is which.
- **Found by a fourth pass: `keytool -list` was prescribed as the validation step for an APK
  signature.** It reads a keystore, not a package.
- **Found by a fifth pass: the `AndroidKeyStore=true` fix had not reached four quick starts.** The
  internal, closed, open and managed Google Play cards each said "**build and sign** the `.aab`"
  above a command containing no signing properties at all. A reader following any of those cards
  would have uploaded the debug-signed bundle those same guides say Play rejects. This is the third
  time in one release that a correct fix stopped short of a file that needed it.
- **Found by a fifth pass: `keytool -printcert -jarfile` was the wrong replacement.** It reads only
  the **v1 (JAR)** signature scheme, so on an APK signed with v2/v3 only it reports `Not a signed
  jar file` — indistinguishable from genuinely unsigned, and the same string §9 uses as evidence of
  an unsigned artefact. §14 now prescribes **`apksigner verify --print-certs`**, which reads every
  scheme; §7 and §9 carry the same correction and §9 states plainly what its original evidence does
  and does not establish.
- **Found by a fifth pass: a Play Protect claim stated harder than its source.** The guide said
  Play Protect "automatically blocks" sideloaded apps requesting certain sensitive permissions,
  naming messages and notifications. Google's wording is that it "may prevent" installation of an
  app that is unverified and uses sensitive permissions, and Google names no permission categories.
  The invented specificity is removed.
- **Found by a fifth pass: two more claims contradicting their own guides.** The ad hoc guide's §5
  described Apple Configurator as required for "the installation route this guide verifies", while
  its §18 and §20 both state no installation was executed. A §5 prerequisite cited §9 for a JDK
  detail §9 does not contain.
- **Found by a fifth pass: the same iOS archive failure carried two different execution dates** —
  2026-08-23 in the App Store guide, 2026-08-24 in the ad hoc guide. The ad hoc guide now says
  explicitly that it re-ran the App Store guide's command a day later and got the same result,
  rather than leaving two dates for one observation.
- **Found by a sixth pass: `env:` was prescribed for App Bundle builds, contradicting this
  repository's own direct APK guide.** Microsoft documents the `env:` password prefix as
  unsupported when the package format is `aab`, and the direct APK guide explains exactly that —
  yet six Play Console files, which all upload App Bundles, prescribed `env:`. They now use
  `file:`, and §10 and the Android hub explain which prefix belongs to which output format.
- **Found by a sixth pass: three more incomplete propagations.** The Play Console **Test and
  release** rename had not reached the six internal/closed/open testing navigation paths; the
  `ArchiveOnBuild` correction had not reached the ad hoc or enterprise quick starts; and the
  `AndroidKeyStore=true` correction had not reached the flagship Google Play quick start, leaving
  it the only Android card without the warning.
- **Found by a sixth pass: the unpublish path pointed at the wrong Play Console section.** It named
  *Grow > Store presence*, where listing content is edited. Unpublishing is under *Test and
  release > Setup > Advanced settings > App availability*.
- **Found by a sixth pass: `keytool -printcert` in the Android checklist's verification column.**
  Bare, it reads a certificate file, not a package — and with `-jarfile` it reads only v1
  signatures, which the direct APK guide had already ruled out. The checklist now uses
  `apksigner verify --print-certs`.
- **Found by a sixth pass: two `start-here` prerequisites pointed at information that does not
  exist** — a freshness-register entry for supported .NET versions (the register tracks vendor
  store requirements, not the .NET release train) and per-channel icon dimension "values" (no guide
  states any). Both now say plainly what this repository does not track, and link outward.
- **Found by a sixth pass: the Bundle ID was said to live in `Info.plist`.** In single-project
  MAUI it does not — `<ApplicationId>` is the only source and the build generates the rest. A
  checklist step told readers to grep a file for a value it cannot contain.
- **Found by a sixth pass: the sample declared a scope exclusion the catalogue did not record.**
  The project file said Mac App Store distribution is out of scope; the catalogue listed only
  Windows. Mac Catalyst is now recorded there, including the fact that the sample still builds it.
- **Found by a fifth pass: the terminology table's "official term" column carried a term Apple does
  not use.** "iOS App Store Package" is third-party usage; Apple writes ".ipa file". Also corrected
  a checklist step that linked to the security-model section for a keystore-creation command that
  lives elsewhere.

### Changed

- **`Last Verified` now separates two dates that were being conflated.** Every channel guide's §20
  previously carried one date covering both source re-verification and execution evidence, which
  meant re-checking a source appeared to re-date a build that had not been re-run. Each §20 now
  states **sources last verified** (which advances) and **execution evidence** (which does not,
  because the run happened when it happened) separately. This also closes the gap release 1.2.0
  left, where the register advanced to 2026-08-26 while every guide still read 2026-08-23 or -24.
- Marked the marshal-methods workaround as **inference**. That the Android build fails with
  `XAGNM7009` and succeeds with `-p:AndroidEnableMarshalMethods=false` was observed here. That the
  property is the *prescribed* remedy is not documented by Microsoft, and the guide now says so.
  `XAGNM7009` itself has no Microsoft reference page; §9 now shows how the code decodes from the
  SDK's own error-code scheme instead of implying it is documented.
- Cited [dotnet/macios#20958](https://github.com/dotnet/macios/issues/20958) for the missing-`.ipa`
  defect, and replaced the guide's approximate account of the target chain with the actual one.
- Narrowed the privacy manifest requirement to what Apple actually requires: approved reasons for
  required-reason APIs, and manifests for SDKs **on Apple's published list** — not for every
  third-party SDK. Restated the SDK floor as an **upload** requirement, Apple's own framing.
- Corrected the target API level statement: **API 35 is the currently binding floor**, with API 36
  applying from 2026-08-31 and an extension to 2026-11-01 available via Play Console's **Policy
  status** page.
- Added Apple's exceptions where the guide stated rules absolutely: D-U-N-S is not required for
  government organisations; the 180-day device removal can be pre-empted by opting in during the
  30 days before expiry; the App Bundle requirement binds new apps, not apps predating August 2021.
- Clarified that the open testing figure of 1,000 is the minimum permitted value of a tester
  **cap**, not a number of testers you must recruit.
- Qualified the `env:` prefix restriction: Microsoft states it against the deprecated singular
  `$(AndroidPackageFormat)`, and its effect on the plural `$(AndroidPackageFormats)` is
  undocumented.
- Replaced the non-existent term **"Play Review"**. Google does not brand its review with a proper
  noun; its documentation says "app review" and Play Console shows the status "In review". The
  controlled terminology now records this, and says plainly that "Play Review" is not a Google term.
- Fixed an arithmetic error in the freshness register: the API 36 deadline was described as 8 days
  from the verification date. It is 5.
- Documented, in the sample project file, that the retained `Platforms/Windows/` scaffolding is
  deliberate — kept so the sample stays diffable against unmodified `dotnet new maui` output —
  rather than an oversight contradicting the project's mobile-only scope. The same note now covers
  the rest of the template residue and records why no `global.json` is pinned.
- Replaced two bare `(§ Requirements & Freshness Register)` references with real links, and
  corrected the root README's description of the completeness matrix, which described it as
  tracking the twenty contracted sections when its eleven columns are review areas.

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
