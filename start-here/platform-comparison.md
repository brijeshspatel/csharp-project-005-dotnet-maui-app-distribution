---
doc_id: maui-dist-platform-comparison
title: iOS vs Android — Platform Comparison
type: guide
version: 1.1.0
status: active
created: 2026-08-23
updated: 2026-08-24
owner: Brijesh Patel
change_summary: Corrects the build-without-vendor-OS row for both platforms, after clean-tree re-verification. Written using ASD-STE100 principles.
---

# 📚 iOS vs Android — Platform Comparison

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
| 🧪 Pre-production testing | TestFlight: internal (100 testers, no review) and external (10,000 testers, first build needs Apple beta review). Ad hoc distribution reaches registered devices only, capped at 100 per product family per year | Internal, closed, open testing tracks (not yet documented in this repository) |
| Review | App Review, all submissions, duration not guaranteed | Play Review, all submissions, duration not guaranteed |
| Privacy declaration | Privacy manifest (required-reason APIs, third-party SDKs) | Data safety declaration |
| 🚀 First release upload | Manual via Visual Studio/Transporter | Manual via Play Console (establishes the signing-key relationship for all future releases) |
| 🔄 Update requirement | Version + build number must both increase | Version code must increase |
| Enterprise/private distribution | Not yet documented (Apple Business Manager / enterprise programme) | Not yet documented (Managed Google Play / Android Enterprise) |
| Full guide | [App Store public release](../platforms/apple/app-store-public-release/README.md) | [Google Play public release](../platforms/android/google-play-public-release/README.md) |
