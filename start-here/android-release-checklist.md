---
doc_id: maui-dist-android-release-checklist
title: Android End-to-End Release Checklist
type: guide
version: 1.1.1
status: active
created: 2026-08-23
updated: 2026-08-25
owner: Brijesh Patel
change_summary: Removes emoji from the section headings so every internal anchor resolves. An emoji in a heading is dropped by the anchor rule and leaves the space beside it, which turned every #7-security-model style link into a broken one. No procedural content, section name or ordering changed.
---

# Android End-to-End Release Checklist

Written using ASD-STE100 principles. This is an authoritative execution path, not a summary —
follow it in order. Each step names its dependency on the step before it. Full detail and
official sources live in the linked guide section; this checklist does not repeat them.

1. ✅ **Register a Google Play Console developer account** (one-time US $25 fee) and complete
   identity verification. *Depends on: nothing.*
   [Details](../platforms/android/google-play-public-release/README.md#4-eligibility)
2. ⚠️ **Decision gate: does the 14-day closed-test requirement apply?** If this is a personal
   account created after 2023-11-13, plan for a 14-day closed test with 12 opted-in testers
   before production access — this affects your timeline from here on, not just at the end.
   *Depends on: step 1.* [Details](../platforms/android/google-play-public-release/README.md#4-eligibility)
3. ✅ **Confirm build tooling.** Target API level 35 now, rising to API level 36 from
   2026-08-31 — check the current floor before building. *Depends on: nothing.*
   [Details](../platforms/android/google-play-public-release/README.md#5-prerequisites)
4. **Set application identity.** Package name as the Application ID property. *Depends on:
   nothing; fix this before creating the app listing so they match.*
   [Details](../platforms/android/google-play-public-release/README.md#8-application-preparation)
5. **Set versioning.** Version name and version code, both higher than any prior release.
   *Depends on: nothing for a first release.*
   [Details](../platforms/android/google-play-public-release/README.md#8-application-preparation)
6. **Build.** `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false`,
   run **at your project's real path**, not a temporary copy — a sufficiently long path can fail
   this step (`APT2098`/`APT2261` "failed to open file"). ⚠️ **Without
   `-p:AndroidEnableMarshalMethods=false` this step fails** on the verified toolchain, with
   `XAGNM7009`. *Depends on: steps 3-5.*
   [Details](../platforms/android/google-play-public-release/README.md#9-build)
7. ⚠️ **STOP — VERIFY BEFORE CONTINUING.** Confirm the `.aab` exists by listing
   `bin/Release/net10.0-android/publish/`. Do not accept the build log as proof. If step 6 failed
   with `XAGNM7009`, confirm the marshal-methods property is set and `obj/` was clean. If it
   failed with a `javac.exe` error and no further detail, retry once with `-v:detailed` before
   assuming a real defect. If it failed with `APT2098`/`APT2261`, shorten the project path or
   enable Windows long-path support before retrying.
8. 🔐 **Create and protect an upload keystore.** Never commit it or its passwords to source
   control. *Depends on: nothing; do this before signing a real release build.*
   [Details](../platforms/android/google-play-public-release/README.md#7-security-model)
9. 🔐 **Sign for real release**, using `-p:AndroidSigningKeyStore` and the related signing
   properties, referencing the keystore from step 8. *Depends on: steps 6 and 8.*
   [Details](../platforms/android/google-play-public-release/README.md#10-sign)
10. 📦 **Package.** Confirm the signed `.aab` exists — Google Play requires the App Bundle
    format, not the `.apk`. *Depends on: step 9.*
    [Details](../platforms/android/google-play-public-release/README.md#11-package)
11. **Create the app listing** in Play Console: name, default language, category, free/paid
    status. *Depends on: step 4 (package name must already be fixed).*
    [Details](../platforms/android/google-play-public-release/README.md#12-configure-distribution-platform)
12. ⚠️ **Decision gate: store readiness.** Complete the store listing, content rating
    questionnaire, and Data safety declaration — Play Console blocks production publishing with
    any of these incomplete. *Depends on: step 11.*
    [Details](../platforms/android/google-play-public-release/README.md#12-configure-distribution-platform)
13. 🧪 **Complete the closed test from step 2, if it applies**, before attempting production
    access. *Depends on: step 2's gate and steps 6-10 (you need a real signed build to test
    with).*
14. 🚀 **Upload the `.aab` manually** for the first release — this establishes the signing-key
    relationship Google uses for every future release. *Depends on: steps 10, 12, and 13 where
    applicable.* [Details](../platforms/android/google-play-public-release/README.md#13-deploy)
15. ✅ **Validate.** Confirm Play Console's pre-launch checks pass and the release reaches
    "Ready to publish." *Depends on: step 14.*
    [Details](../platforms/android/google-play-public-release/README.md#14-validate)
16. 🚀 **Submit for Play Review.** *Depends on: step 15.*
17. **Handle review outcome.** If rejected, correct the named policy issue and return to the
    relevant earlier step (commonly step 5, 6 or 12); if approved, proceed to step 18.
    [Details](../platforms/android/google-play-public-release/README.md#17-troubleshooting)
18. 🚀 **Release.** The app becomes publicly available. *Depends on: step 17's approval.*
19. ✅ **Post-release verification.** Confirm the app is downloadable from the live Play Store
    listing and installs correctly on a real device.
20. 🔄 **Plan the next update.** Increase the version code before repeating from step 6 for any
    future release. [Details](../platforms/android/google-play-public-release/README.md#15-update)
