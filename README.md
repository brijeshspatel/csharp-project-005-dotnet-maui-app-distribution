# .NET MAUI App Distribution

An authoritative, verified guide to distributing .NET MAUI mobile applications, covering
**ten channels** across Apple and Android.

Every material instruction is grounded in current, first-party Apple, Google or Microsoft
documentation, with a `Last Verified` date recorded against it. Where a command or its output is
shown as executed, it was run and its real result quoted — and where a command **cannot** produce
what its own log claims, that is documented too.

---

## Start here

| If you are... | Read |
|---|---|
| New to all of this | [Choose your distribution channel](start-here/choose-your-distribution-channel.md) |
| Deciding what to set up first | [Prerequisites overview](start-here/prerequisites-overview.md) |
| Comparing the two platforms | [iOS vs Android platform comparison](start-here/platform-comparison.md) |
| Ready to ship on iOS | [iOS end-to-end release checklist](start-here/ios-release-checklist.md) |
| Ready to ship on Android | [Android end-to-end release checklist](start-here/android-release-checklist.md) |

## Choose your platform

| Platform | Channels | Hub |
|---|---|---|
| 🍎 Apple / iOS | 4 | [`platforms/apple/`](platforms/apple/README.md) |
| 🤖 Android / Google | 6 | [`platforms/android/`](platforms/android/README.md) |

## All ten channels

Each guide follows the same fixed twenty-section contract, so the same information sits in the
same place in every one. The quick start is a condensed path for a reader who already knows the
platform.

| Channel | Platform | Guide | Quick start |
|---|---|---|---|
| App Store public release | 🍎 Apple | [Guide](platforms/apple/app-store-public-release/README.md) | [Quick start](platforms/apple/app-store-public-release/docs/quick-start-v1.0.0.md) |
| TestFlight | 🍎 Apple | [Guide](platforms/apple/testflight/README.md) | [Quick start](platforms/apple/testflight/docs/quick-start-v1.0.0.md) |
| Ad hoc distribution | 🍎 Apple | [Guide](platforms/apple/ad-hoc-distribution/README.md) | [Quick start](platforms/apple/ad-hoc-distribution/docs/quick-start-v1.0.0.md) |
| Apple Business Manager / enterprise distribution | 🍎 Apple | [Guide](platforms/apple/business-manager-and-enterprise/README.md) | [Quick start](platforms/apple/business-manager-and-enterprise/docs/quick-start-v1.0.0.md) |
| Google Play public release | 🤖 Android | [Guide](platforms/android/google-play-public-release/README.md) | [Quick start](platforms/android/google-play-public-release/docs/quick-start-v1.0.0.md) |
| Google Play internal testing | 🤖 Android | [Guide](platforms/android/google-play-internal-testing/README.md) | [Quick start](platforms/android/google-play-internal-testing/docs/quick-start-v1.0.0.md) |
| Google Play closed testing | 🤖 Android | [Guide](platforms/android/google-play-closed-testing/README.md) | [Quick start](platforms/android/google-play-closed-testing/docs/quick-start-v1.0.0.md) |
| Google Play open testing | 🤖 Android | [Guide](platforms/android/google-play-open-testing/README.md) | [Quick start](platforms/android/google-play-open-testing/docs/quick-start-v1.0.0.md) |
| Managed Google Play / Android Enterprise distribution | 🤖 Android | [Guide](platforms/android/managed-google-play-enterprise/README.md) | [Quick start](platforms/android/managed-google-play-enterprise/docs/quick-start-v1.0.0.md) |
| Direct APK distribution | 🤖 Android | [Guide](platforms/android/direct-apk-distribution/README.md) | [Quick start](platforms/android/direct-apk-distribution/docs/quick-start-v1.0.0.md) |

## Reference

| Document | What it holds |
|---|---|
| [Channel catalogue](docs/maui-distribution-channel-catalogue-v1.0.0.md) | Every channel in scope, and the twenty-section contract each guide follows |
| [Controlled terminology](docs/reference/terminology-v1.0.1.md) | One term per concept, using each vendor's own official term |
| [Channel completeness matrix](docs/reference/channel-completeness-matrix-v1.0.1.md) | Which sections each channel guide actually completed |
| [Requirements and freshness register](docs/reference/requirements-freshness-register-v1.0.0.md) | Every time-sensitive requirement, its source, and when to re-check it |

## Verification

Nothing here is reported as done because it was written. These checks are run, and their output
is quoted in the record that claims it.

| Check | Grades |
|---|---|
| `python tools/anchor_check.py "**/*.md"` | That every in-repository heading anchor resolves |
| `python tools/nav_docs_check.py` | Frontmatter of the navigation documents no other checker reaches, and that this table of contents lists every catalogued channel |
| `python tools/channel_completeness_check.py <matrix>` | That the completeness matrix is well formed and complete |
| `python tools/freshness_register_check.py <register>` | That every freshness row carries its verification evidence |
| `python tools/link_check.py "<glob>"` | That external sources are reachable |

**Two warnings a reader should carry into their own build**, both found by execution here:

- `dotnet publish -f net10.0-ios -c Release` **writes no `.ipa`** while printing that it did, and
  exiting 0 with 0 warnings. **List the file; never read the log.**
- `dotnet publish -f net10.0-android -c Release` **fails from a clean tree** with `XAGNM7009`.
  Adding `-p:AndroidEnableMarshalMethods=false` makes it succeed.

## Scope

Microsoft and Windows application distribution is **out of scope** for this phase. The objective
is mobile application distribution; Windows distribution may be added later if there is a clear
need.

Most channels here are **documented, not demonstrated** — each guide says which it is in its own
section 18. Only Google Play public release and direct APK distribution have execution-verified
build paths, and no channel has a verified upload, review or installation.

## Licence

MIT — see [`LICENSE`](LICENSE).
