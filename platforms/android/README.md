---
doc_id: maui-dist-platform-android
title: Android / Google Distribution
type: index
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial Android platform hub, grouping all Android-related channels and shared Android-specific guidance in one place.
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
| Direct APK distribution | Not yet documented |

## Signing and keystores

See [Google Play public release §7 Security Model](google-play-public-release/README.md#7-security-model)
and [§10 Sign](google-play-public-release/README.md#10-sign) for the upload-key/app-signing-key
distinction every current and future Android channel in this repository relies on.

## Certificates and identities, privacy and compliance, release management, troubleshooting, automation

Currently covered **inside the Google Play guide itself** — only one channel exists so far, so
there is nothing yet to extract into a shared document without duplicating it prematurely. When a
second Android channel repeats material identical across both, that shared material moves here.

## Where to start

New to Android distribution entirely? Start at
[`../../start-here/choose-your-distribution-channel.md`](../../start-here/choose-your-distribution-channel.md).
