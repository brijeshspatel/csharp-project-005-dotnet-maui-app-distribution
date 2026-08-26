# Google Play Open Testing — Quick Start

Publish a test version anyone can join, shortest safe path. Links back to the
[full guide](../README.md) at every step.

**Check this before anything else:** open testing becomes available **after** you have production
access. For a personal account created after 13 November 2023 that means completing a closed test
first. See [§4](../README.md#4-eligibility).

1. Build and sign the `.aab`. **`-p:AndroidKeyStore=true` is what switches signing on** — it
   defaults to `false`, and without it the signing properties are ignored and you get a
   debug-signed bundle Google Play will reject:
   `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
   -p:AndroidKeyStore=true -p:AndroidSigningKeyStore=<keystore> -p:AndroidSigningKeyAlias=<alias>
   -p:AndroidSigningKeyPass=file:<file> -p:AndroidSigningStorePass=file:<file>`. See
   [§9 Build](../README.md#9-build) and [§10 Sign](../README.md#10-sign).
2. Confirm the `.aab` exists by **listing** `bin/Release/net10.0-android/publish/`. See
   [§11](../README.md#11-package).
3. Finish the store listing to a public standard — the app becomes publicly visible, and review
   applies. See [§8](../README.md#8-application-preparation).
4. In Play Console, open **Test and release > Testing > Open testing**, and set capacity: unlimited, or a limited
   number set to at least 1,000 — that is the **smallest cap you may set**, not a number of testers
   you must find. No tester list is needed. See
   [§12](../README.md#12-configure-distribution-platform).
5. Create a release, upload the `.aab`, and roll it out. **Allow several hours.** See
   [§13](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: this build will be publicly installable. Confirm it contains
nothing confidential — no unreleased feature you need kept quiet, no test endpoint, no sample
credential. See [§7](../README.md#7-security-model).

STOP — VERIFY BEFORE CONTINUING: state the private feedback route in the listing before you roll
out. Testers who cannot report a problem privately report it publicly instead. See
[§8](../README.md#8-application-preparation).

You have no list of who installed an open test build, so you cannot withdraw it from testers.
Withdrawal limits future reach only. See [§16](../README.md#16-revoke--withdraw--retire).
