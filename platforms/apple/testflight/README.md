# TestFlight

## 1. What This Channel Is

TestFlight is Apple's beta-testing service, built into App Store Connect. It distributes a build
to testers before — or between — public App Store releases, without going through full App
Review.

## 2. When to Use It

Use TestFlight to validate a build with real users before a public release, or to gather feedback
on a specific new version before it replaces what is already live on the App Store.

## 3. When Not to Use It

Do not use TestFlight as a permanent distribution mechanism — builds expire after 90 days, and it
requires every tester to install the TestFlight app itself. For permanent public distribution, use
[Apple App Store public release](../app-store-public-release/README.md).

## 4. Eligibility

The same Apple Developer Program membership as public App Store release (see that guide's
[§4](../app-store-public-release/README.md#4-eligibility)) — TestFlight is part of the same App
Store Connect account, not a separate enrolment.

## 5. Prerequisites

Identical application-level prerequisites to public App Store release
([§5](../app-store-public-release/README.md#5-prerequisites)): Bundle ID, distribution
certificate, provisioning profile, current iOS SDK. TestFlight adds:

- A beta app description and beta app review information, required before external testers can
  be invited.
- Tester email addresses (internal) or a public link / email list (external).

## 6. How to Obtain the Prerequisites

Follow the public App Store release guide's [§6](../app-store-public-release/README.md#6-how-to-obtain-the-prerequisites)
for the certificate and provisioning profile — the same identity is used for both channels.

## 7. Security Model

Identical to public App Store release
([§7](../app-store-public-release/README.md#7-security-model)). TestFlight adds no separate
signing requirement; it re-signs an already-signed build for local execution on a tester's
device after upload.

## 8. Application Preparation

Identical to public App Store release ([§8](../app-store-public-release/README.md#8-application-preparation)).

## 9. Build

Identical command and result to public App Store release, verified by execution in that guide's
[§9](../app-store-public-release/README.md#9-build): `dotnet publish -f net10.0-ios -c Release`.
This guide does not re-run it.

**Read that section before you rely on a build.** That command **does not produce an `.ipa`** —
it exits 0 and prints a message saying it did. Producing one needs both a real signing identity
**and** the archive properties, as [§10](../app-store-public-release/README.md#10-sign) sets out;
signing alone is not sufficient. A TestFlight upload needs the same signed `.ipa` an App Store
submission needs, produced the same way. What differs
between the two channels is the upload destination and the review path (§12-§13), not the build.

## 10. Sign

Identical to public App Store release ([§10](../app-store-public-release/README.md#10-sign)) —
the same distribution certificate and provisioning profile. TestFlight does not have its own,
separate signing identity.

## 11. Package

Identical to public App Store release ([§11](../app-store-public-release/README.md#11-package)).

## 12. Configure Distribution Platform

Create the beta app description and beta app review information in App Store Connect's TestFlight
tab, on the same app record used for public release. Internal testers (up to 100, App Store
Connect team members) need no further configuration; external testers (up to 10,000) need a
public link or an email-invited group.

## 13. Deploy

Upload the build exactly as in public App Store release's [§13](../app-store-public-release/README.md#13-deploy).
**Internal testers** get access within minutes, no review.

**External testers may require beta review.** Apple's own framing: when you add the **first build
of your app to a group**, that build is sent to App Review; a review is required only for the
first build, and subsequent builds may not require a full review. Note this is scoped to the first
build added to a *group*, not to each version.

**Apple publishes no beta review turnaround time.** An earlier revision of this guide gave
"commonly 24 hours, reported as ranging 4-48 hours" — those figures could not be traced to any
first-party Apple source and have been removed rather than left standing. The only duration Apple
publishes is for App Store submissions, not TestFlight beta review. **Do not promise testers or
stakeholders any beta review duration**, and plan the schedule so that a slow review is an
inconvenience rather than a missed commitment.

## 14. Validate

Confirm the build appears in the TestFlight tab with status "Ready to Test" (internal) or after
beta review completes (external). Confirm testers received their invitation and can install via
the TestFlight app.

## 15. Update

Upload a new build under the same or a new version; each build is independently listed and
independently expires. Internal testers see new builds immediately; a new external build may
need its own beta review pass under the same rules as §13.

## 16. Revoke / Withdraw / Retire

Remove a tester from the internal or external group to end their access. A build stops being
installable to new testers automatically after 90 days from upload; existing installs are not
force-removed from tester devices.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| Build never appears for external testers | Beta app review not yet complete, or beta app description missing | Check the TestFlight tab's build status | Complete the beta app description/review information (§12) and wait for review |
| Tester cannot install | Tester has not accepted the TestFlight invitation, or does not have the TestFlight app | Confirm invitation acceptance in App Store Connect | Re-send the invitation; confirm the tester installed the TestFlight app itself |
| Build missing after 90 days | Automatic expiry | Check the build's upload date | Upload a new build; this is expected behaviour, not a defect |

## 18. Limitations

**Beta review timing for external testers is unknown, not merely unguaranteed.** Apple publishes
no turnaround figure for it, so this guide gives none — an earlier revision quoted publicly
reported ranges, which are removed because they had no first-party source. Plan for a review of
unknown duration. This guide did not execute an upload to a real App Store Connect account. The build step it relies on was verified by execution in the public App Store release
guide, which this guide deliberately does not duplicate; **the signing and packaging steps were
not**, and no `.ipa` was produced in any run of this repository. See that guide's §9 and §18.

## 19. Official Sources

- [TestFlight — Apple Developer](https://developer.apple.com/testflight/)
- [Add internal testers — App Store Connect Help](https://developer.apple.com/help/app-store-connect/test-a-beta-version/add-internal-testers)
- [Invite external testers — App Store Connect Help](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers)
- [Publish a .NET MAUI iOS app for App Store distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-app-store?view=net-maui-10.0)

## 20. Last Verified

**Sources last verified: 2026-08-26.** That pass removed the beta review duration figures formerly
given in §13 — they could not be traced to any first-party Apple source — and restated Apple's own
scoping of beta review to the first build added to a tester *group*.

**Execution evidence: 2026-08-23.** The build claim was verified by execution in the public App
Store release guide on that date and is not re-executed here; **that date does not advance when
sources are re-verified**. The sign and package claims are **not** execution-verified in either
guide.
