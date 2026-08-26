# Google Play — Quick Start

First-ever Google Play release, shortest safe path. This card simplifies navigation; it does not
replace the [full guide](../README.md), which it links back to at every step.

1. Register a Google Play Console developer account (one-time US $25 fee). See
   [§4 Eligibility](../README.md#4-eligibility) — check whether the 14-day closed-test
   requirement applies to your account first.
2. Set your package name and versioning. See [§8 Application Preparation](../README.md#8-application-preparation).
3. Build: `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false`,
   run at the project's **real path**. Without that property the build fails from a clean tree
   with `XAGNM7009`; treat it as a mitigation, not a default. See
   [§9 Build](../README.md#9-build), then **list** the publish folder to confirm the `.aab`.
4. Configure real release signing with your own upload keystore. **`-p:AndroidKeyStore=true` is
   what switches signing on** — it defaults to `false`, and without it the signing properties are
   silently ignored and you ship a debug-signed bundle Google Play will reject:
   `dotnet publish -f net10.0-android -c Release -p:AndroidEnableMarshalMethods=false
   -p:AndroidKeyStore=true -p:AndroidSigningKeyStore=<keystore> -p:AndroidSigningKeyAlias=<alias>
   -p:AndroidSigningKeyPass=file:<file> -p:AndroidSigningStorePass=file:<file>`. See
   [§10 Sign](../README.md#10-sign).
5. Create the app listing, store listing, content rating and Data safety declaration. See
   [§12 Configure Distribution Platform](../README.md#12-configure-distribution-platform).
6. Upload the `.aab` for your first release. Doing it by hand in Play Console is the cautious
   choice — this release configures Play App Signing and fixes your upload key — but Google
   documents no rule against using the Play Developer API. See [§13 Deploy](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: confirm your build targets the current required API level
before step 3 — this floor changes on a published schedule. See the
[Requirements & Freshness Register](../../../../docs/reference/requirements-freshness-register.md).
