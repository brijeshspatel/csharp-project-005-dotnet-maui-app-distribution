---
doc_id: maui-dist-channel-catalogue
title: .NET MAUI Distribution Channel Catalogue
type: index
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial catalogue. Two channels documented (Apple App Store, Google Play). Every other channel this repository's scope discusses is marked explicitly, not silently absent.
---

# .NET MAUI Distribution Channel Catalogue

This catalogue lists every distribution channel this repository's scope discusses, and whether
each is documented yet. A channel linked to a folder rather than a `README.md` is not done.

## Documented channels

| Channel | Platform | Guide | Status |
|---|---|---|---|
| App Store public release | Apple | [`platforms/apple/app-store-public-release/README.md`](../platforms/apple/app-store-public-release/README.md) | Documented |
| Google Play public release | Android | [`platforms/android/google-play-public-release/README.md`](../platforms/android/google-play-public-release/README.md) | Documented |
| TestFlight | Apple | [`platforms/apple/testflight/README.md`](../platforms/apple/testflight/README.md) | Documented |
| Ad hoc distribution | Apple | [`platforms/apple/ad-hoc-distribution/README.md`](../platforms/apple/ad-hoc-distribution/README.md) | Documented |
| Apple Business Manager / enterprise distribution | Apple | [`platforms/apple/business-manager-and-enterprise/README.md`](../platforms/apple/business-manager-and-enterprise/README.md) | Documented |

| Google Play internal testing | Android | [`platforms/android/google-play-internal-testing/README.md`](../platforms/android/google-play-internal-testing/README.md) | Documented |

| Google Play closed testing | Android | [`platforms/android/google-play-closed-testing/README.md`](../platforms/android/google-play-closed-testing/README.md) | Documented |

| Google Play open testing | Android | [`platforms/android/google-play-open-testing/README.md`](../platforms/android/google-play-open-testing/README.md) | Documented |

## Not yet documented

These channels are within the mobile distribution domain this repository covers, but are not
built in this increment. They are listed so a reader can see they were considered, not missed.

| Channel | Platform | Status |
|---|---|---|
| Managed Google Play / Android Enterprise distribution | Android | not yet documented |
| Direct APK distribution | Android | not yet documented |

## Excluded from this repository's current scope

| Channel | Platform | Status |
|---|---|---|
| Microsoft Store / Windows application distribution | Microsoft | excluded from this phase — the objective is mobile application distribution; may be added later if there is a clear need |

## Section contract every documented channel follows

Every channel guide under `platforms/<platform>/<channel>/README.md` uses this fixed section order: What
This Channel Is; When to Use It; When Not to Use It; Eligibility; Prerequisites; How to Obtain
the Prerequisites; Security Model; Application Preparation; Build; Sign; Package; Configure
Distribution Platform; Deploy; Validate; Update; Revoke / Withdraw / Retire; Troubleshooting;
Limitations; Official Sources; Last Verified.
