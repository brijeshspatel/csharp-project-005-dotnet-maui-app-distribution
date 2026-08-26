# Direct APK Distribution

## 1. What This Channel Is

Direct APK distribution means you host a signed `.apk` yourself and the user installs it without a
store. Android calls this installing from an unknown source; it is commonly called sideloading.

**There is no intermediary at all.** No account, no review, no hosting, no update mechanism, and no
one but you deciding what ships.

## 2. When to Use It

Use it when no store can serve the case:

- A device or region where Google Play is unavailable.
- A kiosk, appliance or single-purpose device you control physically.
- An internal tool for a small group, where managed Google Play's EMM requirement is
  disproportionate.
- A build a user must be able to install without any account.

## 3. When Not to Use It

**Do not use it as a convenience.** Every protection the other channels provide is absent here, and
§7 lists what you take on instead.

**Do not use it to reach consumers at scale.** Use
[Google Play public release](../google-play-public-release/README.md).

**Do not use it for an organisation that runs an EMM.** Use
[managed Google Play](../managed-google-play-enterprise/README.md), which keeps Play's update
mechanism.

**Do not use it for testing where Play is available.** The
[testing tracks](../google-play-internal-testing/README.md) handle distribution, opt-in and updates
for you.

**Do not use it if you need to update the app reliably.** See §15. There is no update mechanism.

## 4. Eligibility

**No eligibility requirement, no account, and no fee.** This is the only channel in this repository
with none. Anyone who can build and sign an APK can distribute one.

The absence of a gate is the channel's advantage and its entire risk.

## 5. Prerequisites

| Prerequisite | Notes |
|---|---|
| A JDK, for `keytool` | Install it separately — the .NET Android workload does **not** bundle a JDK, though Visual Studio and Android Studio installs commonly bring one. Any JDK providing `keytool` will do |
| `apksigner`, for verifying a signature | Ships with the Android SDK build-tools. It reads every APK signature scheme; `keytool` reads only the v1 JAR scheme. See §14 |
| A private keystore | Created once, then reused for every update. **Not** the debug keystore |
| A signed `.apk` | The `.aab` is not usable here; see §11 |
| Somewhere to host the file | HTTPS |
| A way to tell users to enable installation from your source | See §13 |

## 6. How to Obtain the Prerequisites

**Create the keystore once.** The same key signs every future update, and it cannot be replaced
later without breaking the update path (§7).

```
keytool -genkeypair -v -keystore {filename}.keystore -alias {keyname} -keyalg RSA -keysize 2048 -validity 10000
```

`keytool` prompts for a password, then for your name, organisational unit, organisation, city,
state and country code. **That information is embedded in the certificate**, though it is not shown
in the app.

**Back up the keystore and its password, separately and durably.** Losing either ends your
ability to ship an update that existing installations will accept. There is no recovery and no
reset — unlike Google Play, there is no key-reset process here, because there is no Google Play.

List the keys in a keystore with:

```
keytool -list -keystore {filename}.keystore
```

**If several JDKs are installed, run `keytool` from the newest.**

## 7. Security Model

**You are the entire trust chain.** Every other channel in this repository interposes a party that
checks something. This one interposes nobody.

| Protection | Google Play | Direct APK |
|---|---|---|
| Policy and security review | Yes | **None** |
| Play App Signing, with key recovery | Yes | **None. Lose the key, lose the update path** |
| Verified delivery over a trusted channel | Yes | **Yours to provide** |
| Automatic updates | Yes | **None** |
| Provenance the user can check | The store listing | **Only what you publish yourself** |

**Google Play Protect still applies.** It scans installed apps, including sideloaded ones. Google's
own wording is that it **may prevent** installation of an app that is unverified and uses sensitive
device permissions — it does not publish a list of which permissions trigger this, and this guide
does not invent one. Treat blocking as a real possibility you cannot predict or test your way out
of, not as a rule you can design around. A legitimate app can be blocked this way. Classification
decisions can be appealed where the app complies with Google's Mobile Unwanted Software principles.

**Do not ask users to disable Play Protect.** It is a signal of malware, users are right to
refuse, and an app distributed with that instruction should not be trusted by anyone.

**Serve the APK over HTTPS**, from a host whose identity a user can check. An APK served over plain
HTTP can be replaced in transit, and the user has no store signature to compare it against.

**Publish the certificate fingerprint** alongside the download so a cautious user can verify what
they received. Read it from your keystore with `keytool -list -keystore <your>.keystore`. Tell
recipients to check it against the package itself with
`apksigner verify --print-certs <downloaded>.apk` — that is what makes the published fingerprint
worth publishing, and unlike `keytool` it reads every APK signature scheme rather than only v1.

## 8. Application Preparation

Identical to [public release §8](../google-play-public-release/README.md#8-application-preparation)
for versioning: increment `ApplicationVersion` for every release you distribute, because your own
update mechanism (§15) will need to compare versions.

**If your app installs other APKs itself**, it needs the `REQUEST_INSTALL_PACKAGES` permission,
which takes effect when the app targets API level 26 or later on Android 8 or later. That
permission is separately policed where the app is also distributed through Play.

## 9. Build

**Verified by execution against this repository's own sample application**
(`sample/DistributionSample`), 2026-08-24, from a fully clean tree with `bin/` and `obj/` removed.

Ask for the APK format explicitly, and supply the signing properties:

```
dotnet publish -f net10.0-android -c Release ^
  -p:AndroidEnableMarshalMethods=false ^
  -p:AndroidPackageFormats=apk ^
  -p:AndroidKeyStore=true ^
  -p:AndroidSigningKeyStore=<path-to-keystore> ^
  -p:AndroidSigningKeyAlias=<key-alias> ^
  -p:AndroidSigningKeyPass=env:AndroidSigningPassword ^
  -p:AndroidSigningStorePass=env:AndroidSigningPassword
```

This exits 0 and writes to `bin/Release/net10.0-android/publish/`:

| Artefact | Size | Signed? |
|---|---|---|
| `com.companyname.distributionsample.apk` | 28,945,466 bytes | No v1 signature — `keytool -printcert` reports `Not a signed jar file`. See the caveat below |
| `com.companyname.distributionsample-Signed.apk` | 29,070,595 bytes | Yes |

**Four things were confirmed, each by inspecting the result rather than reading the log:**

1. **The artefacts exist**, by listing the directory. Sizes are quoted from the files.
2. **The signed APK carries the intended key.** `keytool -printcert -jarfile` reports the
   certificate created for this verification, not a debug certificate. **The signature algorithm
   you see depends on the key size you generated**, so do not treat any specific value here as the
   expected one — a 2048-bit RSA key as generated by the `keytool` command in §6 signs with
   `SHA256withRSA` on current JDKs, while larger keys move to `SHA384withRSA`. What matters is that
   the certificate is *yours*, not which digest it names.

   **Caveat on the tool used, carried forward from a later review.** `keytool -printcert -jarfile`
   reads only the **v1 (JAR)** signature scheme. Its `Not a signed jar file` result for the
   unsigned artefact above therefore establishes the absence of a *v1* signature, not the absence
   of every signature — an APK signed with v2/v3 only produces the same message. The conclusion
   here still holds, because the two artefacts differ and the signed one presents the expected
   certificate, but **§14 now prescribes `apksigner verify --print-certs`** for validation, which
   reads every scheme and does not have this blind spot.
3. **No `.aab` was produced**, which confirms `AndroidPackageFormats=apk` took effect. A release
   build defaults to `aab;apk`.
4. **The password did not reach the build log.** Searching the full log for the passphrase returns
   zero matches, which confirms the `env:` prefix behaves as documented.

The keystore used was created with `keytool` for this verification only, kept outside the
repository, and is not committed. See §18.

**Property names that are easy to get wrong:**

| Property | Note |
|---|---|
| `AndroidPackageFormats` | **Plural.** The default for a release build is `aab;apk`, which produces both. Set `apk` to produce only what this channel needs |
| `AndroidKeyStore` | Defaults to `false`. Without `true`, the signing properties are ignored and you get a debug-signed package |
| `AndroidSigningKeyPass` / `AndroidSigningStorePass` | The default keystore type assumes these are the same value |

**`-p:AndroidEnableMarshalMethods=false` is not optional on the verified toolchain.** Without it
the build fails with `XAGNM7009`, exactly as documented in the
[public release guide's §9](../google-play-public-release/README.md#9-build).

## 10. Sign

Signing happens during the build above; there is no separate step. Two details matter more here
than elsewhere.

**Keep the password out of the build log.** `AndroidSigningKeyPass` and `AndroidSigningStorePass`
both accept an `env:` prefix naming an environment variable, or a `file:` prefix naming a file:

```
-p:AndroidSigningKeyPass=env:AndroidSigningPassword
-p:AndroidSigningKeyPass=file:C:\path\AndroidSigningPassword.txt
```

The `env:` form was used for the verification in §9.

**Microsoft documents that the `env:` prefix is not supported when the package format is `aab`.**
It works for this channel because this channel produces an `apk`, so the restriction cannot bite
here whatever its exact scope.

**One caveat on that restriction.** Microsoft states it against the **deprecated singular**
`$(AndroidPackageFormat)`, not the plural `$(AndroidPackageFormats)` the same pages tell you to
use — and whose Release default is `aab;apk`. How the restriction applies to
`AndroidPackageFormats=aab`, or to that mixed default, is **not documented**. Where your output
includes an App Bundle, prefer the `file:` prefix, which carries no such restriction.

**Never commit a keystore or a password.** Set the keystore path and alias in the project file if
you wish; keep the passwords on the command line, in an environment variable, or in a file outside
the repository.

## 11. Package

**The `.apk` is the artefact for this channel. The `.aab` is not usable.** An Android App Bundle is
an upload format that a store turns into per-device APKs; a user cannot install one. This is the
opposite of the Google Play channels, where the `.aab` is the only acceptable upload.

A release build writes to `bin/Release/net10.0-android/publish/`. **Confirm the `.apk` is there by
listing the directory** — see the public release guide's §9 for why a build log is not evidence.

The signed file carries `-Signed` in its name. **Distribute the signed one.**

## 12. Configure Distribution Platform

**There is no platform.** Host the `.apk` where your users can reach it over HTTPS, and publish
alongside it:

- The version, so a user can tell whether they already have it.
- The certificate fingerprint from §7.
- Plain instructions for §13, because the install will not proceed without them.

## 13. Deploy

The user opens the download link on the Android device. Android begins installing it **only if that
source is permitted to install apps.**

| Android version | What the user must do |
|---|---|
| **8.0 (API 26) and higher** | Open **Install unknown apps** in system settings and permit **the specific app** doing the installing — usually the browser or file manager. It is per-source, not global |
| **7.1.1 (API 25) and lower** | Enable the global **Unknown sources** setting, under **Settings > Security** |

**The per-source model surprises people.** Permitting a browser once does not permit a file
manager later. A user who transfers the APK and installs it a different way must permit that app
too.

Expect Play Protect to inspect the app at install (§7).

## 14. Validate

1. **List the publish directory** and confirm the signed `.apk` exists.
2. Confirm the signature **of the APK itself** with `apksigner verify --print-certs <your>.apk`,
   and check the fingerprint matches what you publish.

   **Use `apksigner`, not `keytool`, for this.** `keytool -list` reads a *keystore*, not a package.
   `keytool -printcert -jarfile` does read a package, but only the **v1 (JAR) signature scheme** —
   on an APK signed with v2/v3 only it reports `Not a signed jar file`, which is
   indistinguishable from a genuinely unsigned file. `apksigner` understands every scheme and
   reports which ones are present, so it is the only one of the three that answers the question
   this step is asking.
3. Install on a device that has **never** had a debug build of this app. A debug-signed install
   already present blocks a release-signed install with a signature mismatch, and that failure is
   easy to misread as a broken package.
4. Confirm the app launches.
5. Download it through the real hosting path, on a device that has not yet permitted your source —
   this is the only way to see what a first-time user actually faces.

## 15. Update

**This channel has no update mechanism. Nothing tells the user a new version exists, and nothing
installs it.**

Your options, in the order most projects should consider them:

| Approach | Note |
|---|---|
| Move to a store or EMM channel | The most reliable fix. This limitation is intrinsic, not incidental |
| Build an in-app version check | The app fetches a version file and tells the user to download. The user still installs manually, and still needs §13's permission |
| Notify out of band | Email or a message with the new link. Adoption is whatever people choose |

**Every update must be signed with the same key** as the installed version. Android refuses an
update signed by a different key — that is what §6's backup warning protects.

## 16. Revoke / Withdraw / Retire

**There is no revocation.** No store to unpublish from, no EMM to remove it with, and no list of
who installed it.

Withdrawing the download removes future installs only. An installed copy runs indefinitely, at
whatever version it has, until the user removes it.

**A serious defect shipped through this channel cannot be recalled.** If that risk is
unacceptable, this is the wrong channel — decide before distributing, not after.

## 17. Troubleshooting

| Symptom | Likely Cause | How to Verify | Corrective Action |
|---|---|---|---|
| No `.apk` in the publish folder, only `.aab` | `AndroidPackageFormats` not set to `apk` | Check the property name — it is plural | Set `-p:AndroidPackageFormats=apk`, per §9 |
| The APK is debug-signed | `AndroidKeyStore` left at its default of `false` | Check the property is set to `true` | Set `-p:AndroidKeyStore=true`, per §9 |
| Install fails with a signature mismatch | A build signed with a different key is already installed, often a debug build | Check what is installed on the device | Uninstall the existing app first, then install. For a real update, sign with the original key |
| Install does not start after download | The source is not permitted to install apps | Check **Install unknown apps** for the app that opened the file | Permit that specific app, per §13 |
| Permitting the browser did not help | The install was started by a different app, such as a file manager | Check which app is performing the install | Permit that app too. The setting is per-source |
| Play Protect blocks the install | The app requests sensitive permissions and came from outside a store | Read the Play Protect message | Reduce the permissions if you can. Appeal where the app complies with the Mobile Unwanted Software principles. **Never tell users to disable Play Protect** |
| Password appears in the build log | The password was passed literally | Search the log for the value | Use the `env:` or `file:` prefix, per §10 |
| Build fails with `XAGNM7009` | Marshal methods, enabled by default in .NET 10 | Re-run from a clean tree; it reproduces | Add `-p:AndroidEnableMarshalMethods=false`, per §9 |

## 18. Limitations

**What was verified: build, signing and packaging**, by execution against this repository's own
sample application, from a clean tree, with the artefact confirmed on disk (§9). A throwaway
keystore was created with `keytool` for that verification and kept outside the repository; **no
keystore, password or certificate is committed anywhere in this project.**

**What was not verified: everything after the file exists.** No device installation, no Play
Protect interaction, and no hosting were exercised. §13-§16 rest on the sources in §19.

**The `-Signed` APK produced in §9 is signed with a throwaway verification key**, not a real
distribution identity. It demonstrates that the signing path works; it is not a distributable
artefact.

**This channel's limitations are structural, not gaps in this guide.** No updates, no revocation
and no review are properties of distributing without an intermediary. They cannot be mitigated
away, only accepted or avoided by choosing another channel.

## 19. Official Sources

- [Publish an Android app using the command line — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/maui/android/deployment/publish-cli?view=net-maui-10.0)
- [Use Google Play Protect to help keep your apps safe and your data private — Google Play Help](https://support.google.com/googleplay/answer/2812853?hl=en)
- [Use of the REQUEST_INSTALL_PACKAGES permission — Play Console Help](https://support.google.com/googleplay/android-developer/answer/12085295?hl=en)
- [Alternative distribution options — Android Developers](https://developer.android.com/distribute/marketing-tools/alternative-distribution)

## 20. Last Verified

**Sources last verified: 2026-08-26.** Every claim resting on §19's sources was re-checked on that
date. That pass qualified §10's `env:` prefix restriction with what Microsoft actually documents —
the restriction is written against the deprecated singular `$(AndroidPackageFormat)`, and its
effect on the plural `$(AndroidPackageFormats)` is undocumented.

**Execution evidence: 2026-08-24.** The §9 build, signing and packaging claims were verified by
execution against this repository's own sample application, from a clean tree, with the artefact
confirmed on disk. **That date does not advance when sources are re-verified.** Installation, Play
Protect behaviour and hosting are **not** execution-verified; see §18.
