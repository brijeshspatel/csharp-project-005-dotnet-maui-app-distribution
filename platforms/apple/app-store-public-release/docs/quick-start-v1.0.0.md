---
doc_id: maui-dist-apple-app-store-quick-start
title: Apple App Store — Quick Start
type: guide
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Initial quick-start card. Written using ASD-STE100 principles.
---

# Apple App Store — Quick Start

First-ever Apple App Store release, shortest safe path. This card simplifies navigation; it does
not replace the [full guide](../README.md), which it links back to at every step.

1. Enrol in the Apple Developer Program. See the full guide's [§4 Eligibility](../README.md#4-eligibility).
2. Create a distribution certificate, App ID and provisioning profile. See [§10 Sign](../README.md#10-sign).
3. Build and package: `dotnet publish -f net10.0-ios -c Release`, verified working on Windows
   without a Mac (ad hoc signing only — see [§9 Build](../README.md#9-build)).
4. Re-run with `-p:CodesignKey`/`-p:CodesignProvision` for a real, App-Store-ready signature. See
   [§10 Sign](../README.md#10-sign).
5. Create an app record in App Store Connect. See [§12 Configure Distribution Platform](../README.md#12-configure-distribution-platform).
6. Upload and submit for review. See [§13 Deploy](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: confirm your build tooling targets the iOS 26 SDK (required for
submissions from 2026-04-28) before step 3. See the [Requirements & Freshness Register](../../../../docs/reference/requirements-freshness-register-v1.0.0.md).
