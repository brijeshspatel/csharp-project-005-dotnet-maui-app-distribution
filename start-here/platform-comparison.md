---
doc_id: maui-dist-platform-comparison
title: iOS vs Android — Platform Comparison
type: guide
version: 1.2.0
status: active
created: 2026-08-23
updated: 2026-08-25
owner: Brijesh Patel
change_summary: Corrects two rows that still described the Android testing tracks and both enterprise channels as undocumented. Every one of them has a guide, now linked from the row.
---

# iOS vs Android — Platform Comparison

Written using ASD-STE100 principles. Every claim here traces to a documented channel guide —
follow the link in the last column for the full detail and its official sources.

| Area | 🍎 iOS (Apple) | 🤖 Android (Google) |
|---|---|---|
| Account | Apple Developer Program, US $99/year | Google Play Console, US $25 one-time |
| Account approval | 24 hours – 2 weeks (individual) | Identity verification; 14-day closed test with 12 testers if the personal account was created after 2023-11-13 |
| App identity | Bundle ID (reverse-DNS), permanent | Package name (reverse-DNS), permanent |
| 🔐 Signing | Distribution certificate + provisioning profile; one identity per app | Upload key + app signing key (Play App Signing recommended); Google can recover a lost upload key, not a lost app signing key if you opt out |
| Build tooling floor | iOS 26 SDK / Xcode 26, required from 2026-04-28 | API level 35 now, API level 36 from 2026-08-31 |
| 📦 Package format | `.ipa` | `.aab` (required for new apps; `.apk` for local install only) |
| Build executable without vendor OS? | **Compiles, but produces no package.** `dotnet publish -f net10.0-ios` exits 0 on Windows and builds the managed and AOT output, but writes no `.ipa` — and reports one it did not write. A signed `.ipa` needs a real Apple identity and a Mac | **Yes, with one property.** `dotnet publish -f net10.0-android -p:AndroidEnableMarshalMethods=false` succeeds on Windows natively and writes a real `.aab`. Without that property it fails with `XAGNM7009` |
| 🧪 Pre-production testing | [TestFlight](../platforms/apple/testflight/README.md): internal (100 testers, no review) and external (10,000 testers, first build needs Apple beta review). [Ad hoc distribution](../platforms/apple/ad-hoc-distribution/README.md) reaches registered devices only, capped at 100 per product family per year | Three Google Play tracks: [internal](../platforms/android/google-play-internal-testing/README.md) (up to 100 testers, fastest), [closed](../platforms/android/google-play-closed-testing/README.md) and [open](../platforms/android/google-play-open-testing/README.md). Closed and open both require production access first |
| Review | App Review, all submissions, duration not guaranteed | Play Review, all submissions, duration not guaranteed |
| Privacy declaration | Privacy manifest (required-reason APIs, third-party SDKs) | Data safety declaration |
| 🚀 First release upload | Manual via Visual Studio/Transporter | Manual via Play Console (establishes the signing-key relationship for all future releases) |
| 🔄 Update requirement | Version + build number must both increase | Version code must increase |
| Enterprise/private distribution | [Apple Business Manager Custom Apps, and the Apple Developer Enterprise Program](../platforms/apple/business-manager-and-enterprise/README.md). Apple does not permit the Enterprise Program where another route would serve | [Managed Google Play / Android Enterprise](../platforms/android/managed-google-play-enterprise/README.md), published privately to named organisations. [Direct APK install](../platforms/android/direct-apk-distribution/README.md) needs no store at all, and no review, updates or recall come with it |
| Full guide | [App Store public release](../platforms/apple/app-store-public-release/README.md) | [Google Play public release](../platforms/android/google-play-public-release/README.md) |
