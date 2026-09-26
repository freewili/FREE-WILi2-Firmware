# FREE-WILi2-Firmware

Complete firmware releases for FREE-WILi2. Download the versioned ZIP from
[Releases](https://github.com/freewili/FREE-WILi2-Firmware/releases).
FreeWili GUI's Firmware Updater defaults to **Stable**; **Preview** selects
GitHub pre-releases. Both channels use the same package format.

## Release notes

### v07 - Day Zero DEFCON release

Initial complete release bundle containing the existing Day Zero images:

| Component | Embedded version |
| --- | --- |
| Main | v07 |
| Display | v07 |
| Bottlenose (ESP32-C5) | spartahackFw1final-1743-g349128 |

This packages the existing firmware without changing its bytes. Includes
Display assets, the merged Bottlenose image, original Bottlenose flashing
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
firmware/FW2Main-v07.uf2
firmware/FW2Display-v07.uf2
bottlenose/bottlenose-spartahackFw1final-1743-g349128-merged.bin
bottlenose/flasher_args.json
```

`manifest.json` records the release name/title and each component's embedded
version, filename, byte size, and SHA-256. Component versions may differ from
the bundle version. Keep the UF2 version in its filename. Keep Bottlenose's
embedded build version in its merged binary filename.

The Bottlenose binary is a complete ESP32-C5 merged image for offset `0x0`.
`flasher_args.json` preserves the original build metadata; its individual
split-image paths are not additional files included in this ZIP.

## Publish a stable or preview release

1. Copy a complete tested set of images into a new `releases/<version>/`
   folder. Use a unique version, such as `v08` or `v08-preview.1`.
2. Write the release notes in the folder's `README.md` and add a summary to
   this README. Create its manifest using `releases/v07/manifest.json` as the schema
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

The root `firmware/` and `bottlenose/` files are legacy compatibility copies
of the Day Zero images. New releases go only in `releases/<version>/` and
their GitHub Release ZIP; do not use those legacy paths for publishing.
