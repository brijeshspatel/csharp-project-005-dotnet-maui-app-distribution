---
doc_id: maui-dist-google-play-quick-start
title: Google Play — Quick Start
type: guide
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial quick-start card. Written using ASD-STE100 principles.
---

# Google Play — Quick Start

First-ever Google Play release, shortest safe path. This card simplifies navigation; it does not
replace the [full guide](../README.md), which it links back to at every step.

1. Register a Google Play Console developer account (one-time US $25 fee). See
   [§4 Eligibility](../README.md#4-eligibility) — check whether the 14-day closed-test
   requirement applies to your account first.
2. Set your package name and versioning. See [§8 Application Preparation](../README.md#8-application-preparation).
3. Build: `dotnet publish -f net10.0-android -c Release`, verified working at this repository's
   own real path (see [§9 Build](../README.md#9-build)).
4. Configure real release signing with your own upload keystore. See [§10 Sign](../README.md#10-sign).
5. Create the app listing, store listing, content rating and Data safety declaration. See
   [§12 Configure Distribution Platform](../README.md#12-configure-distribution-platform).
6. Upload the `.aab` manually for your first release. See [§13 Deploy](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: confirm your build targets the current required API level
before step 3 — this floor changes on a published schedule. See the
[Requirements & Freshness Register](../../../../docs/reference/requirements-freshness-register-v1.0.0.md).
