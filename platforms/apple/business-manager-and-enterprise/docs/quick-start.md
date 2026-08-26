# Apple Business Manager and Enterprise — Quick Start

Distribute privately to an organisation, shortest safe path. Links back to the
[full guide](../README.md) at every step.

**First, choose the route. They are different products.**

| If | Use | Programme |
|---|---|---|
| The recipients are another organisation, or you want Apple to host and deliver | **Custom Apps** | Apple Developer Program (US $99/yr) |
| The recipients are your own employees, and no other route fits | **In-house** | Apple Developer Enterprise Program (US $299/yr, 100+ employees, D-U-N-S, interview) |

STOP — VERIFY BEFORE CONTINUING: Apple does **not** permit the Enterprise Program where App Store,
Custom Apps, ad hoc or TestFlight would serve. Confirm Custom Apps does not fit before applying.
See [§1](../README.md#1-what-this-channel-is).

## Custom Apps

1. Get each recipient's **Organization ID** from their Apple Business Manager. You cannot look it
   up. See [§6](../README.md#6-how-to-obtain-the-prerequisites).
2. Create the app record, then set **App Distribution Methods** to **Private**, Type
   **Organization ID**. See [§12](../README.md#12-configure-distribution-platform).
3. Prepare a demo account and safe sample data — Apple signs in to review it. See
   [§8](../README.md#8-application-preparation).
4. Build, sign with your **App Store** profile **and archive** — `-p:ArchiveOnBuild=true
   -p:RuntimeIdentifier=ios-arm64` alongside `-p:CodesignKey`/`-p:CodesignProvision`, since signing
   alone writes no package — then submit. See [§10](../README.md#10-sign).
5. After approval, the app appears in each named organisation's Apps and Books. See
   [§13](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: confirm the method reads **Private** before you submit. After
approval it **cannot be changed** — switching to public needs a new app record and a new binary.

## In-house

1. Enrol in the Apple Developer Enterprise Program, with a **separate Apple Account**. See
   [§4](../README.md#4-eligibility).
2. Create an **In House** provisioning profile — not App Store, not Ad Hoc. See
   [§6](../README.md#6-how-to-obtain-the-prerequisites).
3. Build, sign with that profile **and archive** — `-p:ArchiveOnBuild=true
   -p:RuntimeIdentifier=ios-arm64` alongside the codesign properties. Signing alone writes no
   package. See [§10](../README.md#10-sign).
4. Confirm the `.ipa` exists by **listing** `bin/Release/net10.0-ios/ios-arm64/publish/`. See
   [§11](../README.md#11-package).
5. Serve it over authenticated HTTPS, or push it through MDM. See
   [§13](../README.md#13-deploy).

 An in-house build has **no device restriction**. Anyone holding the `.ipa` can install it.
Treat it as a credential, and prefer MDM — without MDM you cannot remove it from a device later.
See [§7](../README.md#7-security-model) and [§16](../README.md#16-revoke--withdraw--retire).
