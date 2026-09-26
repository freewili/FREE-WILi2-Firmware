# v08-preview.2 - Current firmware preview

Fresh builds of the current FREE-WILi2 Main, Display, and onboard ESP32-C5
wifiCPU firmware. This is an explicitly published Preview snapshot.

| Component | Embedded version |
| --- | --- |
| Main | v08 |
| Display | v08 |
| wifiCPU (ESP32-C5) | v08 |

## Changes

- Replace the Day Zero Display and wifiCPU images used in preview.1 with
  builds from the current firmware sources. All three processors now use
  embedded version v08; filenames and manifest versions match the images.
- Include the current Display application and regenerated ROM assets in one
  complete UF2. The application includes the current display power recovery,
  screenshot controls, persistent volume, and LED brightness settings.
- Include the current wifiCPU implementation, including its Wi-Fi/BLE and
  terminal services, built for ESP32-C5 with ESP-IDF 6.0.1.
- Retain Main's verified wifiCPU update protocol and current Linux shell,
  app browsing, and cancellable file-copy support.

Firmware source revision: `eacc554d9a79ed04a592427bf61d203f7a030277`.
Release assembly/documentation revision:
`792fb66e28a6fe6543b60fdd345023e28a64765d`.
The wifiCPU binary retains its historical internal ESP-IDF project identity;
its distribution name and embedded version are `wifiCPU` and `v08`.

## Install

In a current FreeWili GUI, open **Setup > Firmware Updater**, choose
**GitHub release > Preview**, and press **Refresh**. Confirm
**v08-preview.2 - Current firmware preview**, then **Update and verify**.
Keep USB power connected until completion. Install all three components for
the matching firmware set; the updater installs Main first.

wifiCPU installation requires an RP SD card owned by Main. The updater
checks the merged ESP32-C5 image and writes only its bootloader, partition
table, application, and storage regions. It preserves NVS and PHY settings.

Preview selects the newest explicitly published Preview package. It does
not track a GitLab branch or automatically publish new commits. Stable
remains the separate v07 Day Zero DEFCON release.

## Validation and limitations

Release builds, embedded versions, complete UF2 block/address validation,
Display asset generation, ESP32-C5 image/partition checksums, and native
wifiCPU protocol tests were checked before publication. The ZIP manifest
contains sizes and SHA-256 hashes for every component.

The exact packaged images were installed individually through FreeWili GUI
on FREE-WILi2 hardware. Main restarted and answered an application request;
Display passed complete flash read-back, application-response, and LCD-power
checks; wifiCPU passed MD5 verification of all four flash regions and an
acknowledged restart request. Saved NVS and PHY regions were excluded from
the wifiCPU programming plan.

This is development firmware for testing, not a Stable promotion. Main and
the Display debug-probe fallback currently require Windows. Only the
standard onboard ESP32-C5 factory partition layout is supported; use a GUI
that supports schema 2 and verified wifiCPU updates. Main restart checking
is not a raw flash read-back. No separate debug-probe, PIC, LoRa module, or
Linux OS images are included.
