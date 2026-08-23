---
doc_id: maui-dist-prerequisites-overview
title: Prerequisites Overview
type: guide
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial overview covering prerequisites common to both documented channels.
---

# Prerequisites Overview

These prerequisites apply before you start either channel. Each channel guide lists its own
platform-specific prerequisites in addition to these.

## Common to both channels

- A supported .NET SDK and .NET MAUI workload, matching what each channel guide's Freshness
  Register entry currently states as supported.
- A stable application identifier: the Bundle ID (Apple) and package name (Android) usually
  follow the same reverse-domain form, but each platform enforces its own identifier and neither
  can change after you first publish with it.
- A versioning scheme: a display version and a platform build number, both of which must
  increase on every release you submit.
- App icons and a splash image, sized per each store's own current requirements — see each
  channel guide's own Prerequisites section for the current values.
- A privacy policy URL, required by both stores before a public listing is accepted.
- Release-configuration build settings verified locally before you configure either store.

## Platform-specific

- Apple: see [`channels/AppleAppStorePublicRelease/README.md`](../channels/AppleAppStorePublicRelease/README.md#prerequisites).
- Android: see [`channels/GooglePlayPublicRelease/README.md`](../channels/GooglePlayPublicRelease/README.md#prerequisites).

## Before you create any signing material

Read the Security Model and Sign sections of whichever channel guide you are following before
generating a certificate, key, or keystore. Losing signing material after a first release can
mean losing the ability to publish updates to that same app listing — this is stated explicitly
in each channel guide, not assumed as background knowledge.
