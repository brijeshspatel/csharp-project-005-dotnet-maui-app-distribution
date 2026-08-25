# Controlled Terminology

One term per concept. Every guide in this repository uses these terms consistently. Where an
official platform term exists, that term is used, not a paraphrase.

| Term used here | Official term | Platform | Meaning |
|---|---|---|---|
| App Bundle | App Bundle (`.aab`) | Android | The publishing format Google Play requires; Google Play generates per-device APKs from it. |
| APK | Android Package (`.apk`) | Android | The installable Android package format. Used for direct install and internal testing; not the Google Play upload format. |
| App Signing Key | App signing key | Android | The private key that signs the final APK a device installs. Managed by Play App Signing unless the developer opts out. |
| Upload Key | Upload key | Android | The private key that signs the App Bundle uploaded to Play Console. Distinct from the app signing key when Play App Signing is enabled. |
| Package Name | Application ID / package name | Android | The unique, permanent identifier for an Android app (for example `com.example.app`). Cannot change after publication. |
| IPA | iOS App Store Package (`.ipa`) | Apple | The installable/archivable iOS package format. |
| Bundle ID | Bundle Identifier | Apple | The unique identifier for an iOS app (for example `com.example.app`), registered in the Apple Developer account. |
| Provisioning Profile | Provisioning profile | Apple | Links an app's Bundle ID, a signing certificate, and (for non-App-Store profiles) permitted devices, authorising the app to run outside Xcode's own debug signing. |
| Distribution Certificate | Distribution certificate | Apple | The certificate used to sign an app for release, distinct from a development certificate. |
| Ad Hoc Signing | Ad hoc code signing | Apple / .NET | .NET's own local signing of an iOS build when no Apple Distribution certificate is configured. Produces an installable `.ipa` for local verification only — not accepted by App Store Connect or a real device without its own trust. |
| Release Track | Release track | Android | A named distribution channel within Google Play Console (internal, closed, open, production). |
| App Review | App Review | Apple | Apple's manual and automated review of a submitted build before it may appear on the App Store. |
| Play Review | Play Review | Android | Google's review of a submitted app before it may appear on Google Play. |
