# FREE-WILi2-Firmware

Complete firmware releases for FREE-WILi2. Download the versioned ZIP from
[Releases](https://github.com/freewili/FREE-WILi2-Firmware/releases).
FreeWili GUI's Firmware Updater defaults to **Stable**; **Preview** selects
GitHub pre-releases. Both channels use the same package format.

## Release notes

### v09 - Stable firmware release

The first Stable release since v07. Main, Display, and wifiCPU are all
rebuilt with embedded version **v09** from one source revision. Since
v08-preview.3 it adds the rebuilt 125 kHz RFID reader/writer with its Wave
view, the Display blanking fix (panel hardware reset, tearing-signal watchdog,
I2C wedge recovery), and the **Wireless > ESP32 Mode** OneWili API bridge. The
OneWili stable command IDs changed: ISO-TP is 613-622, Linux CM0 USB Mode is
633, and ESP32 Mode is 634. It also includes all v08 Preview work: verified
wifiCPU updates, the current Display and wifiCPU applications, ISO-TP, and the
Linux additions. See [full notes](releases/v09/README.md). Select **Stable**
and **Refresh** in the updater.

### v08-preview.3 - ISO-TP transport and Linux updates

Rebuilt Main and Display (embedded version **v08**) from the merged
`feat/wificpu-update` + `feat/isotp` revision. Adds the ISO 15765-2 transport
layer under CAN FD (`i\c	`, inline messages up to 256 bytes, SD-staged
larger messages, STmin trim in microseconds), holds the CAN rail while the
transport or the polled receive queue is armed, and carries the Linux shell,
app-browser and file-copy additions. wifiCPU is the unchanged v08-preview.2
image. See [full notes](releases/v08-preview.3/README.md). Select **Preview**
and **Refresh** in the updater.

### v08-preview.2 - Current firmware preview

Fresh builds of Main, Display, and wifiCPU, all with embedded version **v08**.
Includes the current Display application with regenerated ROM assets and the
current ESP32-C5 wifiCPU firmware. Replaces the Day Zero Display/wifiCPU
images carried in preview.1. See [full notes](releases/v08-preview.2/README.md).
Select **Preview** and **Refresh** in the updater. Preview uses explicitly
published packages; it does not automatically follow GitLab commits.

### v08-preview.1 - wifiCPU updater preview

Adds one-button wifiCPU installation and flash verification through Main v08.
The GUI can update Main, Display, and wifiCPU from one ZIP and preserves saved
Wi-Fi settings. New folders and component names use `wifiCPU` (schema 2).
Display v07 and the existing wifiCPU binary retain their embedded versions.
See [full notes](releases/v08-preview.1/README.md). Select **Preview** in the updater.

### v07 - Day Zero DEFCON release

Initial complete release bundle containing the existing Day Zero images:

| Component | Embedded version |
| --- | --- |
| Main | v07 |
| Display | v07 |
| wifiCPU (ESP32-C5) | spartahackFw1final-1743-g349128 |

This packages the existing firmware without changing its bytes. Includes
Display assets, the merged wifiCPU image, wifiCPU flashing
metadata, and a manifest with component sizes and SHA-256 checksums.
See the [full release notes](releases/v07/README.md).

The [release format specification](RELEASE_FORMAT.md) defines the on-disk
format, naming, validation, and Stable/Preview selection rules.

## Release layout

Each release has a permanent `releases/<version>/` folder. The ZIP contains
that folder's contents at its root:

```text
manifest.json
README.md
firmware/FW2Main-v09.uf2
firmware/FW2Display-v09.uf2
wifiCPU/wifiCPU-v09-merged.bin
wifiCPU/flasher_args.json
```

`manifest.json` records the release name/title and each component's embedded
version, filename, byte size, and SHA-256. Component versions may differ from
the bundle version. Keep the UF2 version in its filename. Keep wifiCPU's
embedded build version in its merged binary filename.

The wifiCPU binary is a complete ESP32-C5 merged image. The updater splits it
into firmware regions to preserve NVS and PHY settings; do not flash its padding
over saved settings.
`flasher_args.json` records the split-image metadata; its individual
split-image paths are not additional files included in this ZIP.

## Publish a stable or preview release

1. Copy a complete tested set of images into a new `releases/<version>/`
   folder. Use a unique version, such as `v08` or `v08-preview.1`.
2. Write the release notes in the folder's `README.md` and add a summary to
   this README. Create its manifest using `releases/v08-preview.2/manifest.json` as the schema
   example. Read component versions from the built images and calculate
   their sizes and SHA-256 checksums. Never relabel an old binary as a new
   component version.
3. Validate and package locally:
   ```sh
   python -m unittest discover -s scripts -p 'test_*.py'
   python scripts/package_release.py releases/v07
   ```
   Substitute the new folder for `releases/v07`. Output is
   `dist/FREE-WILi2-<version>.zip` and its `.zip.sha256` checksum.
4. Commit the complete folder and manifest. In **Actions > Publish firmware
   release > Run workflow**, select that commit's branch, enter the folder
   version, and select **preview** or **stable**. Preview is the publishing
   default. The workflow validates the complete bundle, creates a draft
   with the ZIP/checksum attached, then publishes it in the chosen channel.
5. Verify the download in FreeWili GUI using the matching channel before
   hardware testing. Record hardware results before promoting a Preview.
   To promote an already tested Preview without changing its bytes, turn
   off its GitHub pre-release flag and mark it Latest. Keep its existing
   tag, manifest, and ZIP together; a renamed release requires a new bundle.

Published folders, tags, and assets are immutable: corrections get a new
release version. A release must include all components even if only one
changed. Old single-component nightly releases are not installable bundles
and are ignored by the updater. Stable never falls back to Preview, and an
empty Preview channel is shown as unavailable.

The root `firmware/` and `wifiCPU/` files are legacy compatibility copies
of the Day Zero images. New releases go only in `releases/<version>/` and
their GitHub Release ZIP; do not use those legacy paths for publishing.

Historical v07 files retain their original `bottlenose` paths and schema 1.
The root compatibility image now lives in `wifiCPU/` with its embedded version
in the filename. The binary itself is unchanged.
