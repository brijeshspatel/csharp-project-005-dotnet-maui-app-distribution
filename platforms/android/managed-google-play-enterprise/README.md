# Managed Google Play and Android Enterprise Distribution

## 1. What This Channel Is

Managed Google Play distributes an app **privately to named organisations**. The app is published
through Google Play, so Play handles hosting, delivery and updates, but it never appears in the
public store. Each recipient organisation's IT team then installs or lists it through their own
EMM — Enterprise Mobility Management, also called MDM.

This is the Android counterpart of Apple's
[Custom Apps route](../../apple/business-manager-and-enterprise/README.md).

## 2. When to Use It

Use it to deliver an app to one or more specific businesses — your employer, a client, a partner —
where the recipients manage their devices with an EMM and you want Play to handle distribution.

Use it when you want private delivery **without** losing Play's update mechanism, which direct APK
distribution gives up.

## 3. When Not to Use It

**Do not use it for the general public.** Use
[Google Play public release](../google-play-public-release/README.md).

**Do not use it where the recipients have no EMM.** Distribution runs through the recipient's EMM
console. Without one, there is nothing on their side to distribute the app.

**Do not use it for testing.** Use the
[internal](../google-play-internal-testing/README.md),
[closed](../google-play-closed-testing/README.md) or
[open](../google-play-open-testing/README.md) testing tracks.

**Do not use it for an app you may later want to publish publicly.** See the warning in §12 —
that decision is effectively permanent for a given package name.

## 4. Eligibility

A Google Play Console developer account, as described in the
[public release guide's §4](../google-play-public-release/README.md#4-eligibility). No separate
programme and no separate fee — this is a setting on an ordinary Play Console app, not a different
membership.

Each **recipient** organisation needs managed Google Play, through Android Enterprise, with an EMM.

**Up to 1,000 organisations per app.**

## 5. Prerequisites

| Prerequisite | Notes |
|---|---|
| A Play Console account | The ordinary developer account |
| An app record in Play Console | Standard |
| A signed App Bundle (`.aab`) | Built as in the public release guide's §9-§10 |
| Each recipient's **Organization ID** | Supplied by that organisation's admin. You cannot look it up |
| An EMM on the recipient's side | Theirs to operate, not yours |

## 6. How to Obtain the Prerequisites

Follow the [public release guide's §6](../google-play-public-release/README.md#6-how-to-obtain-the-prerequisites)
for the account and signing key.

**Obtain each Organization ID from the recipient.** Their admin opens the managed Google Play EMM
iframe, selects the organisation icon, and copies the Organization ID string. They send it to you.
There is no way for you to discover it independently, so this step is a dependency on another
organisation's schedule — start it early.

## 7. Security Model

Signing is identical to [public release §7](../google-play-public-release/README.md#7-security-model):
the same upload key, the same Play App Signing arrangement.

**Google Play enforces the distribution boundary**, in the same way Apple does for Custom Apps. The
app is visible only to the organisations you listed. A person outside them cannot find or install
it, and a recipient cannot pass it on.

**Private apps are automatically approved for distribution across every EMM binding associated with
the same Google Workspace or Cloud Identity account** when they are published. Treat "the
organisation" as the unit of access, not "a device" or "a user" — if an organisation has several
EMM bindings under one identity account, the app reaches all of them.

## 8. Application Preparation

Identical to [public release §8](../google-play-public-release/README.md#8-application-preparation).

Choose the package name deliberately. It is the identity that carries the private-or-public
decision described in §12.

## 9. Build

Identical to the [public release guide's §9](../google-play-public-release/README.md#9-build),
which is execution-verified from a clean tree:

```
dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
```

**`-p:AndroidEnableMarshalMethods=false` is not optional on the verified toolchain.** Without it
the build fails with `XAGNM7009`. This guide does not re-run the command.

## 10. Sign

Identical to [public release §10](../google-play-public-release/README.md#10-sign).

## 11. Package

The `.aab` is the upload artefact. **Confirm it exists by listing
`bin/Release/net10.0-android/publish/`.**

## 12. Configure Distribution Platform

In Play Console:

1. Go to **Release > Setup > Advanced settings**, and select the **Managed Google Play** tab.
2. Select **Add organization**.
3. For each recipient, enter the **Organization ID** and a description. Up to 1,000 organisations
   per app.
4. Upload the App Bundle and publish to production.

**WARNING — restricting an app to organisations is not reversible for that package name.** Once
restricted, the app is private and available to those organisations only. **To make it publicly
available you must publish a new app with a different package name** — which means a new listing,
a new identity, and no continuity for anyone who already installed the private one. Decide before
you restrict, not afterwards.

**An alternative route exists.** With a third-party EMM you may be able to publish private apps
from the EMM console rather than from Play Console. This guide documents the Play Console route
because it is the one that does not depend on which EMM the recipient runs.

## 13. Deploy

Publishing is the whole of your side. **After publication the app is searchable and distributable
through the recipients' EMM consoles within a few minutes.**

The recipient's IT team then chooses how their users get it:

- Install it remotely onto managed devices, or
- List it in their users' Managed Play store for self-service installation.

Private apps are distributed exactly like public apps from the EMM's point of view.

## 14. Validate

1. Confirm the `.aab` exists on disk (§11) and the release is published in Play Console.
2. Confirm the app is restricted to the intended Organization IDs, and to no others. **Check the
   list rather than assuming**, because an incorrect ID fails silently — the app simply does not
   appear for the intended recipient.
3. Ask one recipient admin to confirm the app appears in their EMM console.
4. Confirm installation and launch on a managed device.

## 15. Update

Increment the version code, rebuild, and publish a new release. Play delivers updates through the
recipients' EMM exactly as for a public app. **Keeping Play's update path is the main advantage of
this channel over direct APK distribution.**

To add a recipient later, add their Organization ID in the same Managed Google Play tab. Adding an
organisation does not require republishing the binary.

## 16. Revoke / Withdraw / Retire

Remove an organisation's ID to end its access, or unpublish the app to end all distribution.

Removal stops future distribution and updates. An already-installed build stays on the device
unless the recipient's EMM removes it.

**The recipient's EMM is the only reliable removal tool**, and it is theirs, not yours. If removal
from devices matters to you, agree it with the recipient before distributing.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| Recipient cannot find the app in their EMM console | Wrong Organization ID, or the app is not yet published | Compare the stored ID against the one the admin supplied, character for character | Correct the ID. An incorrect ID fails silently |
| App still missing a few minutes after publishing | Propagation, or the release is not actually live | Check the release state in Play Console | Confirm the release is published to production, then wait a few minutes |
| Need to make the app public | The private restriction is fixed for this package name | Check the Managed Google Play tab | Publish a new app with a different package name. The existing one cannot be converted |
| App reaches more of the organisation than expected | Private apps are approved across every EMM binding under the same Workspace or Cloud Identity account | Ask the admin how many bindings that account has | Expected behaviour. Scope by organisation, not by binding |
| Recipient has no EMM | This channel requires one | Confirm with the recipient | Use another channel; without an EMM there is no distribution path here |
| Build fails with `XAGNM7009` | Marshal methods, enabled by default in .NET 10 | Re-run from a clean tree; it reproduces | Add `-p:AndroidEnableMarshalMethods=false`, per §9 |

## 18. Limitations

**No step in this guide was executed.** No Play Console account, no Organization ID and no EMM were
available in this run. The build step is execution-verified in the
[public release guide](../google-play-public-release/README.md#9-build) and is not duplicated here;
**everything from §12 onward rests on the sources in §19.**

**The EMM side is out of this guide's scope.** How a recipient assigns, installs or removes the app
is governed by their EMM's own documentation, not by Play Console, and it varies by vendor. This
guide stops at the boundary where your control ends.

**"Within a few minutes" is Google's own wording**, not a measured figure, and not a commitment.

## 19. Official Sources

- [Publish private apps from the Play Console — Managed Google Play Help](https://support.google.com/googleplay/work/answer/6145139?hl=en)
- [Distribute private apps — Managed Google Play Help](https://support.google.com/googleplay/work/answer/9495634?hl=en)
- [Publish private apps from managed Play in your EMM console — Android Enterprise Help](https://support.google.com/work/android/answer/9146439?hl=en)
- [Publish a .NET MAUI Android app for Google Play distribution — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-google-play?view=net-maui-10.0)

## 20. Last Verified

2026-08-24 — every claim verified against the sources in §19 on this date. The build step it relies
on was verified by execution in the public release guide and is not re-executed here. Nothing in
§12-§16 is execution-verified; see §18.
