# Ad Hoc Distribution — Quick Start

Install a signed build on a fixed list of registered devices, shortest safe path. Links back to
the [full guide](../README.md) at every step.

**Before you start:** you need a Mac (or a paired Mac build host), an Apple Developer Program
membership, and the UDID of every target device.

1. Collect each device's UDID and register it in your Apple Developer account. See
   [§6](../README.md#6-how-to-obtain-the-prerequisites).
2. Create an **Ad Hoc** provisioning profile — not App Store — selecting your App ID, your
   distribution certificate, and every device from step 1. Record the profile name. See
   [§6](../README.md#6-how-to-obtain-the-prerequisites).
3. Build, sign **and archive** in one step, naming the profile from step 2:
   `-p:ArchiveOnBuild=true -p:RuntimeIdentifier=ios-arm64` **together with**
   `-p:CodesignKey`/`-p:CodesignProvision`. **Signing without the archive properties writes no
   package.** See [§10](../README.md#10-sign).
4. Confirm the `.ipa` exists by **listing** `bin/Release/net10.0-ios/ios-arm64/publish/`. See
   [§11](../README.md#11-package).
5. Install with Apple Configurator onto a connected, registered device. See
   [§13](../README.md#13-deploy).

STOP — VERIFY BEFORE CONTINUING: register every device **before** you generate the profile in
step 2. Adding a device afterwards does not update a profile that already exists — you must
regenerate the profile, re-sign and redistribute.

STOP — VERIFY BEFORE CONTINUING: at step 4, list the directory. The build log reports a package
even when it wrote none. See [§9](../README.md#9-build).

Device registration slots are limited to 100 per product family per membership year, and
**disabling a device does not free its slot**. Plan the device list before you register anything.
See [§4](../README.md#4-eligibility).
