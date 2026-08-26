# Google Play Internal Testing — Quick Start

Get a build to up to 100 testers in minutes, shortest safe path. Links back to the
[full guide](../README.md) at every step.

1. Build and sign the `.aab`. **`-p:AndroidKeyStore=true` is what switches signing on** — it
   defaults to `false`, and without it the signing properties are ignored and you get a
   debug-signed bundle Google Play will reject:
   `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
   -p:AndroidKeyStore=true -p:AndroidSigningKeyStore=<keystore> -p:AndroidSigningKeyAlias=<alias>
   -p:AndroidSigningKeyPass=file:<file> -p:AndroidSigningStorePass=file:<file>`. See
   [§9 Build](../README.md#9-build) and [§10 Sign](../README.md#10-sign).
2. Confirm the `.aab` exists by **listing** `bin/Release/net10.0-android/publish/`. See
   [§11](../README.md#11-package).
3. In Play Console, open **Test and release > Testing > Internal testing**, create an email list of up to 100 Google
   Account addresses, and select it for the track. See
   [§12](../README.md#12-configure-distribution-platform).
4. Create a release, upload the `.aab`, and roll it out. It reaches testers within minutes. See
   [§13](../README.md#13-deploy).
5. Send the **opt-in link**. Each tester must open it and opt in. See
   [§13](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: being on the email list is not enough. A tester who has not
opened the opt-in link will not find the app on Google Play.

A user opted into **internal** testing is **not eligible** for open or closed testing, even if
their address is on those lists. If someone must be in a closed or open test, do not add them
here. See [§3](../README.md#3-when-not-to-use-it).

Internal test releases might not go through standard Play policy or security review. Passing
here is not a signal that production review will pass. See [§18](../README.md#18-limitations).
