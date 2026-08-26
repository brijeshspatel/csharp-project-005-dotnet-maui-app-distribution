# Google Play Closed Testing — Quick Start

Test with a controlled group at scale, shortest safe path. Links back to the
[full guide](../README.md) at every step.

**Read this first if your Play Console account is personal and was created after 13 November
2023:** you must run a closed test with **12 testers opted in continuously for 14 days** before you
can apply for production access. Internal and open testing do not satisfy it. See
[§4](../README.md#4-eligibility).

1. Build and sign the `.aab`. **`-p:AndroidKeyStore=true` is what switches signing on** — it
   defaults to `false`, and without it the signing properties are ignored and you get a
   debug-signed bundle Google Play will reject:
   `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
   -p:AndroidKeyStore=true -p:AndroidSigningKeyStore=<keystore> -p:AndroidSigningKeyAlias=<alias>
   -p:AndroidSigningKeyPass=file:<file> -p:AndroidSigningStorePass=file:<file>`. See
   [§9 Build](../README.md#9-build) and [§10 Sign](../README.md#10-sign).
2. Confirm the `.aab` exists by **listing** `bin/Release/net10.0-android/publish/`. See
   [§11](../README.md#11-package).
3. In Play Console, open **Test and release > Testing > Closed testing**, and add an email list or a Google Group.
   See [§12](../README.md#12-configure-distribution-platform).
4. Create a release, upload the `.aab`, and roll it out. **Allow several hours** — this track is
   not instant. See [§13](../README.md#13-deploy).
5. Send the opt-in link. Each tester must opt in. See [§13](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: if you used a Google Group, each tester must **join the group
before** opting in. Joining afterwards does not grant access.

STOP — VERIFY BEFORE CONTINUING: a tester who opts out before 14 days have passed does **not**
count towards the production-access requirement, even if they rejoin later. Track the clock per
tester. See [§14](../README.md#14-validate).

Additional closed tracks do not support enterprise targeting, device compatibility filtering or
country targeting. Use the default closed track if you need any of them. See
[§12](../README.md#12-configure-distribution-platform).
