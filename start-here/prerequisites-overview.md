# Prerequisites Overview

These prerequisites apply before you start **any** of the ten channels this repository documents.
Each channel guide lists its own prerequisites in addition to these.

## Common to every channel

- A supported .NET SDK and .NET MAUI workload, matching what each channel guide's Freshness
  Register entry currently states as supported.
- A stable application identifier: the Bundle ID (Apple) and package name (Android) usually
  follow the same reverse-domain form, but each platform enforces its own identifier and neither
  can change after you first publish with it.
- A versioning scheme: a display version and a platform build number, both of which must
  increase on every release you submit.
- App icons and a splash image, sized per the current requirements of whichever channel you use
  — see that channel guide's own Prerequisites section for the values.
- Release-configuration build settings verified locally before you configure any distribution
  platform.

## Required by the public stores, but not by every channel

- **A privacy policy URL.** Both public store listings require one. The direct APK channel has no
  listing and no reviewer, so nothing enforces it there.
- **A store listing, content rating and privacy declaration.** These belong to the store
  channels. Ad hoc and direct APK distribution have none of them.

## Platform-specific

- Apple: see [`platforms/apple/README.md`](../platforms/apple/README.md) for the four Apple
  channels, and
  [App Store public release §5](../platforms/apple/app-store-public-release/README.md#5-prerequisites)
  for the fullest prerequisite list.
- Android: see [`platforms/android/README.md`](../platforms/android/README.md) for the six
  Android channels, and
  [Google Play public release §5](../platforms/android/google-play-public-release/README.md#5-prerequisites)
  for the fullest prerequisite list.

## Before you create any signing material

Read the Security Model and Sign sections of whichever channel guide you are following before
generating a certificate, key, or keystore. Losing signing material after a first release can
mean losing the ability to publish updates to that same app listing — this is stated explicitly
in each channel guide, not assumed as background knowledge.
