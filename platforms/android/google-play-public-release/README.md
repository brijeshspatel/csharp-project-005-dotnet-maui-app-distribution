# Google Play — Public Release

## 1. What This Channel Is

Google Play is Android's primary public application marketplace. A public release through this
channel makes your app discoverable and installable by any user with a Google Account, in the
countries and device categories you select. Google reviews every submission.

## 2. When to Use It

Use this channel when your app is ready for the general public, and you want the widest possible
reach on Android.

## 3. When Not to Use It

Do not use this channel for testing — use Google Play's internal, closed or open testing tracks
first: [internal](../google-play-internal-testing/README.md),
[closed](../google-play-closed-testing/README.md) or
[open](../google-play-open-testing/README.md). Do not use it for an app restricted to your own
organisation's devices — that is
[managed Google Play](../managed-google-play-enterprise/README.md).

## 4. Eligibility

You need a **Google Play Console developer account**: a **one-time, non-refundable US $25**
registration fee, plus identity verification. **If your personal account was created after
2023-11-13, Google requires a 14-day closed test with at least 12 opted-in testers before
granting production access** — this applies before you can use this channel at all, so confirm
your account's creation date and status first. **Last verified: 2026-08-26.**

## 5. Prerequisites

- A verified Google Play Console developer account (§4), including the closed-test requirement
  where it applies.
- A stable, permanent **package name** (Application ID) in reverse-DNS form.
- App icons, a feature graphic and screenshots meeting Google Play's current published sizes.
- A publicly accessible privacy policy URL.
- A completed **Data safety** declaration describing what data your app collects and why.
- **Your build must target the current required API level.** As of this guide's verification date,
  **API 35 is the binding floor, and API 36 is required for new apps and updates from
  2026-08-31.** An extension to **2026-11-01** can be requested through Play Console's **Policy
  status** page. Google raises this floor every year and an app below it cannot be submitted, so
  confirm the current requirement before you build rather than trusting any fixed number,
  including this one (§17). Wear OS and Android Automotive sit at API 35; Android TV and Android
  XR at API 34.

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
scratch fixture, because an earlier specification-review test saw this exact command fail from a
sufficiently long Windows path, reporting an AAPT2 "failed to open file". That symptom has several
possible causes and path length is only one of them (§17) — the reason to build at the real path
is that a short scratch path cannot reproduce the condition either way:

```
dotnet publish -f net10.0-android -c Release
```

**WARNING — that command alone does not complete on this toolchain.** Re-verified from a
fully clean tree, with `bin/` and `obj/` both removed, it fails with:

```
error XAGNM7009: System.InvalidOperationException: Internal error: missing native code generation
state for architecture 'Arm64'
```

and writes no `.aab`. This was reproduced on two consecutive clean attempts, run sequentially and
**not** under concurrent load, which rules out resource contention as the cause.

**What `XAGNM7009` appears to be.** .NET for Android composes unhandled-exception codes as
`XA<TaskPrefix><Number>`, where `7009` denotes an `InvalidOperationException` — the same pattern is
visible in the documented `XAGJS7009` from the `GenerateJavaStubs` task. On that reading `GNM`
points to the marshal-methods source generator, which matches both the failing step and the
"missing native code generation state" text quoted above.

**Treat that as a decode, not a citation.** `XAGNM7009` is absent from Microsoft's published
error-message index, so there is no reference page to check it against, and the `GNM` prefix
expansion is inferred from the naming scheme rather than read off a first-party prefix table.

**The command that completes here disables marshal methods.** Microsoft's .NET 10 release notes
say marshal methods are enabled by default in .NET 10, having been off by default in .NET 9 — note
that the build-properties reference page still says "False by default", and is stale against those
notes:

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

**Disabling marshal methods is a mitigation, not a default to adopt blindly.** Microsoft describes
marshal methods as "an app startup optimization which uses native entry points for Java `native`
method registration", so turning them off is a genuine performance trade, not a free switch.

**Be clear about what is established here and what is inferred.** That this build fails with
`XAGNM7009` and succeeds with `-p:AndroidEnableMarshalMethods=false` was observed by execution.
That the property is *the* prescribed remedy for this error is **inference** — reasonable, because
the failing task is the marshal-methods generator and the property stops it running, but Microsoft
does not document that link. Treat it as a working mitigation for this toolchain, not a
recommendation for a project whose build already succeeds without it, and retest with the property
removed after any Android workload update.

**One further trap, observed here.** Setting `AndroidEnableMarshalMethods=false` against a `obj/`
directory produced with marshal methods **enabled** fails differently again, with R8 reporting
`Type android.runtime.JavaProxyThrowable is defined multiple times`. That is stale intermediate
state, not a property fault. Clean `obj/` when you change this property.

## 10. Sign

The build in §9 produces a debug-signed package alongside the unsigned one when no explicit
signing configuration is supplied. **A debug-signed bundle is for local testing only and Google
Play will reject it.** For a real release, configure signing explicitly, referencing your own
upload keystore.

**`AndroidKeyStore=true` is the property that switches custom signing on, and it defaults to
`false`.** Supplying the keystore path, alias and passwords *without* it does not error — the
properties are simply ignored, and you get the same debug-signed package this section is warning
you about. An earlier revision of this command omitted it. The marshal-methods property from §9 is
also carried here, because this build is subject to the same clean-tree failure:

```
dotnet publish -f net10.0-android -c Release ^
  -p:AndroidEnableMarshalMethods=false ^
  -p:AndroidKeyStore=true ^
  -p:AndroidSigningKeyStore=<path-to-keystore> ^
  -p:AndroidSigningKeyAlias=<key-alias> ^
  -p:AndroidSigningKeyPass=env:<var-holding-key-password> ^
  -p:AndroidSigningStorePass=env:<var-holding-store-password>
```

**Never commit a keystore or its passwords to source control.** Use a secrets manager or a CI
secret store. This repository's own [`.gitignore`](../../../.gitignore) excludes `*.keystore`,
`*.jks`, `*.p12`, `*.pfx` and `keystore.properties`, along with the Apple equivalents — but treat
that as a backstop, not a control. **The reliable answer is to keep signing material outside the
repository entirely**, where no ignore rule has to be correct for it to stay out.

## 11. Package

The `.aab` produced in §9-§10 is the artefact uploaded to Google Play Console. Keep the matching
`.apk` only for local device testing — it is not the upload artefact for this channel.

## 12. Configure Distribution Platform

Create an app listing in Google Play Console: app name, default language, app or game category,
and free/paid status. Complete the store listing, content rating questionnaire, and Data safety
declaration before your first release can reach production — Play Console will not allow
publishing to production with these incomplete.

## 13. Deploy

**Make the first release deliberately — but not because a rule forces you to.** An earlier revision
of this guide said the first `.aab` "must be uploaded manually" through Play Console. **Google
documents no such requirement.** The Play Developer API supports uploading a bundle and creating a
draft release, and no first-party page restricts the first upload to the console.

What *is* true is why the first release matters: it configures **Play App Signing**, and the key
you sign it with becomes your **upload key** for every release afterwards. That is an
effectively irreversible step, so many teams do the first one by hand to slow themselves down at
it. Treat that as sound practice, not as a platform constraint.

Later releases may use `dotnet publish` plus a Play Console upload, or the Play Developer API for
automation. Automating that pipeline is outside this guide's scope.

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
| `dotnet publish -f net10.0-android -c Release` fails with `APT2264`, or with `APT2098` "failed to open file" / `APT2261` "file failed to compile" | Project path is too long for the Android resource compiler on Windows. **`APT2264` is the only one of these Microsoft ties to path length**, and even there the wording is "generally caused by", not exclusively; `APT2098` and `APT2261` are generic open/compile failures with many possible causes, of which a long path is one | Compare your project's full path length against a known-short path | Move the project closer to a drive root, enable Windows long-path support, or redirect `$(BaseIntermediateOutputPath)` nearer the drive root via `Directory.Build.props` |
| Same command fails with `javac.exe exited with code 1` and no further detail | May be transient resource contention from concurrent processes | Re-run with `-v:detailed` and inspect the actual javac output | Retry; if it recurs identically, inspect the detailed log for a real compiler error |
| `error XAGNM7009: ... missing native code generation state for architecture 'Arm64'` | Marshal methods, enabled by default in .NET 10, fail during native code generation | Re-run from a clean tree; it reproduces | Add `-p:AndroidEnableMarshalMethods=false`, per §9 |
| R8 reports `Type android.runtime.JavaProxyThrowable is defined multiple times` | `AndroidEnableMarshalMethods` was changed against a stale `obj/` | Check whether the property changed since the last build | Delete `obj/` and rebuild, per §9 |
| Publish reports success but no `.aab` is on disk | The artefact was never written; the message is not proof | List `bin/Release/net10.0-android/publish/` | Treat as a failure and read the full log. See the iOS guide's §9 for the same class of defect |
| Upload rejected for target API level | Build targets an API level below Google Play's current floor | Check the current floor in the [Requirements & Freshness Register](../../../docs/reference/requirements-freshness-register.md) | Update `TargetFramework`/Android API level and rebuild |
| Upload rejected: signing key mismatch | Uploaded `.aab` was signed with a different key than the app's first release | Confirm which upload key Play Console expects for this app | Use the correct upload key, or use Play Console's key-reset process if it was lost |

## 18. Limitations

This guide's build step (§9) was verified by execution at this repository's own real path, on
Windows, from a clean tree, confirming that path length does not affect this specific path.
**It required `-p:AndroidEnableMarshalMethods=false`; the command without that property does not
complete on this toolchain.** The artefacts were confirmed on disk by listing them, not inferred
from the build log. Real upload key generation and the actual Play Console submission flow were
not executed in this run — they require a real, verified Google Play Console account. The API-level floor in §5 changes on a
published schedule (see the
[Requirements & Freshness Register](../../../docs/reference/requirements-freshness-register.md))
and must be re-checked, not assumed
current, after 2026-08-31.

## 19. Official Sources

- [Publish a .NET MAUI Android app for Google Play distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-google-play?view=net-maui-10.0)
- [About Android App Bundles — Android Developers](https://developer.android.com/guide/app-bundle)
- [Get started with Play Console — Play Console Help](https://support.google.com/googleplay/android-developer/answer/6112435)
- [Target API level requirements for Google Play apps — Play Console Help](https://support.google.com/googleplay/android-developer/answer/11926878)

## 20. Last Verified

This section separates two different dates, because they mean different things and only one of
them can advance.

**Sources last verified: 2026-08-26.** Every claim resting on §19's sources was re-checked on that
date. That pass restated §5's target API level (API 35 is the currently binding floor; API 36
applies from 2026-08-31, extendable to 2026-11-01 via Play Console's Policy status page),
corrected §17's AAPT2 error-code guidance, and marked the marshal-methods workaround in §9 as
**observed but not documented** by Microsoft as the remedy for `XAGNM7009`.

**Execution evidence: 2026-08-23.** Build claims verified by execution against this repository's
own sample application, at its real repository path, from a clean tree, with the produced
artefacts confirmed on disk. **That date does not advance when sources are re-verified** — the run
happened when it happened. Signing with a real upload key and the Play Console submission flow are
**not** execution-verified.
