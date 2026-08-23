---
doc_id: maui-dist-ios-release-checklist
title: iOS End-to-End Release Checklist
type: guide
version: 1.1.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Corrects step 7. The iOS build produces no .ipa without code signing. Written using ASD-STE100 principles.
---

# 🍎 iOS End-to-End Release Checklist

Written using ASD-STE100 principles. This is an authoritative execution path, not a summary —
follow it in order. Each step names its dependency on the step before it. Full detail and
official sources live in the linked guide section; this checklist does not repeat them.

1. ✅ **Confirm eligibility.** Active Apple Developer Program membership. *Depends on: nothing.*
   [Details](../platforms/apple/app-store-public-release/README.md#4-eligibility)
2. ✅ **Confirm build tooling.** iOS 26 SDK / Xcode-26-equivalent workload installed — required
   for submissions from 2026-04-28. *Depends on: step 1 (you need the account to check current
   requirements against).* [Details](../platforms/apple/app-store-public-release/README.md#5-prerequisites)
3. **Set application identity.** Bundle ID as the Application ID property, matching
   `Info.plist`. *Depends on: nothing; do this before creating any Apple-side identity so they
   match.* [Details](../platforms/apple/app-store-public-release/README.md#8-application-preparation)
4. 🔐 **Create a distribution certificate.** *Depends on: step 1 (Apple Developer Program
   membership).* [Details](../platforms/apple/app-store-public-release/README.md#10-sign)
5. 🔐 **Create an App ID and provisioning profile**, matching the Bundle ID from step 3 and the
   certificate from step 4. *Depends on: steps 3 and 4.*
   [Details](../platforms/apple/app-store-public-release/README.md#10-sign)
6. ⚠️ **STOP — VERIFY BEFORE CONTINUING.** Back up the certificate's private key and record where
   the provisioning profile lives. Losing either after this point means revoking and re-creating
   before any further step can complete. *Depends on: steps 4 and 5.*
7. **Build.** `dotnet publish -f net10.0-ios -c Release`. Verified by execution on Windows:
   it compiles the managed and AOT output. ⚠️ **It produces no `.ipa`**, although it exits 0 and
   prints a message claiming it did. Signing is a prerequisite of a package here, not a later
   refinement. *Depends on: step 3.*
   [Details](../platforms/apple/app-store-public-release/README.md#9-build)
8. 🔐 **Sign for real distribution**, using `-p:CodesignKey`/`-p:CodesignProvision` naming the
   certificate and profile from steps 4-5. *Depends on: steps 5 and 7.*
   [Details](../platforms/apple/app-store-public-release/README.md#10-sign)
9. 📦 **Package.** Confirm the signed `.ipa` exists at the expected output path — **list the
   file; do not read the build log**, which reports a package even when none was written.
   *Depends on: step 8.*
   [Details](../platforms/apple/app-store-public-release/README.md#11-package)
10. **Create an App Store Connect app record**: name, primary language, Bundle ID, SKU.
    *Depends on: step 3 (Bundle ID must already be fixed).*
    [Details](../platforms/apple/app-store-public-release/README.md#12-configure-distribution-platform)
11. 🚀 **Upload the signed build** via Visual Studio's Distribute dialog or Transporter, using an
    app-specific password. *Depends on: steps 9 and 10.*
    [Details](../platforms/apple/app-store-public-release/README.md#13-deploy)
12. ✅ **Validate the upload.** Confirm the build reaches "Ready to Submit" in App Store Connect.
    *Depends on: step 11.* [Details](../platforms/apple/app-store-public-release/README.md#14-validate)
13. 🧪 **Internal TestFlight testing** (recommended before public submission): add up to 100
    internal testers, available within minutes, no review. *Depends on: step 12.*
    [Details](../platforms/apple/testflight/README.md#13-deploy)
14. 🧪 **External TestFlight testing** (where used): invite up to 10,000 testers; the first build
    per version needs Apple beta review. *Depends on: step 13, or step 12 directly if skipping
    internal testing.* [Details](../platforms/apple/testflight/README.md#13-deploy)
15. ⚠️ **Decision gate: ready for public release?** Confirm privacy manifest completeness, App
    Privacy details, age rating, and store listing metadata are all complete. Do not proceed to
    step 16 with any of these incomplete — App Review will reject the submission.
    [Details](../platforms/apple/app-store-public-release/README.md#5-prerequisites)
16. 🚀 **Submit for App Review.** *Depends on: step 15's gate passing.*
    [Details](../platforms/apple/app-store-public-release/README.md#13-deploy)
17. **Handle review outcome.** If rejected, correct the named issue and return to the relevant
    earlier step (commonly step 3, 7 or 15); if approved, proceed to step 18.
    [Details](../platforms/apple/app-store-public-release/README.md#17-troubleshooting)
18. 🚀 **Release.** The app becomes publicly available. *Depends on: step 17's approval.*
19. ✅ **Post-release verification.** Confirm the app is downloadable from the live App Store
    listing and installs correctly on a real device.
20. 🔄 **Plan the next update.** Increase both version and build number before repeating from
    step 7 for any future release. [Details](../platforms/apple/app-store-public-release/README.md#15-update)
