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

You need an active **Apple Developer Program** membership. Individual and organisation enrolment
both require an Apple Account with two-factor authentication; an organisation also needs a
D-U-N-S Number for its legal entity — **except government organisations, for which Apple does not
require one**. Membership costs **US $99 per year** (regional pricing varies). Nonprofits,
accredited educational institutions and government entities may qualify for a **fee waiver**,
provided the organisation is a legal entity, has not signed the Paid Applications Agreement, and
does not sell digital goods or services through its apps. **Last verified: 2026-08-26.**

## 5. Prerequisites

- An enrolled Apple Developer Program membership (§4).
- A macOS build host, or Visual Studio paired to one, for creating a distribution certificate and
  for producing an App-Store-ready signed archive. See §7 for exactly which step this applies to.
- A stable Bundle ID in reverse-DNS form (for example `com.example.app`), matching your .NET MAUI
  project's **Application ID** property.
- App icons and a launch image meeting Apple's current published sizes.
- A publicly accessible privacy policy URL.
- A **privacy manifest** declaring approved reasons for any of Apple's **required-reason APIs**
  your code uses — mandatory for all apps since 2024-05-01 — and required for any SDK on Apple's
  **published list** of commonly used third-party SDKs, which also need a valid signature when
  used as binary dependencies. It is **not** required for every third-party SDK, only those on
  that list. A missing declaration blocks upload to App Store Connect.
- **Your build tooling must use Xcode 26 or later with an SDK for iOS 26** for anything
  **uploaded to App Store Connect** on or after 2026-04-28. Apple frames this as an *upload*
  requirement rather than a submission one, and states it equally for iPadOS 26, tvOS 26,
  visionOS 26 and watchOS 26. It is a hard requirement, not a recommendation. Confirm your
  installed .NET MAUI iOS workload supports it before you rely on it (§9).

## 6. How to Obtain the Prerequisites

Enrol at the Apple Developer Program's own enrolment page. Individual enrolment typically takes
24 hours to two weeks to verify. Create your Bundle ID and distribution certificate as part of
**§10 Sign** below — they are obtained together with the provisioning profile, not separately in
advance.

## 7. Security Model

Three things must agree before Apple accepts a build: a **distribution certificate** (proves who
you are), an **App ID** matching your Bundle ID, and a **provisioning profile** binding the two
for App Store distribution. The certificate's private key exists only on the machine that created
it (or wherever it was exported to) — losing it means revoking the certificate and re-creating
your provisioning profile, which does not lose your existing App Store listing but does require
re-signing every future build with a new identity.

**There is no self-signed fallback, and this guide previously said otherwise.** Running
`dotnet publish` for iOS without a real distribution certificate does **not** produce a package
.NET signs itself. Device builds require a genuine signing identity: the SDK's archive target
errors outright when no code-signing key is set, and the target that writes the `.ipa` depends on
`Codesign`. Apple's *ad hoc code signing* — the placeholder identity `-` — is applied by the SDK
**only to simulator builds** and never yields a distributable package.

Do not confuse that with **ad hoc distribution** (§3), which is a genuine Apple channel using a
real distribution certificate and a device-limited provisioning profile. The two share an
adjective and nothing else; see the [controlled terminology](../../../docs/reference/terminology.md).
§9 records what this repository actually observed: **no package at all**, which is the absence of a
signed artefact rather than the presence of a self-signed one.

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
then writes no such file; the `publish` folder is created and left empty.

**The mechanism matches a still-open SDK issue,
[dotnet/macios#20958](https://github.com/dotnet/macios/issues/20958)**, whose diagnosis is the one
below. Note the issue's own reproduction runs `build` and `publish` as separate ordered steps
rather than the single bare command used here, so treat this as the same underlying fault rather
than as a report of this exact invocation.

The mechanism, read from the SDK's own targets files: in `Xamarin.Shared.Sdk.Publish.targets` the
`Publish` target emits that message whenever `$(BuildIpa)` is true, with no check that the package
was written.
The target that actually writes the archive is `_CoreCreateIpa` (in `Xamarin.iOS.Common.targets`),
which depends on `Codesign` and is reached through `CreateIpa`. Because `$(BuildIpa)` is set by
`_PrePublish`, a run in which `Build` executes first leaves `_CoreCreateIpa` skipped while
`Publish` still prints its success line.

**Never accept that line, or exit code 0, as evidence that an `.ipa` exists. Confirm the file is
on disk.**

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
build ran here on Windows with no Mac. Producing an installable, distributable `.ipa` does not: it
needs a real signing identity (§10) and Apple's archiving tools. Treat §10-§11 as prerequisites of
a package, not as refinements of one you already have.

**Do not read the above as an endorsement of Windows-only iOS work.** Microsoft's own command-line
guidance documents **Pair to Mac** (`-p:ServerAddress`, `-p:ServerUser` and related properties) as
the supported route for building iOS from Windows, and its documented flow always supplies
`-p:CodesignKey` and `-p:CodesignProvision`. What this repository observed is the behaviour of the
unsigned, unpaired command — useful because it is the command people reach for first and the one
whose log misleads, not because it is a supported path to a shippable artefact.

## 10. Sign

To sign with a real distribution identity, supply `CodesignKey` and `CodesignProvision`, naming the
distribution certificate and provisioning profile you created for this app — **together with the
archive properties**:

```
dotnet publish -f net10.0-ios -c Release ^
  -p:ArchiveOnBuild=true ^
  -p:RuntimeIdentifier=ios-arm64 ^
  -p:CodesignKey="Apple Distribution: <Your Name or Org> (<Team ID>)" ^
  -p:CodesignProvision="<Provisioning Profile Name>"
```

**`ArchiveOnBuild=true` is not optional, and an earlier revision of this guide omitted it.**
Microsoft documents that property as the one that produces the `.ipa`. Without it the SDK never
reaches the target that writes the package, so the command signs a build and still leaves you with
no artefact — the same empty-publish-folder outcome §9 documents, reached by a longer route. The
ad hoc and enterprise guides in this repository have always carried both properties; this guide
now matches them.

Creating the distribution certificate itself is documented by Microsoft as a Visual-Studio-driven
step (**Tools > Options > Xamarin > Apple Accounts > Create Certificate > iOS Distribution**),
which exports the private key to Keychain Access on a paired Mac build host. **This repository did
not execute this step** — it requires a real Apple Developer Program identity and, per Microsoft's
own current documentation, a Mac build host paired to Visual Studio. This is the credentials and
tooling limitation this guide names plainly, not an unstated one.

## 11. Package

Run with **both** a real signing identity **and** the archive properties — the full command is in
§10 — and `dotnet publish` (or Visual Studio's own Archive/Distribute flow) produces the `.ipa`
uploaded to App Store Connect.

**Two conditions, not one.** Signing alone does not yield a package, and `ArchiveOnBuild` alone
fails with `Code signing must be enabled to create an Xcode archive.` **No `.ipa` exists until
both are satisfied** — see the warning in §9. There is no unsigned intermediate package to inspect
on this platform, so the only proof is the file on disk.

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
| Signing mismatch on upload | Provisioning profile does not match the certificate or Bundle ID used to sign | Compare the profile's App ID and certificate against `CodesignProvision`/`CodesignKey` | Regenerate or select the correct profile, per §10 |
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

This section separates two different dates, because they mean different things and only one of
them can advance.

**Sources last verified: 2026-08-26.** Every claim resting on §19's sources was re-checked on that
date. That pass corrected §4's D-U-N-S and fee-waiver conditions, narrowed §5's privacy-manifest
scope to Apple's published SDK list, restated §5's SDK floor as an *upload* requirement, and
replaced §7's incorrect description of unsigned builds.

**Execution evidence: 2026-08-23.** The §9 build claims were verified by execution against this
repository's own sample application, including a clean-tree re-run that corrected an earlier,
incorrect claim that an `.ipa` had been produced. **That date does not advance when sources are
re-verified** — the run happened when it happened. Packaging and signing (§10-§11) are **not**
execution-verified.
