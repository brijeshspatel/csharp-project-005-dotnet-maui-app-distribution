# Controlled Terminology

One term per concept. Every guide in this repository uses these terms consistently. Where an
official platform term exists, that term is used, not a paraphrase.

**Read the first column as naming the concept, not prescribing capitalisation.** Entries are
Title Cased here so the table scans; in running prose the guides follow each vendor's own casing —
"upload key", "app signing key", "package name" and "track" are lowercase, while "App Review" and
"Apple Business Manager" are capitalised because Apple capitalises them. Where the two columns
disagree on case, the **Official term** column governs.

| Term used here | Official term | Platform | Meaning |
|---|---|---|---|
| App Bundle | Android App Bundle (`.aab`) | Android | The publishing format Google Play requires for new apps; Google Play generates per-device APKs from it. Google's full term is "Android App Bundle"; "App Bundle" is the accepted short form and is what this repository uses after first mention. |
| APK | Android Package (`.apk`) | Android | The installable Android package format. Used for direct install and local testing. **It is not the Google Play upload format for any track** — internal, closed and open testing all take an App Bundle, exactly as production does. |
| App Signing Key | App signing key | Android | The private key that signs the final APK a device installs. Managed by Play App Signing unless the developer opts out. |
| Upload Key | Upload key | Android | The private key that signs the App Bundle uploaded to Play Console. Distinct from the app signing key when Play App Signing is enabled. |
| Package Name | Application ID / package name | Android | The unique, permanent identifier for an Android app (for example `com.example.app`). Cannot change after publication. |
| IPA | ".ipa file" / app archive | Apple | The installable, uploadable iOS package format. Apple's documentation calls it simply an ".ipa file"; the expansion "iOS App Store Package" is third-party usage, not Apple's, so this repository does not present it as an official term. |
| Bundle ID | Bundle Identifier | Apple | The unique identifier for an iOS app (for example `com.example.app`), registered in the Apple Developer account. |
| Provisioning Profile | Provisioning profile | Apple | Links an app's Bundle ID, a signing certificate, and (for non-App-Store profiles) permitted devices, authorising the app to run outside Xcode's own debug signing. |
| Distribution Certificate | Distribution certificate | Apple | The certificate used to sign an app for release, distinct from a development certificate. |
| Ad hoc code signing | Ad hoc code signing (`codesign -s -`) | Apple / .NET | Signing with the placeholder identity `-`, which seals a binary without any certificate or identity. .NET for iOS applies it **only to simulator builds** — the SDK's own source calls it the placeholder key. **It never produces a distributable `.ipa`:** device builds require a real identity, the archive target errors without a code-signing key, and the target that writes the package depends on `Codesign`. |
| Ad hoc distribution | Ad hoc distribution | Apple | An Apple **distribution channel**: a build signed with a real distribution certificate and an ad hoc provisioning profile that enumerates specific registered device UDIDs. Despite the shared adjective it is unrelated to *ad hoc code signing* above, and the two must never be used interchangeably. |
| Track | "track" / "testing track" | Android | A named distribution stream within Google Play Console: internal, closed, open, or production. Google writes this lowercase and does not treat it as a proper noun, so neither does this repository. |
| App Review | App Review | Apple | Apple's manual and automated review of a submitted build before it may appear on the App Store. Apple does capitalise this as a proper noun. |
| Google Play app review | "app review"; release status "In review" | Android | Google's review of a submitted app or update before it may be published. **Google does not brand this with a proper noun.** Its documentation uses lowercase "app review", "send for review" and "changes in review", and Play Console shows the release status "In review". Write "Google Play's app review" or simply "review" — never "Play Review", which is not a term Google uses. |
