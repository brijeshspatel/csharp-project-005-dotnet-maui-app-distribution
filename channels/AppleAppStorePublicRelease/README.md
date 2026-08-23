---
doc_id: maui-dist-channel-apple-app-store
title: Apple App Store — Public Release
type: guide
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial channel guide. Written using ASD-STE100 principles.
---

# Apple App Store — Public Release

Written using ASD-STE100 principles.

## 1. What This Channel Is

The Apple App Store is Apple's public application marketplace for iOS and iPadOS. A public
release through this channel makes your app discoverable and installable by any user with an
Apple Account, in the countries you select. Apple reviews every submission before it appears.

## 2. When to Use It

Use this channel when your app is ready for the general public, and you want the widest possible
reach on iOS without restricting who can install it.

## 3. When Not to Use It

Do not use this channel for an app still under active internal or external testing — use
TestFlight first (not yet documented in this repository; see the channel catalogue). Do not use
it for an app intended only for your own organisation's devices — that is enterprise or ad hoc
distribution (not yet documented).

## 4. Eligibility

You need an active **Apple Developer Program** membership. Individual and organisation
enrolment both require an Apple Account with two-factor authentication; an organisation also
needs a D-U-N-S number for its legal entity. Membership costs **US $99 per year** (regional
pricing varies); nonprofit, educational and government entities may qualify for a fee waiver.
**Last verified: 2026-08-23.**

## 5. Prerequisites

- An enrolled Apple Developer Program membership (§4).
- A macOS build host, or Visual Studio paired to one, for creating a distribution certificate and
  for producing an App-Store-ready signed archive. See §7 for exactly which step this applies to.
- A stable Bundle ID in reverse-DNS form (for example `com.example.app`), matching your .NET MAUI
  project's **Application ID** property.
- App icons and a launch image meeting Apple's current published sizes.
- A publicly accessible privacy policy URL.
- A **privacy manifest** file declaring any required-reason APIs and third-party SDK data
  collection your app uses — omitting a used API from this file can cause App Review to reject
  the build.
- **Your build tooling must target the iOS 26 SDK (Xcode 26 or later)** for any submission made
  on or after 2026-04-28 — this is a hard Apple requirement, not a recommendation. Confirm your
  installed .NET MAUI iOS workload version supports this before you rely on it (§9).

## 6. How to Obtain the Prerequisites

Enrol at the Apple Developer Program's own enrolment page. Individual enrolment typically takes
24 hours to two weeks to verify. Create your Bundle ID and distribution certificate as part of
§10-§11 below — they are obtained together with the provisioning profile, not separately in
advance.

## 7. Security Model

Three things must agree before Apple accepts a build: a **distribution certificate** (proves who
you are), an **App ID** matching your Bundle ID, and a **provisioning profile** binding the two
for App Store distribution. The certificate's private key exists only on the machine that created
it (or wherever it was exported to) — losing it means revoking the certificate and re-creating
your provisioning profile, which does not lose your existing App Store listing but does require
re-signing every future build with a new identity.

**Ad hoc signing is not the same as this.** Running `dotnet publish` for iOS without specifying a
real distribution certificate produces a package .NET signs itself, for local verification only.
It is not accepted by App Store Connect. See §9 for exactly what this repository verified.

## 8. Application Preparation

Set your Bundle ID as the **Application ID** property in your .NET MAUI project — Visual Studio
keeps this synchronised with `Info.plist` automatically. Set your display version and build
number; both must increase on every submission. Confirm your target framework is current enough
to satisfy §5's SDK requirement.

## 9. Build

**Verified by execution against this repository's own sample application**
(`sample/DistributionSample`), 2026-08-23:

```
dotnet publish -f net10.0-ios -c Release
```

This succeeded on a Windows machine with no macOS host, producing
`bin/Release/net10.0-ios/ios-arm64/publish/DistributionSample.ipa`. The build log reported: "X.509
certificate chain validation will use the default trust store selected by .NET for code signing"
— this is .NET's own **ad hoc** signing, used because no `CodesignKey`/`CodesignProvision` was
supplied. **This proves the managed-code build and packaging step itself does not require a Mac.**
It does not prove App-Store-ready signing, which needs the identity described in §10-§11.

## 10. Sign

To sign with a real distribution identity, add the `CodesignKey` and `CodesignProvision`
properties, naming the distribution certificate and provisioning profile created in §11:

```
dotnet publish -f net10.0-ios -c Release ^
  -p:CodesignKey="Apple Distribution: <Your Name or Org> (<Team ID>)" ^
  -p:CodesignProvision="<Provisioning Profile Name>"
```

Creating the distribution certificate itself is documented by Microsoft as a Visual-Studio-driven
step (**Tools > Options > Xamarin > Apple Accounts > Create Certificate > iOS Distribution**),
which exports the private key to Keychain Access on a paired Mac build host. **This repository did
not execute this step** — it requires a real Apple Developer Program identity and, per Microsoft's
own current documentation, a Mac build host paired to Visual Studio. This is the credentials and
tooling limitation this guide names plainly, not an unstated one.

## 11. Package

Once signed with a real identity, `dotnet publish` (or Visual Studio's own Archive/Distribute
flow) produces the `.ipa` uploaded to App Store Connect. The unsigned/ad-hoc `.ipa` verified in
§9 is structurally the same package format; only its signature differs.

## 12. Configure Distribution Platform

Create an app record in **App Store Connect** before uploading: name, primary language, Bundle
ID, and a unique SKU. This record is what your uploaded build attaches to.

## 13. Deploy

Upload via Visual Studio's Distribute dialog (select **App Store**, then **Upload to Store**,
authenticating with an app-specific password — not your normal Apple Account password), or via
Transporter for a `.ipa` already produced. Uploading requires the app record from §12 to already
exist.

## 14. Validate

Confirm the build appears in App Store Connect under your app record, in "Processing" then
"Ready to Submit" status. Transporter reports packaging errors before upload completes, which
catches most signing mismatches early.

## 15. Update

Increase both the display version and the build number, repeat §9-§14, and attach the new build
to the same app record. Apple does not require a new provisioning profile per release unless your
certificate has expired or capabilities changed.

## 16. Revoke / Withdraw / Retire

Remove an app from sale from its App Store Connect record (**Pricing and Availability**). This
stops new installs; it does not remove the app from devices that already installed it. Revoking a
distribution certificate invalidates every provisioning profile built from it — done only when
the certificate itself is compromised or no longer needed.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| Build rejected: privacy manifest missing a declaration | A required-reason API or third-party SDK is used but not declared | Check App Review's rejection message for the named API | Add the declaration to the privacy manifest, per §5, and resubmit |
| Signing mismatch on upload | Provisioning profile does not match the certificate or Bundle ID used to sign | Compare the profile's App ID and certificate against `CodesignProvision`/`CodesignKey` | Regenerate or select the correct profile in §11 |
| Build built on the wrong SDK | Tooling predates the iOS 26 SDK requirement (effective 2026-04-28) | Check the installed `ios` workload version | Update the .NET MAUI iOS workload before building |

## 18. Limitations

This guide's build and packaging steps (§9) were verified by execution on Windows without a Mac.
Creating a genuine Apple distribution certificate (§10) was not executed in this run — it requires
an enrolled Apple Developer Program identity and, per Microsoft's current documentation, a
Mac-paired Visual Studio. App Review timing is not guaranteed; do not present any duration as a
commitment.

## 19. Official Sources

- [Publish a .NET MAUI iOS app for App Store distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-app-store?view=net-maui-10.0)
- [Publish a .NET MAUI iOS app using the command line — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-cli?view=net-maui-10.0)
- [Apple Developer Program — Become a member](https://developer.apple.com/programs/enroll/)
- [Apple Developer — SDK minimum requirements](https://developer.apple.com/news/upcoming-requirements/)

## 20. Last Verified

2026-08-23 — build/package claims verified by execution against this repository's own sample
application; all other claims verified against the sources in §19 on the same date.
