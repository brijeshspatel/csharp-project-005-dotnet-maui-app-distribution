# Direct APK Distribution — Quick Start

Host a signed APK yourself, shortest safe path. Links back to the [full guide](../README.md) at
every step.

**Decide before you start.** This channel has no review, no automatic updates and **no way to
recall a build**. If any of those matter, choose another channel. See
[§3](../README.md#3-when-not-to-use-it) and [§16](../README.md#16-revoke--withdraw--retire).

1. Create your keystore **once**:
   `keytool -genkeypair -v -keystore myapp.keystore -alias myapp -keyalg RSA -keysize 2048 -validity 10000`.
   See [§6](../README.md#6-how-to-obtain-the-prerequisites).
2. Back up the keystore **and** its password, separately. See
   [§6](../README.md#6-how-to-obtain-the-prerequisites).
3. Build and sign, asking for the APK format explicitly and keeping the password out of the log:
   `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false -p:AndroidPackageFormats=apk -p:AndroidKeyStore=true -p:AndroidSigningKeyStore=myapp.keystore -p:AndroidSigningKeyAlias=myapp -p:AndroidSigningKeyPass=env:AndroidSigningPassword -p:AndroidSigningStorePass=env:AndroidSigningPassword`.
   See [§9](../README.md#9-build).
4. Confirm the **signed** `.apk` exists by **listing** `bin/Release/net10.0-android/publish/`. The
   signed file has `-Signed` in its name. See [§11](../README.md#11-package).
5. Host it over HTTPS, and publish the version and certificate fingerprint beside it. See
   [§12](../README.md#12-configure-distribution-platform).
6. Tell users how to permit installation from your source. See [§13](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: lose the keystore or its password and you can never ship an update
that existing installations will accept. There is no reset. Do step 2 before step 3.

STOP — VERIFY BEFORE CONTINUING: `AndroidPackageFormats` is **plural**, and `AndroidKeyStore`
defaults to **false**. Get either wrong and you ship a debug-signed package, or no `.apk` at all.
See [§17](../README.md#17-troubleshooting).

 On Android 8.0 and higher, permitting installation is **per source** — permitting the browser
does not permit a file manager. See [§13](../README.md#13-deploy).

 Never tell users to disable Google Play Protect. If it blocks your app, reduce the permissions
or appeal. See [§7](../README.md#7-security-model).
