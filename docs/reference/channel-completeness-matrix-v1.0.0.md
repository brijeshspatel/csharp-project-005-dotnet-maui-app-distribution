---
doc_id: maui-dist-channel-completeness-matrix
title: Channel Completeness Matrix
type: reference
version: 1.0.0
status: active
created: 2026-08-23
updated: 2026-08-23
owner: Brijesh Patel
change_summary: Corrects the Build column after clean-tree re-verification, adds the ad hoc distribution channel, and rewrites every row as a single line so none is silently skipped.
---

# Channel Completeness Matrix

One row per distribution channel this repository documents. Every column is filled or marked
`N/A — <reason>`; a blank cell is a defect, not an omission.

| Channel | Selection Guidance | Prerequisites | Setup | 🔐 Signing | Build | 🧪 Test | 🚀 Deploy | Update | Revoke | Troubleshoot | Official Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Apple App Store | Yes | Yes | Yes | Yes | Partial (executed) — compiles on Windows; produces no `.ipa` without signing, see its §9 | N/A — store-side testing tracks are separate channels; TestFlight is documented, the Google Play tracks are not yet | Yes | Yes | Yes | Yes | Yes |
| Google Play | Yes | Yes | Yes | Yes | Yes (executed, clean tree, artefacts confirmed on disk; needs `AndroidEnableMarshalMethods=false`, see its §9) | N/A — store-side testing tracks are separate channels, not yet documented | Yes | Yes | Yes | Yes | Yes |
| TestFlight | Yes | Yes | Yes | Yes | N/A — identical to Apple App Store's build, not re-executed; that build produces no `.ipa` without signing, see its §9 | Yes — this channel is itself Apple's own testing mechanism | Yes | Yes | Yes | Yes | Yes |
| Apple Business Manager and enterprise | Yes | Yes | Yes | Yes | N/A — the build command is identical to Apple App Store's and was not re-executed; that build produces no `.ipa` without signing, see its §9 | N/A — these are private distribution routes, not testing services; TestFlight is the Apple testing channel | Yes | Yes | Yes | Yes | Yes |
| Ad hoc distribution | Yes | Yes | Yes | Yes | Partial (executed) — the archive command's failure without a signing identity was verified; no `.ipa` was produced, see its §9 | N/A — this channel is a distribution mechanism, not a testing service; TestFlight is the Apple testing channel | Yes | Yes | Yes | Yes | Yes |
