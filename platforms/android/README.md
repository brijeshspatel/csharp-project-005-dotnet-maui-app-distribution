---
doc_id: maui-dist-platform-android
title: Android / Google Distribution
type: index
version: 1.1.0
status: active
created: 2026-08-23
updated: 2026-08-25
owner: Brijesh Patel
change_summary: Corrects the channel count from one to six, and rewrites the shared-material paragraph. ADR 0013's condition for extracting shared Android material into this hub has now been met; the paragraph now records that as outstanding work for increment B rather than claiming the condition has not yet fired.
---

# Android / Google Distribution

This is the entry point for every Android distribution channel this repository documents, and
for the guidance shared across them.

## Channels

| Channel | Status |
|---|---|
| [Google Play public release](google-play-public-release/README.md) | Documented |
| [Google Play internal testing](google-play-internal-testing/README.md) | Documented |
| [Google Play closed testing](google-play-closed-testing/README.md) | Documented |
| [Google Play open testing](google-play-open-testing/README.md) | Documented |
| [Managed Google Play / Android Enterprise distribution](managed-google-play-enterprise/README.md) | Documented |
| [Direct APK distribution](direct-apk-distribution/README.md) | Documented |

## Signing and keystores

See [Google Play public release §7 Security Model](google-play-public-release/README.md#7-security-model)
and [§10 Sign](google-play-public-release/README.md#10-sign) for the upload-key/app-signing-key
distinction every current and future Android channel in this repository relies on.

## Certificates and identities, privacy and compliance, release management, troubleshooting, automation

Currently covered **inside each channel's own guide**, with the Google Play public release guide
holding the authoritative explanation that the other five reference.

**The condition for extracting them has now been met.** ADR 0013 recorded that shared,
platform-specific material moves into this hub once a later Android channel repeats it. Six
Android channels now exist, and they do repeat material. **The extraction has not happened yet**
— it is increment B of the documentation restructure, and this paragraph stays until it is done.
It records outstanding work, not a completed state.

## Where to start

New to Android distribution entirely? Start at
[`../../start-here/choose-your-distribution-channel.md`](../../start-here/choose-your-distribution-channel.md).
