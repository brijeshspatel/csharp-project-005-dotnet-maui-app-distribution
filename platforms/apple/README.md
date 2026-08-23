---
doc_id: maui-dist-platform-apple
title: Apple / iOS Distribution
type: index
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial Apple platform hub, grouping all Apple-related channels and shared Apple-specific guidance in one place.
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
| Apple Business Manager / enterprise distribution | Not yet documented |

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
Security Model and Troubleshooting sections) rather than as a separate shared document, because
only two channels exist so far and their content does not yet diverge enough to justify
extracting it. **This is a placeholder statement of intent, not a claim that the extraction has
happened** — when a third or fourth Apple channel repeats material identical across all of them,
that shared material moves here instead of being copied again, per the same principle.

## Where to start

New to Apple distribution entirely? Start at
[`../../start-here/choose-your-distribution-channel.md`](../../start-here/choose-your-distribution-channel.md).
