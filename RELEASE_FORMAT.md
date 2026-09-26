# FREE-WILi2 firmware release format (schema 1)

## Release identity and channels

A release is a complete, tested set of Main, Display, and Bottlenose images.
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
bottlenose/bottlenose-<bottlenose-version>-merged.bin
bottlenose/flasher_args.json
```

`README.md` is mandatory and contains the release title, component versions,
changes, installation information, and known limitations. Its contents also
become the GitHub Release notes. The repository README contains a release
history summary and links to these per-release notes.

`manifest.json` is UTF-8 JSON. See the complete real
[v07 manifest](releases/v07/manifest.json). Required top-level fields:

| Field | Meaning |
| --- | --- |
| `schema` | Integer `1` |
| `product` | Exact string `FREE-WILi2` |
| `release` | Bundle version matching the folder/tag/ZIP |
| `title` | Human-readable release name |
| `files` | Exactly four component records below |

Every file record contains `component`, `version`, `file`, `size` (bytes),
and `sha256` (64 lowercase hexadecimal digits). Components are exactly
`main`, `display`, `bottlenose`, and `bottlenose-flasher-args`, once each.
The flashing metadata uses the same version as its Bottlenose image.
Paths are case-sensitive relative paths with one folder and one filename;
absolute paths, backslashes, `..`, duplicate paths/components, and unlisted
files are rejected. Main and Display use their UF2 embedded version in the
filename. Bottlenose uses its ESP-IDF app descriptor version.

The merged Bottlenose image is for ESP32-C5 at offset `0x0`. Original
`flasher_args.json` contains split-image source build paths; these are
metadata and are not extra ZIP members.

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

The current updater installs Main and Display. Bottlenose is bundled and
integrity checked for separate installation. Local UF2 input remains
supported independently of release packages.

## Produce a release

Follow the publishing steps in [README.md](README.md). The deterministic
packager `scripts/package_release.py` validates embedded component versions,
filenames, manifest hashes, and completeness before writing the ZIP and its
checksum. The **Publish firmware release** workflow requires an explicit
channel, defaulting to Preview, and publishes only after assets are attached.
