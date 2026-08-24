---
doc_id: maui-dist-platform-apple
title: Apple / iOS Distribution
type: index
version: 1.1.0
status: active
created: 2026-08-23
updated: 2026-08-25
owner: Brijesh Patel
change_summary: Corrects the channel count from two to four, and rewrites the shared-material paragraph. ADR 0013's condition for extracting shared Apple material into this hub has now been met; the paragraph now records that as outstanding work for increment B rather than claiming the condition has not yet fired.
---

# Apple / iOS Distribution

This is the entry point for every Apple distribution channel this repository documents, and for
the guidance shared across them.

## Channels

| Channel | Status |
|---|---|
| [App Store public release](app-store-public-release/README.md) | Documented |
| [TestFlight](testflight/README.md) | Documented |
| [Ad hoc distribution](ad-hoc-distribution/README.md) | Documented |
| [Apple Business Manager and enterprise distribution](business-manager-and-enterprise/README.md) | Documented |

## Signing and provisioning

App Store public release, TestFlight and ad hoc distribution share one **certificate**: the same
Apple distribution certificate. They do **not** share a provisioning profile — an ad hoc profile
embeds an explicit device list and is generated separately, as its
[§7](ad-hoc-distribution/README.md#7-security-model) explains. See
[App Store public release §7 Security Model](app-store-public-release/README.md#7-security-model)
and [§10 Sign](app-store-public-release/README.md#10-sign) — every current and future Apple
channel in this repository references that explanation rather than repeating it, per this
project's efficient-information-architecture principle (one authoritative explanation per shared
concept).

## Certificates and identities, privacy and compliance, release management, troubleshooting, automation

Each of these is currently covered **inside each channel's own guide** (its Prerequisites,
Security Model and Troubleshooting sections) rather than as a separate shared document.

**The condition for extracting them has now been met.** ADR 0013 recorded that shared,
platform-specific material moves into this hub once a later Apple channel repeats it. Four Apple
channels now exist, and they do repeat material. **The extraction has not happened yet** — it is
increment B of the documentation restructure, and this paragraph stays until it is done. It
records outstanding work, not a completed state.

## Where to start

New to Apple distribution entirely? Start at
[`../../start-here/choose-your-distribution-channel.md`](../../start-here/choose-your-distribution-channel.md).
