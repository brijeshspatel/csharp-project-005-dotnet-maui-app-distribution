# Managed Google Play — Quick Start

Distribute privately to named organisations, shortest safe path. Links back to the
[full guide](../README.md) at every step.

**Start step 1 early.** It depends on someone in another organisation, not on you.

1. Ask each recipient's admin for their **Organization ID**. They copy it from the managed Google
   Play EMM iframe. You cannot look it up. See
   [§6](../README.md#6-how-to-obtain-the-prerequisites).
2. Build and sign the `.aab` —
   `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false`. See
   [§9](../README.md#9-build).
3. Confirm the `.aab` exists by **listing** `bin/Release/net10.0-android/publish/`. See
   [§11](../README.md#11-package).
4. In Play Console, go to **Release > Setup > Advanced settings > Managed Google Play**, select
   **Add organization**, and enter each Organization ID with a description. Up to 1,000. See
   [§12](../README.md#12-configure-distribution-platform).
5. Upload the App Bundle and publish to production. The app reaches recipients' EMM consoles within
   a few minutes. See [§13](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: restricting an app to organisations is **not reversible for that
package name**. Making it public later means publishing a new app under a different package name,
with no continuity for existing installs. Decide before step 4. See
[§12](../README.md#12-configure-distribution-platform).

STOP — VERIFY BEFORE CONTINUING: check each Organization ID character for character. A wrong ID
fails silently — the app simply never appears for that recipient. See
[§14](../README.md#14-validate).

⚠️ Removal from devices is done by the recipient's EMM, which is theirs and not yours. Agree it
before distributing if it matters. See [§16](../README.md#16-revoke--withdraw--retire).
