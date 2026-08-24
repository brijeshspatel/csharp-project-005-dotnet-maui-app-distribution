---
doc_id: maui-dist-channel-google-play-internal-testing
title: Google Play Internal Testing
type: guide
version: 1.0.0
status: active
created: 2026-08-24
updated: 2026-08-24
owner: Brijesh Patel
change_summary: Initial channel guide, fourth run under ADR 0012. Written using ASD-STE100 principles.
---

# 🤖 Google Play Internal Testing

Written using ASD-STE100 principles.

## 1. What This Channel Is

Internal testing is the fastest of Google Play's three testing tracks. It distributes an App Bundle
to a small, named list of testers through Google Play itself, **within minutes** of upload.

It is the track closest to the developer, and the one with the fewest gates.

## 2. When to Use It

Use internal testing for initial quality checks on a build — smoke testing a release candidate,
confirming a fix on a real device, or checking that an upload is well-formed — with a small group
you control.

**You can start an internal test before app setup is complete.** That makes it the only track
usable very early in a project's life.

## 3. When Not to Use It

**Do not use it to satisfy the production-access testing requirement.** That requirement names
**closed** testing specifically, which is a separate channel in the
[channel catalogue](../../../docs/maui-distribution-channel-catalogue-v1.0.0.md).

**Do not use it for more than 100 testers.** Use closed or open testing.

⚠️ **Do not enrol a person in internal testing if they also need open or closed testing.** A user
opted into internal testing is **not eligible** for the open and closed tracks, even when their
address appears on those tracks' lists. This trap is described in §17.

**Do not treat it as a policy check.** Internal test releases might not go through standard Play
policy or security review, so passing here proves nothing about what production review will say.

## 4. Eligibility

A Google Play Console developer account, as described in the
[Google Play public release guide's §4](../google-play-public-release/README.md#4-eligibility).
No additional enrolment.

**Tester limit: up to 100 testers per app.**

## 5. Prerequisites

| Prerequisite | Notes |
|---|---|
| A Play Console account | Same account as public release |
| An app record in Play Console | Required, but app setup need not be complete |
| A signed App Bundle (`.aab`) | Built as in the public release guide's §9-§10 |
| An email list of testers | Google Account addresses. Maximum 100 |

App signing, target API level and the App Bundle format requirements are identical to public
release. See that guide's [§5](../google-play-public-release/README.md#5-prerequisites).

## 6. How to Obtain the Prerequisites

Follow the [public release guide's §6](../google-play-public-release/README.md#6-how-to-obtain-the-prerequisites)
for the account and signing key. The one item specific to this channel is the tester list: collect
the Google Account email address of every tester. In Play Console you create the list by entering
addresses separated by commas, or by uploading a CSV file.

## 7. 🔐 Security Model

Identical to [public release §7](../google-play-public-release/README.md#7-security-model). The
same upload key and the same Play App Signing arrangement apply — an internal test build is a real,
signed release artefact, not a debug build.

**What differs is who can obtain it.** Access is controlled by the email list, and by each tester
opting in through the link. A person not on the list cannot install the app.

⚠️ **A debug-signed bundle is not acceptable here.** As with public release, Play rejects it. See
that guide's [§10](../google-play-public-release/README.md#10-sign).

## 8. Application Preparation

Identical to [public release §8](../google-play-public-release/README.md#8-application-preparation),
with one relaxation: the store listing does not need to be complete, because the app is not
publicly visible.

Increment the version code for every upload, exactly as for production.

## 9. Build

Identical to the [public release guide's §9](../google-play-public-release/README.md#9-build),
which is execution-verified from a clean tree. Use the same command:

```
dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
```

⚠️ **The `-p:AndroidEnableMarshalMethods=false` property is not optional on the verified
toolchain.** Without it the build fails with `XAGNM7009`. The full evidence, including the produced
artefacts and their sizes confirmed on disk, is in that guide's §9. This guide does not re-run the
command.

## 10. 🔐 Sign

Identical to [public release §10](../google-play-public-release/README.md#10-sign). Use your real
upload keystore; the debug-signed output is for local testing only.

## 11. 📦 Package

The `.aab` is the upload artefact, as for production. **Confirm it exists by listing
`bin/Release/net10.0-android/publish/`** — see the public release guide's §9 for why the build log
is not sufficient evidence.

## 12. Configure Distribution Platform

In Play Console, open **Testing > Internal testing**:

1. On the **Testers** tab, create or select an email list, and add tester addresses. Enter them
   comma-separated, or upload a CSV.
2. Save the list, and select it for this track.
3. Copy the **opt-in link**. Each tester must open it and opt in themselves; being on the list is
   not by itself enough.

## 13. 🚀 Deploy

Create a release on the internal testing track and upload the `.aab`, then roll it out.

**A new App Bundle published to the internal test track becomes available to testers within
minutes.** This is the defining property of the track, and the reason to use it.

Send the opt-in link to your testers. Each opens it, reads the tester responsibilities, and opts
in. They then install the app from Google Play as normal.

## 14. ✅ Validate

1. Confirm the release shows as available on the internal testing track in Play Console.
2. Confirm at least one tester has opted in through the link.
3. Confirm the app installs from Google Play on that tester's device, and launches.

A tester who reports that Google Play cannot find the app has usually not opted in, or is signed
in with a different Google Account than the one on the list. See §17.

## 15. 🔄 Update

Increment the version code, rebuild, and upload a new release to the same track. Testers receive
the update through Google Play. Availability is again within minutes.

## 16. Revoke / Withdraw / Retire

Remove a tester's address from the email list to end their access, or remove the list from the
track to end everyone's. You can also halt the release in Play Console.

Removal stops future distribution and updates. **An already-installed build stays on the device**
until the tester removes it.

## 17. ⚠️ Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| Tester cannot find the app on Google Play | They have not opted in through the link | Ask whether they opened the opt-in link and accepted | Send the link again; opting in is a separate step from being listed |
| Tester opted in but still cannot install | They are signed in to Google Play with a different Google Account | Compare the account on the device against the listed address | Add the correct address, or have them switch account |
| A tester is excluded from a closed or open test | They are opted into **internal** testing, which makes them ineligible for the other tracks | Check whether the address is on the internal testing list | Have them opt out of internal testing first |
| Upload rejected: version code already used | The version code was not incremented | Compare the bundle's version code against the last upload | Increment and rebuild |
| Upload rejected: signed with the wrong key | The bundle was debug-signed, or signed with a key Play does not expect | Check which key the bundle carries | Sign with the correct upload key, per §10 |
| Build fails with `XAGNM7009` | Marshal methods, enabled by default in .NET 10 | Re-run from a clean tree; it reproduces | Add `-p:AndroidEnableMarshalMethods=false`, per §9 |

## 18. Limitations

**No step in this guide was executed against a real Play Console account.** No Play Console
account, tester list or upload was available in this run. The build step is execution-verified in
the [public release guide](../google-play-public-release/README.md#9-build) and is deliberately not
duplicated here; **everything from §12 onward rests on the sources in §19.**

**Internal test releases might not be subject to standard Play policy or security review.** Passing
an internal test therefore says nothing about whether the app will pass production review. Do not
read it as pre-approval.

**The 100-tester limit is a hard ceiling on this track.** It cannot be raised.

## 19. 📚 Official Sources

- [Set up an open, closed, or internal test — Play Console Help](https://support.google.com/googleplay/android-developer/answer/9845334?hl=en)
- [Prepare and roll out a release — Play Console Help](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en)
- [Publish a .NET MAUI Android app for Google Play distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-google-play?view=net-maui-10.0)

## 20. ✅ Last Verified

2026-08-24 — every claim verified against the sources in §19 on this date. The build step it relies
on was verified by execution in the public release guide and is not re-executed here. Nothing in
§12-§16 is execution-verified; see §18.
