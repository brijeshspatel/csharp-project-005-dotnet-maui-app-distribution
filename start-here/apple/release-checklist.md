# iOS End-to-End Release Checklist

The authoritative execution path for releasing a .NET MAUI app to the Apple App Store, from
nothing configured to a verified public release.

**Work down the table in order.** Every row names what it depends on, what success looks like, and
how to prove it. Where a row needs more than a line of explanation, follow its link.

**Before you start:** [prerequisites overview](../prerequisites-overview.md) ·
[choose your channel](../choose-your-distribution-channel.md) ·
[Apple platform hub](../../platforms/apple/README.md)

## The sequence

| # | Phase | Action | Depends on | Expected result | How to verify | ☐ |
|--:|---|---|---|---|---|:-:|
| 1 | Prerequisites | Hold an active [Apple Developer Program](../../platforms/apple/app-store-public-release/README.md#4-eligibility) membership | — | Membership shows as active | Sign in to developer.apple.com and read the membership status | ☐ |
| 2 | Prerequisites | Install the [iOS 26 SDK / Xcode 26 workload](../../platforms/apple/app-store-public-release/README.md#5-prerequisites) | 1 | Toolchain matches Apple's current floor | `dotnet workload list` shows the iOS workload | ☐ |
| 3 | Application setup | [Fix the Bundle ID](../../platforms/apple/app-store-public-release/README.md#8-application-preparation) as `<ApplicationId>` in the `.csproj` | — | One identifier, and only one place holding it | Read `<ApplicationId>` from the `.csproj`. **Do not expect a Bundle ID in `Info.plist`** — single-project MAUI generates it, so there is nothing there to cross-check | ☐ |
| 4 | Signing | [Create a distribution certificate](../../platforms/apple/app-store-public-release/README.md#10-sign) | 1 | Certificate issued and installed | It appears in Keychain, and in Apple's Certificates list | ☐ |
| 5 | Signing | [Create an App ID and provisioning profile](../../platforms/apple/app-store-public-release/README.md#10-sign) matching steps 3 and 4 | 3, 4 | Profile references the right Bundle ID and certificate | Open the profile and read both values | ☐ |
| 6 | **Gate** | **Back up the certificate's private key** and record where the profile lives | 4, 5 | A recoverable copy exists off this machine | Restore it somewhere else and confirm it imports | ☐ |
| 7 | Build | `dotnet publish -f net10.0-ios -c Release` | 3 | Managed and AOT output compile | Read the exit code **and** see step 8 | ☐ |
| 8 | **Gate** | **Confirm no `.ipa` was produced, and understand why** | 7 | The publish folder is **empty** | `ls bin/Release/net10.0-ios/ios-arm64/publish/`. The build **prints that it created a package it did not write**. Never trust that line | ☐ |
| 9 | Signing | [Sign and archive](../../platforms/apple/app-store-public-release/README.md#10-sign) with `-p:ArchiveOnBuild=true -p:RuntimeIdentifier=ios-arm64` **and** `-p:CodesignKey`/`-p:CodesignProvision`. **Signing without the archive properties produces no package** | 5, 7 | A signed archive is produced | Exit code 0 is not enough — step 10 lists the file | ☐ |
| 10 | Package | [Produce and locate the signed `.ipa`](../../platforms/apple/app-store-public-release/README.md#11-package) | 9 | The file exists on disk | **List the file.** Do not read the build log | ☐ |
| 11 | Store setup | [Create the App Store Connect record](../../platforms/apple/app-store-public-release/README.md#12-configure-distribution-platform): name, language, Bundle ID, SKU | 3 | The app exists in App Store Connect | The Bundle ID matches step 3 exactly | ☐ |
| 12 | Deploy | [Upload the signed build](../../platforms/apple/app-store-public-release/README.md#13-deploy) via Transporter or Visual Studio, using an app-specific password | 10, 11 | Upload completes without error | The build appears in App Store Connect | ☐ |
| 13 | Validate | [Confirm the build processes](../../platforms/apple/app-store-public-release/README.md#14-validate) | 12 | Build reaches **Ready to Submit** | Read the build's status in App Store Connect | ☐ |
| 14 | Testing | [Internal TestFlight](../../platforms/apple/testflight/README.md): up to 100 testers, no review | 13 | Testers can install within minutes | A tester installs and launches the build | ☐ |
| 15 | Testing | [External TestFlight](../../platforms/apple/testflight/README.md) where used: up to 10,000 testers | 14, or 13 if skipping internal | Beta review passes for the first build added to the external group. Apple publishes no turnaround time — do not commit to a date | The build shows as approved for external testing | ☐ |
| 16 | **Gate** | **Confirm store readiness**: privacy manifest, App Privacy answers, age rating, listing metadata | 13 | Every item complete | Walk the App Store Connect checklist. **App Review rejects incomplete submissions** | ☐ |
| 17 | Release | [Submit for App Review](../../platforms/apple/app-store-public-release/README.md#13-deploy) | 16 | Submission accepted into review | Status changes to Waiting for Review | ☐ |
| 18 | Release | Handle the outcome. If rejected, fix the named issue and return to step 3, 7 or 16 | 17 | Approved, or a clear reason to fix | Read the resolution centre message. [Troubleshooting](../../platforms/apple/app-store-public-release/README.md#17-troubleshooting) | ☐ |
| 19 | Release | Release to the public | 18 | The app is live | The listing is reachable from a device that never had it | ☐ |
| 20 | Post-release | Verify the live listing | 19 | It downloads and launches | Install from the public App Store on a real device | ☐ |
| 21 | Post-release | [Plan the next update](../../platforms/apple/app-store-public-release/README.md#15-update) | 19 | Version **and** build number both increase | Compare against the released values before rebuilding | ☐ |

## The two gates that catch people

**Step 8 is the one that costs a day.** `dotnet publish` for iOS exits 0, reports 0 warnings, and
prints `Created the package: ...DistributionSample.ipa` while leaving the publish folder empty.
The SDK's `Publish` target emits that line whenever `BuildIpa` is set, and never invokes the target
that would create the file. **A signed `.ipa` needs a real Apple signing identity.** The log is not
evidence; the file is.

**Step 16 is the one that costs a week.** App Review rejects a submission with an incomplete
privacy manifest or missing App Privacy answers, and the wait restarts.

## If you are not shipping publicly

| You want | Go to |
|---|---|
| Beta testers only | [TestFlight](../../platforms/apple/testflight/README.md) |
| A fixed list of registered devices | [Ad hoc distribution](../../platforms/apple/ad-hoc-distribution/README.md) |
| Your own organisation only | [Business Manager and enterprise](../../platforms/apple/business-manager-and-enterprise/README.md) |
| The Android equivalent of this page | [Android release checklist](../android/release-checklist.md) |
