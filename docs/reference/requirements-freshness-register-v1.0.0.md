---
doc_id: maui-dist-requirements-freshness-register
title: Requirements & Freshness Register
type: reference
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Populated with Apple App Store and Google Play public-release entries.
---

# Requirements & Freshness Register

Every time-sensitive external requirement this repository depends on is recorded here, with the
date it was last independently verified and what should trigger re-checking it.

| Requirement | Platform | Area | Effective Date | Last Verified | Official Source | Applies To | Impact | Status | Reverification Trigger |
|---|---|---|---|---|---|---|---|---|---|
| Apple Developer Program membership fee is US $99/year | Apple | account | ongoing | 2026-08-23 | https://developer.apple.com/programs/enroll/ | New and existing accounts | Budget for annual renewal | Current | Apple pricing page changes |
| App Store submissions require the iOS 26 SDK (Xcode 26+) | Apple | build tooling | 2026-04-28 | 2026-08-23 | https://developer.apple.com/news/upcoming-requirements/ | New app / update, submitted on or after 2026-04-28 | Build tooling must target iOS 26 SDK or submission is rejected | Current | Apple announces a new SDK floor |
| Distribution requires a distribution certificate + provisioning profile + App ID | Apple | signing | ongoing | 2026-08-23 | https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-app-store?view=net-maui-10.0 | New app / update | Cannot submit without all three | Current | Microsoft or Apple changes the signing model |
| App Review privacy manifest required for required-reason APIs / third-party SDKs | Apple | privacy | ongoing | 2026-08-23 | https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-app-store?view=net-maui-10.0 | New app / update | Missing declaration risks rejection | Current | Apple privacy policy changes |
| Google Play requires an Android App Bundle (.aab) for new apps | Android | build tooling | 2021-08 | 2026-08-23 | https://developer.android.com/guide/app-bundle | New app | APK-only uploads no longer accepted for new apps | Current | Google Play Console policy changes |
| Google Play Console one-time registration fee is US $25 | Android | account | ongoing | 2026-08-23 | https://support.google.com/googleplay/android-developer/answer/6112435 | New developer accounts | Budget for one-time fee, non-refundable | Current | Google changes registration pricing |
| Google Play target API level: API 35 required now, API 36 required from 2026-08-31 | Android | build tooling | 2026-08-31 (API 36 floor) | 2026-08-23 | https://support.google.com/googleplay/android-developer/answer/11926878 | New app / update | Builds targeting below the current floor are rejected | Upcoming (API 36 floor is 8 days away as of Last Verified) | 2026-08-31, or Google announces a new floor |
| Personal developer accounts created after 2023-11-13 must complete a 14-day closed test with 12 opted-in testers before production access | Android | account | 2023-11-13 | 2026-08-23 | https://support.google.com/googleplay/android-developer/answer/6112435 | New personal accounts | Cannot reach production without completing this test | Current | Google changes the testing-track requirement |
