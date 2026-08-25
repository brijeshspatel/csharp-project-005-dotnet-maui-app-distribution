# Apple App Store — Public Release

## 1. What This Channel Is

The Apple App Store is Apple's public application marketplace for iOS and iPadOS. A public
release through this channel makes your app discoverable and installable by any user with an
Apple Account, in the countries you select. Apple reviews every submission before it appears.

## 2. When to Use It

Use this channel when your app is ready for the general public, and you want the widest possible
reach on iOS without restricting who can install it.

## 3. When Not to Use It

Do not use this channel for an app still under active internal or external testing — use
[TestFlight](../testflight/README.md) first. Do not use it for an app intended only for your
own organisation's devices — that is
[Apple Business Manager or enterprise distribution](../business-manager-and-enterprise/README.md),
or [ad hoc distribution](../ad-hoc-distribution/README.md) for a fixed list of registered
devices.

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
(`sample/DistributionSample`), 2026-08-23, and re-verified the same day from a fully clean tree
with `bin/` and `obj/` both removed:

```
dotnet publish -f net10.0-ios -c Release
```

On a Windows machine with no macOS host, this command **exits 0 with 0 warnings and 0 errors** and
compiles the managed and AOT output to `bin/Release/net10.0-ios/ios-arm64/`. **It does not produce
an `.ipa`.**

**WARNING — the build log claims an `.ipa` that does not exist.** The command prints
`Created the package: bin\Release\net10.0-ios\ios-arm64\publish\DistributionSample.ipa` and
then writes no such file; the `publish` folder is created and left empty. This is a reporting
defect in the iOS SDK itself. In
`Microsoft.iOS.Sdk.net10.0_26.5/26.5.10301/targets/Xamarin.Shared.Sdk.Publish.targets`, the
`Publish` target emits that message whenever `BuildIpa` is true, but `Publish` depends only on
`_PrePublish;Build` and never invokes `CreateIpa`, which is the target that would write the
archive. **Never accept that line, or exit code 0, as evidence that an `.ipa` exists. Confirm the
file is on disk.**

**Producing a real `.ipa` requires code signing.** Adding the archive properties Microsoft
documents for command-line publishing makes the requirement explicit instead of silent:

```
dotnet publish -f net10.0-ios -c Release -p:ArchiveOnBuild=true -p:RuntimeIdentifier=ios-arm64
```

This fails immediately, and correctly, with:

```
error : Code signing must be enabled to create an Xcode archive.
```

**What this proves, and what it does not.** The managed compilation and AOT steps of an iOS Release
build run on Windows with no Mac. Producing an installable, distributable `.ipa` does not: it needs
a real signing identity (§10) and Apple's archiving tools. Treat §10-§11 as prerequisites of a
package, not as refinements of one you already have.

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
flow) produces the `.ipa` uploaded to App Store Connect. **No `.ipa` exists before that point** —
see the warning in §9. There is no unsigned intermediate package to inspect on this platform.

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
| Build reports `Created the package: ...DistributionSample.ipa` but no `.ipa` exists | The SDK's `Publish` target prints this message unconditionally when `BuildIpa` is true, without running `CreateIpa` | List the `publish` folder; it is empty | Expected without signing. Supply `CodesignKey`/`CodesignProvision` per §10, or use the Archive/Distribute flow. See §9 |
| `error : Code signing must be enabled to create an Xcode archive.` | `ArchiveOnBuild=true` was set with no signing identity | Confirm whether `CodesignKey` and `CodesignProvision` are supplied | Supply a real distribution identity per §10, or drop `ArchiveOnBuild` and accept that no `.ipa` is produced |

## 18. Limitations

**This guide's packaging step is documented, not demonstrated.** Execution on Windows without a
Mac proves the managed and AOT compilation steps only. **No `.ipa` was produced in any run of this
repository**, because every route to one requires a real Apple signing identity — see §9 for the
commands run and their exact results. Creating a genuine Apple distribution certificate (§10) was
likewise not executed: it requires an enrolled Apple Developer Program identity and, per
Microsoft's current documentation, a Mac-paired Visual Studio. Every claim in §10-§13 therefore
rests on the sources in §19, not on execution in this environment. App Review timing is not
guaranteed; do not present any duration as a commitment.

## 19. Official Sources

- [Publish a .NET MAUI iOS app for App Store distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-app-store?view=net-maui-10.0)
- [Publish a .NET MAUI iOS app using the command line — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-cli?view=net-maui-10.0)
- [Apple Developer Program — Become a member](https://developer.apple.com/programs/enroll/)
- [Apple Developer — SDK minimum requirements](https://developer.apple.com/news/upcoming-requirements/)

## 20. Last Verified

2026-08-23 — the §9 build claims were verified by execution against this repository's own sample
application, including a clean-tree re-run that corrected an earlier, incorrect claim that an
`.ipa` had been produced. Packaging and signing (§10-§11) are **not** execution-verified. All other
claims were verified against the sources in §19 on the same date.
