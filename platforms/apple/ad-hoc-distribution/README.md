# Ad Hoc Distribution

## 1. What This Channel Is

Ad hoc distribution installs a signed build directly onto a fixed list of iOS devices that you
registered in advance in your Apple Developer account. The build carries an **ad hoc distribution
provisioning profile**, which embeds the device list. A device that is not in that list cannot run
the build.

It does not use the App Store, and it does not go through App Review.

## 2. When to Use It

Use ad hoc distribution when you must put a release-configuration build on specific, known devices
and TestFlight does not fit. Two cases are common:

- Testing with a group whose devices you control, where you do not want a tester to install the
  TestFlight app or accept an invitation.
- Distributing inside a company where App Store Connect is not an option.

## 3. When Not to Use It

**Do not use ad hoc distribution for general beta testing.** [TestFlight](../testflight/README.md)
is the better channel: it does not consume device registration slots, it does not require you to
collect device identifiers, and it distributes to far more testers.

**Do not use it for public distribution.** Use
[App Store public release](../app-store-public-release/README.md).

**Do not use it as a way to avoid App Review for a shipping product.** The device limit in §4 makes
that impractical, and the registration slots do not reset when you want them to (§4).

## 4. Eligibility

Ad hoc distribution is available to the **Apple Developer Program** and the **Apple Developer
Enterprise Program**. The Apple Developer Program membership is the same one described in the
[App Store guide's §4](../app-store-public-release/README.md#4-eligibility) — no separate
enrolment.

**The device limit governs this channel more than anything else.**

**WARNING — two different device limits are published, and the stricter reading is not the
correct one.** Microsoft's .NET MAUI documentation states ad hoc distribution is "limited to 100
devices per membership year, for both development and distribution". **Apple's own documentation
states the limit is 100 devices _per product family_, per membership year** — a separate 100 for
each of Apple TV, Apple Vision Pro, Apple Watch, iPad, iPhone, iPod touch and Mac. Apple is the
authority on its own programme. Plan against Apple's figure, and be aware that summaries of it
elsewhere are frequently wrong.

**Registration slots do not behave the way most people assume:**

| Behaviour | What actually happens |
|---|---|
| Disabling a device you no longer use | **Does not** free a slot. The disabled device still counts against the 100 |
| Removing a device mid-year | Slots are reclaimed only at membership renewal, not on demand |
| At renewal | Account Holders, Admins and App Managers may remove specific devices, or remove all of them, restoring the full 100 per product family. New devices can be added after that removal is completed |
| 30 days before membership expiry | You may download the registered device list, and optionally remove all devices immediately |
| 180 days after membership expiry | All devices are removed automatically if you did not act |

**Plan the device list before you start registering.** A slot spent on a device you no longer test
with is a slot you cannot recover until renewal.

## 5. Prerequisites

| Prerequisite | Notes |
|---|---|
| Apple Developer Program membership | Same membership as App Store release. See [App Store §5](../app-store-public-release/README.md#5-prerequisites) |
| A distribution certificate | The same certificate type used for App Store release. One certificate serves both channels |
| An App ID | May be the same App ID used for development and for App Store release |
| The UDID of every target device | Collected per device, before the provisioning profile is created |
| An **ad hoc** distribution provisioning profile | Distinct from the App Store profile. It embeds the device list |
| A Mac, or a Mac build host paired to Visual Studio | Required to produce a signed `.ipa`. See §10 |
| Apple Configurator, on a Mac | Required for the installation route this guide **documents** — no installation was executed here, see §18. See §13 |

## 6. How to Obtain the Prerequisites

The certificate and App ID steps are identical to App Store release; follow
[App Store §6](../app-store-public-release/README.md#6-how-to-obtain-the-prerequisites) rather than
repeating them here. Two steps are specific to this channel.

**Register each device.** You need the device's name and its Unique Device Identifier (UDID). The
required account role is **Account Holder** or **Admin**.

1. Connect the device to a Mac with a cable.
2. Open Xcode, then **Window > Devices and Simulators**.
3. Select the **Devices** tab, then select the device.
4. Copy the **Identifier** value.
5. In a browser, open **Certificates, Identifiers & Profiles > Devices** in your Apple Developer
   account, and select the add button.
6. Set the correct **Platform**, give the device a name, and paste the identifier into
   **Device ID (UDID)**. Select **Continue**.
7. Review the information, then select **Register**.

Xcode and Xcode Server can also register a connected device automatically.

**Create the ad hoc provisioning profile.** In **Certificates, Identifiers & Profiles > Profiles**,
add a profile, and select **Ad Hoc** — not App Store. Select your App ID, then your distribution
certificate, then **select the devices this build may install on**. Name the profile and generate
it. Record the name: §10 needs it.

## 7. Security Model

Ad hoc distribution uses the **same distribution certificate** as App Store release, so the
identity model in [App Store §7](../app-store-public-release/README.md#7-security-model) applies
unchanged, including the consequences of losing the private key.

**What differs is what the provisioning profile authorises.** An App Store profile authorises
Apple to distribute the app. An ad hoc profile authorises **a specific, enumerated set of devices**
to run it. The device list is embedded in the profile at generation time, which has one consequence
that governs day-to-day use:

**Adding a device later does not update a profile you already generated.** You must regenerate
the profile with the new device included, then re-sign and redistribute the build. There is no way
to authorise a new device against an already-distributed ad hoc build.

An ad hoc build is signed with a **real distribution identity**. Despite the shared adjective, it
has nothing to do with *ad hoc code signing* (`codesign -s -`), which the .NET SDK applies only to
simulator builds and which never produces a distributable package. The App Store guide's
[§9](../app-store-public-release/README.md#9-build) records a build that produced **no package at
all** — the absence of a signed artefact, not the presence of a self-signed one.

## 8. Application Preparation

Identical to [App Store §8](../app-store-public-release/README.md#8-application-preparation): set
the **Application ID** property to your Bundle ID, and set the display version and build number.
The Bundle ID must match the App ID in the ad hoc provisioning profile.

## 9. Build

**This channel's build cannot be completed in this repository's environment, and this guide does
not claim otherwise.** What was executed, and what it proves, is set out below.

Producing an ad hoc `.ipa` requires the archive form of the publish command:

```
dotnet publish -f net10.0-ios -c Release -p:ArchiveOnBuild=true -p:RuntimeIdentifier=ios-arm64
```

**Verified by execution, 2026-08-24**, against this repository's own sample application — a re-run
of the same command the [App Store guide](../app-store-public-release/README.md#9-build) executed
on 2026-08-23, repeated here because this channel depends on it rather than merely referencing it.
Both runs produced the same result. This command **fails**, correctly and immediately, with:

```
error : Code signing must be enabled to create an Xcode archive.
```

That is the expected and correct result without a signing identity. It also demonstrates the
essential difference from the App Store guide's §9: **there is no unsigned ad hoc package to
inspect.** Signing is a prerequisite of producing the artefact, not a step applied afterwards.

**Do not fall back to `dotnet publish -f net10.0-ios -c Release` and assume you have a package.**
That command exits 0 and prints `Created the package: ...DistributionSample.ipa` while writing no
file at all. The cause is documented in the
[App Store guide's §9](../app-store-public-release/README.md#9-build). **Always list the output
directory.**

## 10. Sign

Supply the distribution certificate and the **ad hoc** provisioning profile created in §6:

```
dotnet publish -f net10.0-ios -c Release ^
  -p:ArchiveOnBuild=true ^
  -p:RuntimeIdentifier=ios-arm64 ^
  -p:CodesignKey="Apple Distribution: <Your Name or Org> (<Team ID>)" ^
  -p:CodesignProvision="<Ad Hoc Provisioning Profile Name>"
```

`CodesignProvision` takes the profile **name**, as recorded in §6. **The distribution channel is
determined by the provisioning profile, not by a command-line switch** — the same command with an
App Store profile produces an App Store build. Selecting the wrong profile is the most common way
to produce a build that installs nowhere.

These properties may also be set in a `<PropertyGroup>` in the project file, conditioned on the
iOS target framework and the Release configuration. A command-line value takes precedence over the
project file.

**Building from Windows requires a network-accessible Mac.** Apple's build tools run only on macOS.
Add these to the command, or supply them from a secret store rather than the project file:

| Parameter | Value |
|---|---|
| `-p:ServerAddress` | IP address of the Mac build host |
| `-p:ServerUser` | System username on that host |
| `-p:ServerPassword` | Password for that user. Omit it to use saved SSH keys |
| `-p:TcpPort` | `58181` |
| `-p:_DotNetRootRemoteDirectory` | `/Users/{macOS username}/Library/Caches/Xamarin/XMA/SDKs/dotnet/` |

**Never commit `ServerPassword`, a certificate, or a profile to source control.**

## 11. Package

A successful signed build writes the `.ipa` to
`bin/Release/net10.0-ios/ios-arm64/publish/`. **Confirm the file is on disk by listing that
directory.** Do not accept the build log's own message as evidence — see §9.

Visual Studio's **Archive Manager > Distribute > Ad Hoc** flow produces the same artefact through
a dialog rather than the command line, and asks for the signing identity and profile at the point
of export.

## 12. Configure Distribution Platform

**There is no distribution platform to configure.** This is the defining operational property of
this channel: no App Store Connect record, no upload, no review queue, and no server-side state of
any kind. The provisioning profile you embedded at signing time is the entire distribution control
mechanism.

The practical consequence is that **everything this channel needs, it needs before signing.** Once
the `.ipa` exists, its device list is fixed.

## 13. Deploy

Install the `.ipa` with **Apple Configurator** on a Mac, with the target device connected by USB or
Thunderbolt:

1. Connect the device to the Mac.
2. In Apple Configurator, select the device or devices.
3. Select the add button in the toolbar, then **Apps** — or drag the `.ipa` onto the selected
   devices.
4. Navigate to the folder holding your `.ipa`, select it, then select **Add Apps**.

Apple Configurator installs onto iPhone, iPad and Apple TV. Apple TV connects wirelessly rather
than by cable, and requires Wi-Fi plus Ethernet.

A build may only install on a device whose UDID is in the embedded profile. Installation onto any
other device fails, by design.

## 14. Validate

Confirm three things, in this order:

1. **The `.ipa` exists on disk** at the path in §11. List the directory.
2. **The app installs** onto a registered device through Apple Configurator without error.
3. **The app launches and runs** on that device. An ad hoc build that installs but immediately
   closes usually indicates a provisioning or entitlement mismatch — see §17.

Confirm installation on at least one device that was registered late in the process, if any were.
That is the case most likely to reveal a stale provisioning profile.

## 15. Update

Increment the build number, then rebuild, re-sign and redistribute. Every recipient must install
the new `.ipa` through the same route; there is no update notification and no automatic delivery.

**If the device list changed, regenerate the provisioning profile first** (§7). A rebuild against
the old profile silently produces a build the new devices cannot install.

## 16. Revoke / Withdraw / Retire

Ad hoc distribution has **no remote withdrawal mechanism.** A build already installed on a device
stays there until someone removes it from that device.

The available controls are indirect:

| Control | Effect |
|---|---|
| Revoking the distribution certificate | Invalidates the signing identity. Existing installs are affected, and every profile that used the certificate must be regenerated. This also affects App Store builds signed with the same certificate |
| Letting the provisioning profile expire | Ad hoc profiles expire. The app stops launching on expiry |
| Disabling a device in the account | Prevents future profile inclusion. **Does not** free a device slot (§4) |

**Certificate revocation is not a targeted tool.** It affects every build signed with that
certificate, across every channel. Do not use it to withdraw one ad hoc build.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| `error : Code signing must be enabled to create an Xcode archive.` | `ArchiveOnBuild=true` with no signing identity | Check whether `CodesignKey` and `CodesignProvision` are supplied | Supply both, per §10 |
| Build reports `Created the package: ...ipa` but no file exists | The plain publish command was used; the SDK prints this unconditionally | List the publish directory; it is empty | Use the archive form with signing, per §9-§10 |
| App will not install on a device | The device's UDID is not in the embedded provisioning profile | Compare the device UDID against the profile's device list | Register the device, regenerate the profile, re-sign, redistribute |
| A newly registered device still cannot install | The profile was generated before the device was registered | Check the profile's generation date against the registration date | Regenerate the profile and re-sign. Adding a device never updates an existing profile |
| App installs, then closes immediately on launch | Provisioning profile or entitlement mismatch | Check that the App ID capabilities match the app's entitlements | Align the App ID capabilities and `Entitlements.plist`, regenerate the profile, rebuild |
| Cannot register any more devices | The product family's 100-device limit is reached | Check the device count for that product family | Wait for membership renewal and remove devices then. Disabling does not free a slot |
| Build from Windows fails to reach the Mac | Pair to Mac is not configured or unreachable | Confirm the Mac host address, user and port `58181` | Correct the `Server*` parameters, per §10 |

## 18. Limitations

**This guide is documented, not demonstrated, from §10 onward.** The only step verified by
execution is that the archive command fails without a signing identity (§9). Producing a signed ad
hoc `.ipa`, registering a real device, generating a real ad hoc profile, and installing through
Apple Configurator all require an enrolled Apple Developer Program identity, real devices and a
Mac. **None of those were available in this run, and none of them are claimed as verified.** Every
claim in §10-§16 rests on the sources in §19.

**Over-the-air installation is out of scope here.** An ad hoc build can also be installed from a
web server through a manifest and an `itms-services` link. That route was **not** verified against
a current first-party Apple source in this run, so it is named for completeness and deliberately
not documented as a procedure. Treat any third-party description of it as unverified.

**The device limit is the practical ceiling on this channel**, and §4 records a published
discrepancy about what that limit is. Verify the current figure against Apple's own page before
planning around it.

## 19. Official Sources

- [Publish a .NET MAUI iOS app for ad-hoc distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-ad-hoc?view=net-maui-10.0)
- [Publish a .NET MAUI iOS app using the command line — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-cli?view=net-maui-10.0)
- [Devices overview — Apple Developer Account Help](https://developer.apple.com/help/account/devices/devices-overview/)
- [Register a single device — Apple Developer Account Help](https://developer.apple.com/help/account/devices/register-a-single-device/)
- [Add apps to a device in Apple Configurator for Mac — Apple Support](https://support.apple.com/guide/apple-configurator-mac/add-apps-to-a-device-cad4cd08c03/mac)

## 20. Last Verified

**Sources last verified: 2026-08-26.** Every claim was re-checked against the sources in §19 on
that date. That pass updated two §19 URLs to Apple's canonical `/help/account/devices/` locations
after Apple reorganised those pages, and corrected §7's description of ad hoc *code signing*.

**Execution evidence: 2026-08-24.** The §9 build failure was verified by execution against this
repository's own sample application on that date; **that date does not advance when sources are
re-verified**. Signing, packaging, device registration and installation are **not**
execution-verified; see §18.
