# FREE-WILi2 firmware release format (schema 2)

## Release identity and channels

A release is a complete, tested set of Main, Display, and wifiCPU images.
It lives at `releases/<version>/` in this repository. `<version>` starts with
`v` and a digit, followed by ASCII letters, digits, dots, or hyphens: for
example `v07`, `v08`, or `v08-preview.1`. The folder, GitHub tag, manifest
`release`, and ZIP filename must agree. The human-readable `title` may include
spaces, such as `v07 - Day Zero DEFCON release`.

* **Stable:** published GitHub Releases with `prerelease: false`.
* **Preview:** published GitHub Releases with `prerelease: true`.
* Draft releases are never selectable. The updater chooses the most recently
  published complete package in the selected channel. Single-component
  releases without the expected ZIP are ignored. An empty channel is
  unavailable; there is no silent fallback to a different channel.

Channel is GitHub release metadata, not embedded in the ZIP. A tested
Preview can therefore become Stable without changing its bytes or identity.
Published files and tags must never be replaced in place. Use a new release
version for a correction. Component versions are independent of the bundle
version and must reflect the actual embedded firmware identities.

## Archive and manifest

The uploaded release assets are `FREE-WILi2-<version>.zip` and
`FREE-WILi2-<version>.zip.sha256`. Use the standard ZIP format with stored or
DEFLATE members, no encryption, no ZIP64, and no symlinks. The ZIP's root is
the release folder's contents (no extra wrapping directory):

```text
README.md
manifest.json
firmware/FW2Main-<main-version>.uf2
firmware/FW2Display-<display-version>.uf2
wifiCPU/wifiCPU-<wifiCPU-version>-merged.bin
wifiCPU/flasher_args.json
```

`README.md` is mandatory and contains the release title, component versions,
changes, installation information, and known limitations. Its contents also
become the GitHub Release notes. The repository README contains a release
history summary and links to these per-release notes.

`manifest.json` is UTF-8 JSON. See the complete real
[current manifest](releases/v08-preview.1/manifest.json). Required top-level fields:

| Field | Meaning |
| --- | --- |
| `schema` | Integer `2` |
| `product` | Exact string `FREE-WILi2` |
| `release` | Bundle version matching the folder/tag/ZIP |
| `title` | Human-readable release name |
| `files` | Exactly four component records below |

Every file record contains `component`, `version`, `file`, `size` (bytes),
and `sha256` (64 lowercase hexadecimal digits). Components are exactly
`main`, `display`, `wifiCPU`, and `wifiCPU-flasher-args`, once each.
The flashing metadata uses the same version as its wifiCPU image.
Paths are case-sensitive relative paths with one folder and one filename;
absolute paths, backslashes, `..`, duplicate paths/components, and unlisted
files are rejected. Main and Display use their UF2 embedded version in the
filename. wifiCPU uses its ESP-IDF app descriptor version.

The merged wifiCPU image is an ESP32-C5 factory image for base offset `0x0`.
Do not write the entire merged image over an existing device: its padding covers
saved settings. The updater validates the C5 image headers, segment checksums,
SHA-256 digests, ESP-IDF identity and partition-table MD5, then splits the image:

| Region | Offset | Limit |
| --- | --- | --- |
| Bootloader | `0x2000` | Before `0x8000` |
| Partition table | `0x8000` | 4 KiB |
| Application | `0x10000` | 2 MiB factory partition |
| Storage | `0x210000` | 16 KiB |

NVS (`0x9000..0xefff`) and PHY (`0xf000..0xffff`) are never programmed.
Other layouts require a new installer implementation; do not silently reinterpret
them. `flasher_args.json` describes the split-image offsets and names; these
split files are not additional ZIP members. The GUI creates them in memory.
The historical embedded ESP-IDF project identity `bottlenose` remains valid;
renaming the distribution does not change that binary or its embedded version.

## Integrity and installation

Maximum compressed archive size is 96 MiB; maximum total extracted data is
128 MiB. Individual images are at most 40 MiB. README/manifest/flasher
metadata are each at most 64 KiB. Only the six expected file members are
accepted. Extraction takes place in memory, never at archive-supplied paths.

The updater pins the selected release asset's download URL, size, and
GitHub SHA-256 digest, checks the ZIP before opening it, checks member CRCs,
and validates all manifest sizes/SHA-256 hashes before any firmware update.
Main and Display UF2 validation independently checks processor identity,
block completeness, addresses, and supported UF2 flags. The filename does
not authorize flashing a target. Changing a channel clears the previous
selection; Update uses the displayed release, not a newer release published
silently during the operation.

The updater installs Main, Display and wifiCPU. wifiCPU needs Main v08 or newer
and an RP SD card owned by Main. Main is updated first when included. Each
wifiCPU region must pass flash MD5 read-back; success also requires the current
update token, four verified regions, and an acknowledged reset. A stale result,
write/verify failure, or missing acknowledgement is never success. Local UF2 and
wifiCPU merged BIN files are supported independently of release packages.

Schema 1 is retained for immutable historical releases such as v07. It used
`bottlenose` and `bottlenose-flasher-args` components and a `bottlenose/` folder.
New releases use schema 2 and the exact case-sensitive name `wifiCPU`. Never
rewrite a published folder or ZIP just to apply the new name. v07's Main cannot
perform verified wifiCPU installation; select the newer Preview or install
only Main/Display from the older bundle.

## Produce a release

Follow the publishing steps in [README.md](README.md). The deterministic
packager `scripts/package_release.py` validates embedded component versions,
filenames, manifest hashes, and completeness before writing the ZIP and its
checksum. The **Publish firmware release** workflow requires an explicit
channel, defaulting to Preview, and publishes only after assets are attached.
