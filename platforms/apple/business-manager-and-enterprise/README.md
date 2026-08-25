# Apple Business Manager and Enterprise Distribution

## 1. What This Channel Is

This channel covers the two ways to distribute an iOS app privately to an organisation, without
listing it publicly on the App Store. **They are different products with different rules, and this
guide keeps them apart deliberately.**

| Route | What it is | Who runs distribution |
|---|---|---|
| **Custom Apps** through Apple Business Manager | A private app record in App Store Connect, made visible only to organisations you name. Apple hosts and delivers it | Apple, through the recipient's Apple Business Manager |
| **In-house distribution** through the Apple Developer Enterprise Program | A build signed with an in-house distribution certificate, distributed by you to your own employees | You, through your own website or MDM |

**WARNING — these are not interchangeable, and Apple enforces the difference.** Apple states the
Apple Developer Enterprise Program is **not permitted** for an app whose need could be met by
public App Store distribution, Apple Business custom apps, ad hoc distribution, or TestFlight.
Choosing the Enterprise Program to avoid App Review is a rejected application, not a shortcut.

## 2. When to Use It

**Use Custom Apps when** you supply an app to one or more organisations that are not your own
employer — a client, a partner, a franchise network — or when you want Apple to handle hosting,
delivery and updates. This is the route Apple expects for most private distribution.

**Use in-house distribution when** the app is proprietary to your own organisation, is used only by
your own employees, and genuinely cannot be served by any other route.

## 3. When Not to Use It

**Do not use either route for the general public.** Use
[App Store public release](../app-store-public-release/README.md).

**Do not use either for beta testing.** Use [TestFlight](../testflight/README.md).

**Do not use in-house distribution to reach a small set of known devices.** Use
[ad hoc distribution](../ad-hoc-distribution/README.md), which needs no separate programme.

**Do not apply to the Enterprise Program to skip App Review.** See the warning in §1.

## 4. Eligibility

### Custom Apps

The standard **Apple Developer Program** membership, the same one described in the
[App Store guide's §4](../app-store-public-release/README.md#4-eligibility). No separate
enrolment, and no separate certificate.

Setting a distribution method requires the **Account Holder**, **Admin** or **App Manager** role
in App Store Connect.

### Apple Developer Enterprise Program

Substantially harder to obtain. An organisation must meet **all** of these:

| Requirement | Detail |
|---|---|
| Size | 100 or more employees |
| Legal status | A legal entity. Not a DBA, fictitious business, trade name or branch |
| D-U-N-S Number | The nine-digit Dun & Bradstreet business identifier |
| Website | A publicly available site on a domain associated with the organisation |
| Security | Systems that restrict internal-use app downloads to employees, and that protect credentials and assets |
| Verification | Pass Apple's verification interview, and a continuous evaluation process afterwards |

The applicant must have legal authority to bind the organisation — the owner or founder, an
executive team member, a senior project lead, or someone with delegated legal authority.

**Cost: US $299 per membership year**, against US $99 for the standard Apple Developer Program.

**A separate Apple Account is required** if you are already enrolled in the standard Apple
Developer Program. The two memberships cannot share one account.

**Renewal triggers re-verification** of the organisation. Apple may reject an application at its
sole discretion.

## 5. Prerequisites

| Prerequisite | Custom Apps | In-house |
|---|---|---|
| Programme membership | Apple Developer Program | Apple Developer Enterprise Program |
| Distribution certificate | Standard Apple distribution certificate | **In-house** distribution certificate |
| App ID | Yes | Yes |
| Provisioning profile type | App Store | **In House** |
| App Store Connect access | Yes | **No — enterprise members have none** |
| Device registration | Not required | Not required |
| Recipient's Organization ID | Required, from their Apple Business Manager | Not applicable |
| Your own hosting or MDM | Not required | **Required** |
| Mac, or paired Mac build host | Required to sign | Required to sign |

## 6. How to Obtain the Prerequisites

The distribution certificate and App ID steps match the App Store guide's
[§6](../app-store-public-release/README.md#6-how-to-obtain-the-prerequisites), with one difference
for in-house: the provisioning profile is created by selecting **In House**, not App Store and not
Ad Hoc. An in-house profile contains an App ID and a distribution certificate, and — unlike an ad
hoc profile — **no device list**.

**For Custom Apps, obtain each recipient's Organization ID.** The recipient finds it in their own
Apple Business Manager account and gives it to you. You cannot look it up.

## 7. Security Model

Both routes use a distribution certificate, so the identity model in the
[App Store guide's §7](../app-store-public-release/README.md#7-security-model) applies, including
what losing the private key costs.

**What differs is who controls reach.**

- **Custom Apps.** Apple enforces the boundary. The app is visible only inside the Apple Business
  Manager accounts you named. You cannot over-distribute by accident, and a recipient cannot pass
  it on.
- **In-house.** **You** enforce the boundary. The provisioning profile places no limit on which
  devices may install the build — that is the point of the programme, and it is also the risk.
  Anyone who obtains the `.ipa` and the profile can install it. Apple's eligibility criteria
  require you to operate systems that prevent this, which is why §4 asks for them.

**An in-house build has no technical device restriction whatsoever.** Treat the `.ipa` as a
credential. Serve it only over authenticated HTTPS or through MDM, never from an open URL.

## 8. Application Preparation

Identical to [App Store §8](../app-store-public-release/README.md#8-application-preparation).

**For Custom Apps, one extra obligation applies.** Apple must sign in and operate the app to
review it. Prepare a working demo account and, where the app handles sensitive or proprietary
data, sample data that is safe to expose. An app the reviewer cannot enter is rejected.

## 9. Build

The build command is the same as every other Apple channel; only the provisioning profile differs.
See the [App Store guide's §9](../app-store-public-release/README.md#9-build) for what was verified
by execution, and note its warning in full:

**`dotnet publish -f net10.0-ios -c Release` produces no `.ipa`.** It exits 0 and prints
`Created the package: ...` while writing nothing. Producing a package requires code signing. This
guide did not produce an `.ipa`; see §18.

## 10. Sign

Supply the distribution certificate and the profile for the route you chose:

```
dotnet publish -f net10.0-ios -c Release ^
  -p:ArchiveOnBuild=true ^
  -p:RuntimeIdentifier=ios-arm64 ^
  -p:CodesignKey="Apple Distribution: <Your Organisation> (<Team ID>)" ^
  -p:CodesignProvision="<App Store profile, or In House profile>"
```

**The provisioning profile decides the channel.** An In House profile produces an in-house build;
an App Store profile produces a build you upload to App Store Connect, which is what a Custom App
requires. The command does not otherwise change.

Building from Windows requires a paired Mac build host, with the `Server*` parameters described in
the [ad hoc guide's §10](../ad-hoc-distribution/README.md#10-sign).

## 11. Package

A signed build writes the `.ipa` to `bin/Release/net10.0-ios/ios-arm64/publish/`. **List the
directory to confirm it exists**; the build log is not evidence (§9).

Visual Studio's Archive Manager offers **Distribute > Enterprise** for the in-house route, and
**Distribute > App Store** for a Custom App.

## 12. Configure Distribution Platform

### Custom Apps

1. Create the app record in App Store Connect, as for a public release.
2. Under **App Distribution Methods**, select **Private**.
3. Set **Type** to **Organization ID**, then enter each recipient organisation's ID. Choose
   **Apple Account** instead only for a business still on the legacy Volume Purchase Program.
4. Submit the build for review.

**WARNING — this choice is close to irreversible.** Once the app is approved, the distribution
method cannot be changed. Moving between private and public requires **creating a new app record
and resubmitting the binary**, which means a new App Store Connect record and a fresh review. The
only permitted post-approval change is public to unlisted.

### In-house

**There is no platform to configure. Enterprise Program members have no App Store Connect access
at all.** You are the distributor. Prepare a manifest alongside the `.ipa` and host both, or hand
both to your MDM.

## 13. Deploy

### Custom Apps

Apple delivers the app. After approval it appears in the **Apps and Books** section of each named
organisation's Apple Business Manager. Their IT team assigns it exactly as they assign an App Store
app, including device-based assignment and managed-app behaviour. **No individual purchase is
required.**

### In-house

Distribute the `.ipa` yourself, by either route Apple documents:

- **A secure website**, serving the `.ipa` and its manifest over HTTPS, behind authentication.
- **Mobile Device Management**, which is the route to prefer at any scale.

Both require the app to be prepared for distribution, including the manifest.

## 14. Validate

**Custom Apps.** Confirm the app record shows **Private** before submission. After approval,
confirm with one recipient that it appears in their Apple Business Manager, and that a device
assignment installs it.

**In-house.** Confirm the `.ipa` exists on disk (§11). Confirm installation on a device that is
**not** a registered development device — an in-house build must install anywhere inside your
organisation, and testing only on a registered device proves nothing about that.

Confirm in both cases that the app launches and runs, not merely that it installs.

## 15. Update

**Custom Apps.** Increment the build number and submit a new version. **Every updated version goes
through App Review again**, typically one to two days.

**In-house.** Increment the build number, rebuild, re-sign, and replace the hosted artefact or push
through MDM. There is no review. There is also no automatic update: a device keeps the installed
version until something replaces it.

## 16. Revoke / Withdraw / Retire

**Custom Apps.** Remove an organisation from the private distribution list, or remove the app from
sale. Apple stops delivering it. Copies already installed are unaffected.

**In-house.** Withdrawal is yours to perform, and the tools are blunt:

| Control | Effect |
|---|---|
| Withdraw the hosted artefact | Stops new installations. Does nothing to existing ones |
| Remove through MDM | Removes the app from managed devices. The only targeted control available |
| Let the provisioning profile expire | The app stops launching everywhere, on a date you do not choose precisely |
| Revoke the distribution certificate | Invalidates every build signed with it, across every app |

**Without MDM there is no reliable way to remove an in-house app from a device.** Decide this
before distributing, not afterwards.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| Enterprise Program application rejected | The need is met by App Store, Custom Apps, ad hoc or TestFlight; or an eligibility criterion in §4 is unmet | Re-read §4 against your organisation | Use Custom Apps instead. That is the route Apple expects |
| Cannot enrol — the Apple Account is already in use | The account is already in the standard Apple Developer Program | Check the account's existing memberships | Enrol with a different Apple Account, per §4 |
| Custom App rejected: reviewer could not sign in | No working demo account, or the app needs data the reviewer has no access to | Check the rejection message for the sign-in step reached | Supply a demo account and safe sample data, per §8 |
| Custom App not visible to the recipient | Wrong Organization ID, or the app is not yet approved | Confirm the ID against the one the recipient supplied, and check the app's review state | Correct the ID and resubmit if needed |
| Need to make a private app public, or the reverse | The distribution method is fixed at approval | Check the app record's current method | Create a new app record and resubmit the binary. The existing record cannot be converted |
| In-house app installs, then will not launch | Provisioning profile expired, or the certificate was revoked | Check the profile's expiry date and the certificate's state | Regenerate the profile, re-sign, redistribute |
| In-house app installs on devices outside the organisation | Expected. There is no device restriction | Confirm how the artefact is served | Put the download behind authentication or MDM, per §7 |

## 18. Limitations

**Nothing in this guide was executed.** No Apple Developer Enterprise Program membership, no Apple
Business Manager organisation, and no recipient organisation were available in this run. The build
and signing commands are the same ones the
[App Store](../app-store-public-release/README.md#9-build) and
[ad hoc](../ad-hoc-distribution/README.md#9-build) guides cover, and only their documented failure
without a signing identity is execution-verified. **Every claim in §4-§16 rests on the sources in
§19.**

**The manifest format for in-house web distribution is not documented here.** Apple documents it in
the deployment guide cited in §19. It was not verified in this run, and reproducing it from memory
would risk an incorrect specification.

**Enterprise Program eligibility is assessed by Apple, not by a checklist.** §4 lists the published
criteria. Meeting them does not guarantee acceptance, and Apple states it may reject an
application at its sole discretion.

## 19. Official Sources

- [Publish a .NET MAUI iOS app for in-house distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/ios/deployment/publish-in-house?view=net-maui-10.0)
- [Apple Developer Enterprise Program](https://developer.apple.com/programs/enterprise/)
- [Set distribution methods — App Store Connect Help](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/set-distribution-methods/)
- [Distribute Custom Apps to Apple devices — Apple Support](https://support.apple.com/guide/deployment/distribute-custom-apps-dep0113f6e18/web)
- [Distribute proprietary in-house apps to Apple devices — Apple Support](https://support.apple.com/guide/deployment/depce7cefc4d/web)

## 20. Last Verified

2026-08-24 — every claim verified against the sources in §19 on this date. No step was executed;
see §18.
