---
doc_id: maui-dist-channel-google-play-closed-testing
title: Google Play Closed Testing
type: guide
version: 1.0.1
status: active
created: 2026-08-24
updated: 2026-08-25
owner: Brijesh Patel
change_summary: Removes emoji from the section headings so every internal anchor resolves. An emoji in a heading is dropped by the anchor rule and leaves the space beside it, which turned every #7-security-model style link into a broken one. No procedural content, section name or ordering changed.
---

# Google Play Closed Testing

Written using ASD-STE100 principles.

## 1. What This Channel Is

Closed testing distributes an App Bundle through Google Play to a controlled group of testers that
you choose, at a scale internal testing cannot reach. Unlike internal testing, closed test releases
**are** subject to standard Play policy review.

**For many developer accounts it is also a gate, not a choice.** See §4.

## 2. When to Use It

Use closed testing when you need a real testing population — larger than 100 people, or organised
into groups you can target separately — and you want the build to have passed policy review before
testers see it.

**Use it when you must reach production at all**, if your account falls under the testing
requirement in §4.

## 3. When Not to Use It

**Do not use it for a very small, very fast check.** Internal testing reaches testers in minutes;
closed testing takes several hours. See
[Google Play internal testing](../google-play-internal-testing/README.md).

**Do not use it to reach the general public.** Open testing lists the app on Google Play for anyone
to join.

## 4. Eligibility

A Google Play Console developer account, as described in the
[Google Play public release guide's §4](../google-play-public-release/README.md#4-eligibility).

⚠️ **WARNING — for many accounts, closed testing is mandatory before production access.**

**Personal Play Console accounts created after 13 November 2023** must run a closed test before
they can apply for production access:

| Requirement | Value |
|---|---|
| Track | **Closed** testing specifically. Internal and open testing do not satisfy it |
| Minimum testers | **12** |
| Continuous duration | **14 days**, opted in continuously |
| Then | Apply for production access through the Play Console dashboard |
| Google's response time | Seven days or less |

**A tester who opts in, tests for fewer than 14 days, and then opts out does not count.** The
14-day clock is per tester and continuous, not a calendar window during which 12 people passed
through. This is the single most misread requirement on this channel.

The application asks about the closed test, the app's design, and production readiness.

## 5. Prerequisites

| Prerequisite | Notes |
|---|---|
| A Play Console account | Same account as public release |
| A complete app record | More complete than internal testing requires, because policy review applies |
| A signed App Bundle (`.aab`) | Built as in the public release guide's §9-§10 |
| A tester group | Email lists, or a Google Group |

**Tester capacity:**

| Limit | Value |
|---|---|
| Email lists | Up to 200 in total |
| Users per list | Up to 2,000 |
| Lists per track | Up to 50 |

## 6. How to Obtain the Prerequisites

Follow the [public release guide's §6](../google-play-public-release/README.md#6-how-to-obtain-the-prerequisites)
for the account and signing key.

**Choose how you will manage testers**, because the two routes behave differently:

- **Email lists.** Enter addresses comma-separated, or upload a CSV.
- **A Google Group**, given as `yourgroupname@googlegroups.com`. ⚠️ **A user must join the group
  _before_ opting into the test.** Joining afterwards does not grant access retrospectively, and
  this is a common cause of a tester who "cannot see the app".

## 7. Security Model

Identical to [public release §7](../google-play-public-release/README.md#7-security-model) — the
same upload key and Play App Signing arrangement, and a real signed release artefact.

Access is controlled by list or group membership plus each tester's own opt-in. Both are required.

## 8. Application Preparation

Identical to [public release §8](../google-play-public-release/README.md#8-application-preparation).

**Prepare the app as if for production.** Closed test releases go through standard Play policy
review, so a listing or policy problem surfaces here rather than being deferred.

## 9. Build

Identical to the [public release guide's §9](../google-play-public-release/README.md#9-build),
which is execution-verified from a clean tree:

```
dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
```

⚠️ **`-p:AndroidEnableMarshalMethods=false` is not optional on the verified toolchain.** Without it
the build fails with `XAGNM7009`. This guide does not re-run the command; the evidence, including
artefact sizes confirmed on disk, is in that guide's §9.

## 10. Sign

Identical to [public release §10](../google-play-public-release/README.md#10-sign).

## 11. Package

The `.aab` is the upload artefact. **Confirm it exists by listing
`bin/Release/net10.0-android/publish/`.**

## 12. Configure Distribution Platform

In Play Console, open **Testing > Closed testing**:

1. Select the track, or create an additional closed track.
2. On the **Testers** tab, add an email list or a Google Group.
3. Save, and copy the **opt-in link**.

⚠️ **Additional closed tracks are less capable than the default one.** They do **not** support
enterprise targeting, device compatibility filtering, or country targeting. If you need any of
those, use the default closed track.

## 13. Deploy

Create a release on the closed track, upload the `.aab`, and roll it out.

**Availability takes several hours after first publication**, and updates take a similar delay.
This is the practical difference from internal testing, and it is the reason not to use this track
for a quick check.

Send the opt-in link. Each tester opens it, reads the tester responsibilities, and opts in. If you
used a Google Group, they must already be a member.

## 14. Validate

1. Confirm the release reaches an available state on the closed track — allow several hours.
2. Confirm testers have opted in.
3. Confirm the app installs from Google Play and launches.

**If you are working towards production access, track the 14-day clock per tester**, and confirm at
least 12 testers stay opted in continuously. Play Console shows the opted-in count; a count that
dips and recovers does not restart at zero for testers who never left, but it does for anyone who
opted out.

## 15. Update

Increment the version code, rebuild, and upload a new release to the track. Expect the same
several-hour delay. Policy review applies to updates as well.

## 16. Revoke / Withdraw / Retire

Remove an email list or Google Group from the track, or remove individual addresses, to end
access. Halting the release stops distribution.

Removal stops future distribution and updates. **An already-installed build stays on the device.**

⚠️ **Removing testers while working towards production access resets nothing in your favour.**
Anyone removed stops counting towards the 12-tester, 14-day requirement.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| Tester cannot see the app, and you used a Google Group | They opted in before joining the group | Check their group membership date against their opt-in | Have them join the group, then opt in again |
| Tester cannot see the app, and you used an email list | They have not opted in, or use a different Google Account | Compare the device's account against the listed address | Send the opt-in link again, or correct the address |
| Tester is excluded despite being listed | They are opted into **internal** testing, which makes them ineligible for closed testing | Check the internal testing list for their address | Have them opt out of internal testing |
| Release not visible after upload | Normal. Closed testing takes several hours, unlike internal testing | Check the release state in Play Console | Wait. Do not re-upload |
| Production access refused | The 12-tester, 14-day continuous requirement is unmet | Check each tester's continuous opted-in duration | Testers who opted out mid-way do not count; run the test again with a stable group |
| Additional closed track will not target a country or device | Additional closed tracks do not support those filters | Check which track you are using | Use the default closed track |
| Build fails with `XAGNM7009` | Marshal methods, enabled by default in .NET 10 | Re-run from a clean tree; it reproduces | Add `-p:AndroidEnableMarshalMethods=false`, per §9 |

## 18. Limitations

**No step in this guide was executed against a real Play Console account.** The build step is
execution-verified in the [public release guide](../google-play-public-release/README.md#9-build)
and is not duplicated here; **everything from §12 onward rests on the sources in §19.**

**The production-access requirement in §4 applies to personal accounts created after 13 November
2023.** Organisation accounts have been subject to differing requirements over time. Check the
current rule for your own account type against the source in §19 rather than assuming this
guide's figure applies to you — Google has revised this requirement before, including reducing the
tester minimum from 20 to 12 in December 2024.

**"Several hours" is Google's own wording**, not a measured figure, and it is not a commitment.

## 19. Official Sources

- [Set up an open, closed, or internal test — Play Console Help](https://support.google.com/googleplay/android-developer/answer/9845334?hl=en)
- [App testing requirements for new personal developer accounts — Play Console Help](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en)
- [Prepare and roll out a release — Play Console Help](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en)
- [Publish a .NET MAUI Android app for Google Play distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-google-play?view=net-maui-10.0)

## 20. Last Verified

2026-08-24 — every claim verified against the sources in §19 on this date. The build step it relies
on was verified by execution in the public release guide and is not re-executed here. Nothing in
§12-§16 is execution-verified; see §18.
