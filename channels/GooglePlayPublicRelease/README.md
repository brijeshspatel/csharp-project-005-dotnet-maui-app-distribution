---
doc_id: maui-dist-channel-google-play
title: Google Play — Public Release
type: guide
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial channel guide. Written using ASD-STE100 principles.
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

This succeeded, producing both `com.companyname.distributionsample.aab` (unsigned) and
`com.companyname.distributionsample-Signed.aab`/`.apk` (debug-signed) under
`bin/Release/net10.0-android/publish/`. **Google Play requires the App Bundle (`.aab`) format**,
not the `.apk`, for new app submissions.

**A transient failure was observed and is worth naming.** The first attempt at this exact command,
run while other work was executing concurrently on this machine, failed with `javac.exe exited
with code 1` and no further detail. A clean retry with `-v:detailed` succeeded with zero errors.
If this command fails for you with the same message, retry before assuming a real defect —
resource contention during compilation is a plausible, ordinary cause; a path-length failure (the
issue this repository specifically tested for) reports `APT2098`/`APT2261`, a different and more
specific error.

## 10. Sign

The build in §9 produces a debug-signed package by default when no explicit signing
configuration is supplied. For a real release, configure signing explicitly, referencing your own
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
| Same command fails with `javac.exe exited with code 1` and no further detail | Often transient — resource contention from concurrent processes | Re-run with `-v:detailed` and inspect the actual javac output | Retry; if it recurs identically, inspect the detailed log for a real compiler error |
| Upload rejected for target API level | Build targets an API level below Google Play's current floor | Check the current floor in the register (§ Requirements & Freshness Register) | Update `TargetFramework`/Android API level and rebuild |
| Upload rejected: signing key mismatch | Uploaded `.aab` was signed with a different key than the app's first release | Confirm which upload key Play Console expects for this app | Use the correct upload key, or use Play Console's key-reset process if it was lost |

## 18. Limitations

This guide's build step (§9) was verified by execution at this repository's own real path, on
Windows, confirming Risk R-8 (path length) does not affect this specific path. Real upload key
generation and the actual Play Console submission flow were not executed in this run — they
require a real, verified Google Play Console account. The API-level floor in §5 changes on a
published schedule (§ Requirements & Freshness Register) and must be re-checked, not assumed
current, after 2026-08-31.

## 19. Official Sources

- [Publish a .NET MAUI Android app for Google Play distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-google-play?view=net-maui-10.0)
- [About Android App Bundles — Android Developers](https://developer.android.com/guide/app-bundle)
- [Get started with Play Console — Play Console Help](https://support.google.com/googleplay/android-developer/answer/6112435)
- [Target API level requirements for Google Play apps — Play Console Help](https://support.google.com/googleplay/android-developer/answer/11926878)

## 20. Last Verified

2026-08-23 — build claims verified by execution against this repository's own sample application,
at its real repository path; all other claims verified against the sources in §19 on the same
date.
