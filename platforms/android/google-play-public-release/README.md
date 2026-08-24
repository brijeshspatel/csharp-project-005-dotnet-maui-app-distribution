---
doc_id: maui-dist-channel-google-play
title: Google Play — Public Release
type: guide
version: 1.1.1
status: active
created: 2026-08-23
updated: 2026-08-25
owner: Brijesh Patel
change_summary: Removes emoji from the section headings so every internal anchor resolves. An emoji in a heading is dropped by the anchor rule and leaves the space beside it, which turned every #7-security-model style link into a broken one. No procedural content, section name or ordering changed.
---

# Google Play — Public Release

Written using ASD-STE100 principles.

## 1. What This Channel Is

Google Play is Android's primary public application marketplace. A public release through this
channel makes your app discoverable and installable by any user with a Google Account, in the
countries and device categories you select. Google reviews every submission.

## 2. When to Use It

Use this channel when your app is ready for the general public, and you want the widest possible
reach on Android.

## 3. When Not to Use It

Do not use this channel for testing — use Google Play's internal, closed or open testing tracks
first (not yet documented in this repository; see the channel catalogue). Do not use it for an
app restricted to your own organisation's devices — that is managed/enterprise distribution (not
yet documented).

## 4. Eligibility

You need a **Google Play Console developer account**: a **one-time, non-refundable US $25**
registration fee, plus identity verification. **If your personal account was created after
2023-11-13, Google requires a 14-day closed test with at least 12 opted-in testers before
granting production access** — this applies before you can use this channel at all, so confirm
your account's creation date and status first. **Last verified: 2026-08-23.**

## 5. Prerequisites

- A verified Google Play Console developer account (§4), including the closed-test requirement
  where it applies.
- A stable, permanent **package name** (Application ID) in reverse-DNS form.
- App icons, a feature graphic and screenshots meeting Google Play's current published sizes.
- A publicly accessible privacy policy URL.
- A completed **Data safety** declaration describing what data your app collects and why.
- **Your build must target the current required API level.** As of this guide's Last Verified
  date, Google requires API level 35 now, rising to **API level 36 from 2026-08-31** — eight days
  after this guide was verified. Confirm the current floor before you build (§17).

## 6. How to Obtain the Prerequisites

Register at Google Play Console, pay the one-time fee, and complete identity verification before
creating your first app listing. If the closed-test requirement in §4 applies to your account,
plan for at least 14 days between your first internal build and requesting production access.

## 7. Security Model

Google Play distinguishes an **upload key** (signs the App Bundle you upload) from an **app
signing key** (signs what actually reaches devices). With **Play App Signing** — the default and
recommended path — Google holds the app signing key, and you keep only the upload key; losing the
upload key is recoverable through Play Console's own key-reset process. Opting out of Play App
Signing means you alone hold the signing key permanently, with no Google-side recovery if it is
lost.

## 8. Application Preparation

Set your package name as the **Application ID** property in your .NET MAUI project. Set your
version name and version code; both must increase on every release. Confirm your target API level
against §5's current requirement before building for release.

## 9. Build

**Verified by execution against this repository's own sample application**
(`sample/DistributionSample`), 2026-08-23, **at this repository's own real path** — not only a
scratch fixture, because an earlier specification-review test found this exact command can fail
from a sufficiently long Windows path (AAPT2 "failed to open file"):

```
dotnet publish -f net10.0-android -c Release
```

⚠️ **WARNING — that command alone does not complete on this toolchain.** Re-verified from a
fully clean tree, with `bin/` and `obj/` both removed, it fails with:

```
error XAGNM7009: System.InvalidOperationException: Internal error: missing native code generation
state for architecture 'Arm64'
```

and writes no `.aab`. This was reproduced on two consecutive clean attempts, run sequentially and
**not** under concurrent load, which rules out resource contention as the cause.

**The command that completes here disables marshal methods**, which .NET 10 enables by default and
which Microsoft documents as the mitigation when marshal methods misbehave:

```
dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
```

This exits 0 and writes these artefacts to `bin/Release/net10.0-android/publish/`:

| Artefact | Size | Use |
|---|---|---|
| `com.companyname.distributionsample.aab` | 28,344,696 bytes | unsigned App Bundle |
| `com.companyname.distributionsample-Signed.aab` | 28,478,415 bytes | debug-signed App Bundle |
| `com.companyname.distributionsample-Signed.apk` | 29,058,372 bytes | debug-signed APK, local testing only |

**The sizes are quoted because each file was confirmed on disk, not because a log said so.** A
.NET publish can report success and name an artefact it never wrote — this repository's iOS guide
documents exactly that behaviour for the same sample application, in its
[§9](../../apple/app-store-public-release/README.md#9-build). **List the file. Never trust the
message.**

**Google Play requires the App Bundle (`.aab`) format**, not the `.apk`, for new app submissions.

**Disabling marshal methods is a mitigation, not a default to adopt blindly.** Marshal methods are
a startup-performance optimisation. Disabling them is the documented response to a marshal-method
fault, and it is what makes this build complete here; it is not a recommendation for a project
whose build already succeeds without it. Retest with the property removed after any Android
workload update.

**One further trap, observed here.** Setting `AndroidEnableMarshalMethods=false` against a `obj/`
directory produced with marshal methods **enabled** fails differently again, with R8 reporting
`Type android.runtime.JavaProxyThrowable is defined multiple times`. That is stale intermediate
state, not a property fault. Clean `obj/` when you change this property.

## 10. Sign

The build in §9 produces a debug-signed package alongside the unsigned one when no explicit
signing configuration is supplied. **A debug-signed bundle is for local testing only and Google
Play will reject it.** For a real release, configure signing explicitly, referencing your own
upload keystore:

```
dotnet publish -f net10.0-android -c Release ^
  -p:AndroidSigningKeyStore=<path-to-keystore> ^
  -p:AndroidSigningKeyAlias=<key-alias> ^
  -p:AndroidSigningKeyPass=<key-password> ^
  -p:AndroidSigningStorePass=<store-password>
```

**Never commit a keystore or its passwords to source control.** Use a secrets manager or a CI
secret store; this repository's own `.gitignore` excludes common keystore file extensions.

## 11. Package

The `.aab` produced in §9-§10 is the artefact uploaded to Google Play Console. Keep the matching
`.apk` only for local device testing — it is not the upload artefact for this channel.

## 12. Configure Distribution Platform

Create an app listing in Google Play Console: app name, default language, app or game category,
and free/paid status. Complete the store listing, content rating questionnaire, and Data safety
declaration before your first release can reach production — Play Console will not allow
publishing to production with these incomplete.

## 13. Deploy

For a brand-new app, the first `.aab` **must be uploaded manually** through Play Console's own
release flow — this is what establishes the signing key relationship for every future release.
Subsequent releases may use `dotnet publish` plus Play Console's upload, or the Google Play
Developer API for automation (not covered by this guide's manual-first scope).

## 14. Validate

Play Console runs automated pre-launch checks after upload (crash detection, basic
compatibility). Confirm the release reaches "Ready to publish" before submitting to review, and
resolve any pre-launch warnings first.

## 15. Update

Increase the version code (and version name) and repeat §9-§14. Google Play rejects an upload
whose version code does not exceed the previous release.

## 16. Revoke / Withdraw / Retire

Unpublish an app from its Play Console listing (**Grow > Store presence > Main store listing**
status controls, or the dedicated unpublish action). This stops new installs; it does not remove
the app from devices that already installed it. There is no equivalent to revoking a certificate
here unless you manage your own signing key outside Play App Signing.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| `dotnet publish -f net10.0-android -c Release` fails with `APT2098`/`APT2261` "failed to open file" | Project path is too long for the Android resource compiler on Windows | Compare your project's full path length against a known-short path | Move the project closer to a drive root, or enable Windows long-path support |
| Same command fails with `javac.exe exited with code 1` and no further detail | May be transient resource contention from concurrent processes | Re-run with `-v:detailed` and inspect the actual javac output | Retry; if it recurs identically, inspect the detailed log for a real compiler error |
| `error XAGNM7009: ... missing native code generation state for architecture 'Arm64'` | Marshal methods, enabled by default in .NET 10, fail during native code generation | Re-run from a clean tree; it reproduces | Add `-p:AndroidEnableMarshalMethods=false`, per §9 |
| R8 reports `Type android.runtime.JavaProxyThrowable is defined multiple times` | `AndroidEnableMarshalMethods` was changed against a stale `obj/` | Check whether the property changed since the last build | Delete `obj/` and rebuild, per §9 |
| Publish reports success but no `.aab` is on disk | The artefact was never written; the message is not proof | List `bin/Release/net10.0-android/publish/` | Treat as a failure and read the full log. See the iOS guide's §9 for the same class of defect |
| Upload rejected for target API level | Build targets an API level below Google Play's current floor | Check the current floor in the register (§ Requirements & Freshness Register) | Update `TargetFramework`/Android API level and rebuild |
| Upload rejected: signing key mismatch | Uploaded `.aab` was signed with a different key than the app's first release | Confirm which upload key Play Console expects for this app | Use the correct upload key, or use Play Console's key-reset process if it was lost |

## 18. Limitations

This guide's build step (§9) was verified by execution at this repository's own real path, on
Windows, from a clean tree, confirming Risk R-8 (path length) does not affect this specific path.
**It required `-p:AndroidEnableMarshalMethods=false`; the command without that property does not
complete on this toolchain.** The artefacts were confirmed on disk by listing them, not inferred
from the build log. Real upload key generation and the actual Play Console submission flow were
not executed in this run — they require a real, verified Google Play Console account. The API-level floor in §5 changes on a
published schedule (§ Requirements & Freshness Register) and must be re-checked, not assumed
current, after 2026-08-31.

## 19. Official Sources

- [Publish a .NET MAUI Android app for Google Play distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-google-play?view=net-maui-10.0)
- [About Android App Bundles — Android Developers](https://developer.android.com/guide/app-bundle)
- [Get started with Play Console — Play Console Help](https://support.google.com/googleplay/android-developer/answer/6112435)
- [Target API level requirements for Google Play apps — Play Console Help](https://support.google.com/googleplay/android-developer/answer/11926878)

## 20. Last Verified

2026-08-23 — build claims verified by execution against this repository's own sample application,
at its real repository path, from a clean tree, with the produced artefacts confirmed on disk.
Signing with a real upload key and the Play Console submission flow are **not** execution-verified.
All other claims were verified against the sources in §19 on the same date.
