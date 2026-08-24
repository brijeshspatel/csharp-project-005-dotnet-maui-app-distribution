---
doc_id: maui-dist-channel-google-play-open-testing
title: Google Play Open Testing
type: guide
version: 1.0.0
status: active
created: 2026-08-24
updated: 2026-08-24
owner: Brijesh Patel
change_summary: Initial channel guide, sixth run under ADR 0012. Written using ASD-STE100 principles.
---

# 🤖 Google Play Open Testing

Written using ASD-STE100 principles.

## 1. What This Channel Is

Open testing publishes a test version of the app **on Google Play, where anyone can find it and
join**. Users discover it through Play search, from the app's production listing page, or through
a shareable opt-in link. Testers can submit private feedback that is not shown as a public review.

It is the most public of the three testing tracks, and the only one where you do not choose the
testers.

## 2. When to Use It

Use open testing when you want scale and real-world diversity — many devices, many networks, many
locales — and you are willing for the test build to be publicly discoverable.

Use it to gather feedback privately at a point where the app is presentable but not final.

## 3. When Not to Use It

**Do not use it for anything confidential.** The app is listed on Google Play and anyone may
install it. An unreleased feature in an open test is a released feature in practice.

**Do not use it to satisfy the production-access testing requirement.** That requirement names
**closed** testing. See
[Google Play closed testing](../google-play-closed-testing/README.md#4-eligibility).

**Do not use it as your first test.** ⚠️ **Open testing becomes available only after you have
production access**, which for many accounts means completing a closed test first.

**Do not use it for a quick check.** Availability takes several hours, as with closed testing.

## 4. Eligibility

A Google Play Console developer account, as described in the
[Google Play public release guide's §4](../google-play-public-release/README.md#4-eligibility).

⚠️ **Open testing becomes available after you gain production access.** For a personal account
created after 13 November 2023, that means the closed test described in the
[closed testing guide's §4](../google-play-closed-testing/README.md#4-eligibility) must be
completed first. **Open testing is therefore not a starting point**, despite being the most open
track.

**Tester capacity: unlimited by default.** You may instead specify a target with a minimum of
1,000 testers.

## 5. Prerequisites

| Prerequisite | Notes |
|---|---|
| A Play Console account with production access | See the warning in §4 |
| A complete, presentable store listing | The app becomes publicly visible |
| A signed App Bundle (`.aab`) | Built as in the public release guide's §9-§10 |

The app and its listing must be **ready for visibility on Google Play**. Review applies.

## 6. How to Obtain the Prerequisites

Follow the [public release guide's §6](../google-play-public-release/README.md#6-how-to-obtain-the-prerequisites)
for the account and signing key, and complete production access first if you do not have it.

**No tester list is needed.** That is the defining difference from the other two tracks — testers
enrol themselves.

## 7. 🔐 Security Model

Identical to [public release §7](../google-play-public-release/README.md#7-security-model) — the
same upload key and Play App Signing arrangement.

**There is no access control.** Membership is self-service: anyone who finds the listing or the
opt-in link may join. Treat an open test build as published software, and apply the same care to
secrets, endpoints and test data that you would to a production release.

## 8. Application Preparation

Identical to [public release §8](../google-play-public-release/README.md#8-application-preparation),
and to the same standard — the listing is public.

Make it obvious in the listing that this is a test version, and say how to send feedback. Testers
who cannot report a problem privately tend to report it publicly instead.

## 9. Build

Identical to the [public release guide's §9](../google-play-public-release/README.md#9-build),
which is execution-verified from a clean tree:

```
dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
```

⚠️ **`-p:AndroidEnableMarshalMethods=false` is not optional on the verified toolchain.** Without it
the build fails with `XAGNM7009`. This guide does not re-run the command.

## 10. 🔐 Sign

Identical to [public release §10](../google-play-public-release/README.md#10-sign).

## 11. 📦 Package

The `.aab` is the upload artefact. **Confirm it exists by listing
`bin/Release/net10.0-android/publish/`.**

## 12. Configure Distribution Platform

In Play Console, open **Testing > Open testing**:

1. Select the track.
2. Choose the tester capacity: unlimited, or a target with a minimum of 1,000.
3. Save, and copy the **opt-in link** for sharing directly.

No email list and no Google Group are required.

## 13. 🚀 Deploy

Create a release on the open track, upload the `.aab`, and roll it out.

**Availability takes several hours**, for the first publication and for later changes.

Once live, users find the test in two ways: through Google Play itself — search results and the
production listing page — or through the opt-in link you share. Each tester opts in, then installs
from Google Play as normal.

## 14. ✅ Validate

1. Confirm the release reaches an available state on the open track — allow several hours.
2. Confirm the test is discoverable: search Google Play, and check the production listing page.
3. Confirm the app installs and launches from a device that has never been a registered tester.
   That is the case this track exists to cover, and the one an internal or closed test cannot
   prove.
4. Confirm the private feedback path works.

## 15. 🔄 Update

Increment the version code, rebuild, and upload a new release to the track. Expect the same
several-hour delay. Review applies to updates.

## 16. Revoke / Withdraw / Retire

Halt the release, or reduce the track's availability, to stop new testers joining and to stop
distribution.

**An already-installed build stays on the device.** With an unbounded, self-enrolled population you
have no list of who installed it, so plan withdrawal as "stop distributing and ship a replacement",
never as "remove it from testers".

⚠️ **Anything shipped to an open test should be treated as permanently public.** Withdrawal limits
future reach only.

## 17. ⚠️ Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| Open testing track unavailable in Play Console | Production access not yet granted | Check the account's production access state | Complete the closed test and apply for production access first, per §4 |
| Test not discoverable on Google Play | Normal for several hours after publication, or review is incomplete | Check the release state in Play Console | Wait. Do not re-upload |
| A specific person cannot join | They are opted into **internal** testing, which makes them ineligible for open testing | Check the internal testing list for their address | Have them opt out of internal testing |
| Feedback arrives as public reviews | The private feedback path is not obvious in the listing | Read the listing as a new tester would | State the feedback route in the listing, per §8 |
| Release rejected at review | The app or listing is not ready for public visibility | Read the rejection message | Correct the listing or the app; open testing applies the public standard |
| Build fails with `XAGNM7009` | Marshal methods, enabled by default in .NET 10 | Re-run from a clean tree; it reproduces | Add `-p:AndroidEnableMarshalMethods=false`, per §9 |

## 18. Limitations

**No step in this guide was executed against a real Play Console account.** The build step is
execution-verified in the [public release guide](../google-play-public-release/README.md#9-build)
and is not duplicated here; **everything from §12 onward rests on the sources in §19.**

**"Several hours" is Google's own wording**, not a measured figure, and not a commitment.

**The production-access precondition in §4 is derived from Google's statement that open testing
becomes available after production access**, combined with the testing requirement for personal
accounts created after 13 November 2023. Account types and dates change; check the current rule
for your own account rather than assuming this guide's applies.

## 19. 📚 Official Sources

- [Set up an open, closed, or internal test — Play Console Help](https://support.google.com/googleplay/android-developer/answer/9845334?hl=en)
- [App testing requirements for new personal developer accounts — Play Console Help](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en)
- [Prepare and roll out a release — Play Console Help](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en)
- [Publish a .NET MAUI Android app for Google Play distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-google-play?view=net-maui-10.0)

## 20. ✅ Last Verified

2026-08-24 — every claim verified against the sources in §19 on this date. The build step it relies
on was verified by execution in the public release guide and is not re-executed here. Nothing in
§12-§16 is execution-verified; see §18.
