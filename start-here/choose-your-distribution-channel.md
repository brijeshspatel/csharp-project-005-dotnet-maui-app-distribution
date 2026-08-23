---
doc_id: maui-dist-choose-channel
title: Choose Your Distribution Channel
type: guide
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial guide covering the two documented channels.
---

# Choose Your Distribution Channel

This repository currently documents two channels: public release through the **Apple App
Store**, and public release through **Google Play**. Most .NET MAUI apps that reach the public
need both, since Apple and Android users cannot install from each other's store.

## Overall lifecycle

```mermaid
flowchart TD
    A[Nothing configured] --> B[Prerequisites]
    B --> C[Prepare application]
    C --> D{Choose platform}
    D -->|iOS| E[Apple App Store public release]
    D -->|Android| F[Google Play public release]
    E --> G[Sign and package]
    F --> G
    G --> H[Internal testing]
    H --> I[Store readiness]
    I --> J[Submit]
    J --> K[Review]
    K --> L[Release]
    L --> M[Post-release verification]
```

## Which channel do I need?

| Your situation | Read this first |
|---|---|
| Publishing to the general public on iOS | [`channels/AppleAppStorePublicRelease/README.md`](../channels/AppleAppStorePublicRelease/README.md) |
| Publishing to the general public on Android | [`channels/GooglePlayPublicRelease/README.md`](../channels/GooglePlayPublicRelease/README.md) |
| Beta testing before a public iOS release | Not yet documented — see the catalogue |
| Beta testing before a public Android release | Not yet documented — see the catalogue |
| Distributing only inside your own organisation | Not yet documented — see the catalogue |
| Distributing on Windows | Out of scope for this phase — see the catalogue |

See [`docs/maui-distribution-channel-catalogue-v1.0.0.md`](../docs/maui-distribution-channel-catalogue-v1.0.0.md)
for the complete list of channels this repository's scope covers, including those not yet
documented.

## Before you start either channel

Read [`prerequisites-overview.md`](prerequisites-overview.md) first. Some prerequisites —
supported .NET MAUI version, application identifier, versioning, icons — apply to both channels
and are worth settling before you pick one.
