# Android End-to-End Release Checklist

The authoritative execution path for releasing a .NET MAUI app to Google Play, from nothing
configured to a verified public release.

**Work down the table in order.** Every row names what it depends on, what success looks like, and
how to prove it. Where a row needs more than a line of explanation, follow its link.

**Before you start:** [prerequisites overview](../prerequisites-overview.md) ·
[choose your channel](../choose-your-distribution-channel.md) ·
[Android platform hub](../../platforms/android/README.md)

## The sequence

| # | Phase | Action | Depends on | Expected result | How to verify | ☐ |
|--:|---|---|---|---|---|:-:|
| 1 | Prerequisites | Register a [Google Play Console developer account](../../platforms/android/google-play-public-release/README.md#4-eligibility) (one-time US $25) and complete identity verification | — | Account verified | The Play Console shows the account as verified | ☐ |
| 2 | **Gate** | **Decide whether the 14-day closed-test requirement applies.** It does for a personal account created after 2023-11-13 | 1 | You know your timeline before you build, not after | Read the account type and creation date in Play Console. This changes step 14, not just the end | ☐ |
| 3 | Prerequisites | [Confirm the target API level](../../platforms/android/google-play-public-release/README.md#5-prerequisites): **API 36 from 2026-08-31**, API 35 until then, with an extension to 2026-11-01 available via Play Console's **Policy status** page. The floor rises annually | — | Target matches Google's current floor | Check the floor before building; it moves annually | ☐ |
| 4 | Application setup | [Fix the package name](../../platforms/android/google-play-public-release/README.md#8-application-preparation) as the Application ID | — | One identifier, permanent after first publish | Read it from the `.csproj` | ☐ |
| 5 | Application setup | [Set the version name and version code](../../platforms/android/google-play-public-release/README.md#8-application-preparation) | — | Both higher than any prior release | Compare against the last released values | ☐ |
| 6 | Build | `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false`, run at the project's **real path** | 3, 4, 5 | Build succeeds | Read the exit code, **then** step 7 | ☐ |
| 7 | **Gate** | **Confirm the `.aab` exists on disk** | 6 | A real App Bundle file, with a size | `ls bin/Release/net10.0-android/publish/`. Do not accept the build log as proof | ☐ |
| 8 | Signing | [Create and protect an upload keystore](../../platforms/android/google-play-public-release/README.md#7-security-model) | — | Keystore exists, backed up, never committed | Confirm it is outside the repository and in `.gitignore` | ☐ |
| 9 | Signing | [Sign for real release](../../platforms/android/google-play-public-release/README.md#10-sign) with the `AndroidSigningKeyStore` properties | 6, 8 | A signed App Bundle | `keytool -printcert` shows the intended certificate | ☐ |
| 10 | Package | [Confirm the signed `.aab`](../../platforms/android/google-play-public-release/README.md#11-package). Google Play requires the App Bundle, not an `.apk` | 9 | `.aab` present, `.apk` not required | List the file and read its size | ☐ |
| 11 | Store setup | [Create the app listing](../../platforms/android/google-play-public-release/README.md#12-configure-distribution-platform): name, language, category, free or paid | 4 | Listing exists with the right package name | The package name matches step 4 exactly | ☐ |
| 12 | **Gate** | **Complete store readiness**: store listing, content rating questionnaire, Data safety declaration | 11 | All three complete | **Play Console blocks production publishing while any is incomplete** | ☐ |
| 13 | Testing | Run an [internal test](../../platforms/android/google-play-internal-testing/README.md) — fastest feedback, up to 100 testers | 10 | Testers install from the internal track | A tester installs and launches the build | ☐ |
| 14 | Testing | If step 2 applies, complete the [closed test](../../platforms/android/google-play-closed-testing/README.md): 12 opted-in testers, 14 continuous days | 2, 10 | Production access granted | Play Console shows production access unlocked | ☐ |
| 15 | Deploy | [Upload the `.aab`](../../platforms/android/google-play-public-release/README.md#13-deploy) for the first release. Doing it by hand in Play Console is a deliberate slow-down at an irreversible step, not a platform rule — the Play Developer API can upload too | 10, 12, and 14 where it applies | Upload accepted; Play App Signing configured and the upload key fixed | The release shows your App Bundle | ☐ |
| 16 | Validate | [Confirm the pre-launch checks](../../platforms/android/google-play-public-release/README.md#14-validate) | 15 | Release reaches **Ready to publish** | Read the release status and the pre-launch report | ☐ |
| 17 | Release | Submit for review | 16 | Submission accepted | Status changes to In review | ☐ |
| 18 | Release | Handle the outcome. If rejected, fix the named policy issue and return to step 5, 6 or 12 | 17 | Approved, or a clear reason to fix | Read the policy message. [Troubleshooting](../../platforms/android/google-play-public-release/README.md#17-troubleshooting) | ☐ |
| 19 | Release | Release to production | 18 | The app is live | The listing is reachable from a device that never had it | ☐ |
| 20 | Post-release | Verify the live listing | 19 | It downloads and launches | Install from the public Play Store on a real device | ☐ |
| 21 | Post-release | [Plan the next update](../../platforms/android/google-play-public-release/README.md#15-update) | 19 | Version code increases | Compare against the released value before rebuilding | ☐ |

## The two gates that catch people

**Step 6 fails from a clean tree without the marshal-methods property.** `dotnet publish` for
Android exits with `XAGNM7009 ... missing native code generation state`. Adding
`-p:AndroidEnableMarshalMethods=false` makes it succeed and write a real `.aab`. This is a
**mitigation, not a recommendation** — the property disables a startup optimisation. A long project
path can also fail this step: Microsoft documents `APT2264` as the maximum-path-length error, and a
long path may also surface as the more generic `APT2098` or `APT2261`.

**Step 2 decides your timeline, and it is easy to read too late.** A personal account created after
2023-11-13 needs 12 opted-in testers running a closed test for 14 continuous days *before*
production access. The clock is per tester and continuous; a tester who opts out restarts theirs.

## If you are not shipping publicly

| You want | Go to |
|---|---|
| Fast feedback from a trusted few | [Internal testing](../../platforms/android/google-play-internal-testing/README.md) |
| A larger invited group | [Closed testing](../../platforms/android/google-play-closed-testing/README.md) |
| Anyone who opts in | [Open testing](../../platforms/android/google-play-open-testing/README.md) |
| Your own organisation only | [Managed Google Play](../../platforms/android/managed-google-play-enterprise/README.md) |
| No store at all | [Direct APK distribution](../../platforms/android/direct-apk-distribution/README.md) |
| The iOS equivalent of this page | [iOS release checklist](../apple/release-checklist.md) |
