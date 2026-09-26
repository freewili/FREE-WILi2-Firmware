# v08-preview.1 - wifiCPU updater preview

Preview firmware for testing the new wifiCPU updater in FreeWili GUI.

| Component | Embedded version |
| --- | --- |
| Main | v08 |
| Display | v07 |
| wifiCPU (ESP32-C5) | spartahackFw1final-1743-g349128 |

## Changes

- One-button wifiCPU installation through Main with MD5 verification of every
  written flash region and an explicit result for the current update session.
- Fix the C5 flashing stub byte count so partially filled flash sectors finish
  successfully. Failed finish, verification, or reset commands fail the update.
- Use the exact name `wifiCPU` in the GUI, package folder, binary filename and
  manifest component names. Schema 2 documents this naming; immutable v07
  packages retain schema 1 and their historical names.
- Display and wifiCPU firmware bytes are unchanged from Day Zero. The wifiCPU
  binary retains its historical embedded project identity and build version.

Main source revision: `0b6a2431cf87a266fc463fc54acd8406999b2583`.
This is a development firmware Preview, not a promoted Stable release.

## Install

Use the updated FreeWili GUI, open **Setup > Firmware Updater**, choose
**GitHub release > Preview**, then **Update and verify**. Main, Display and
wifiCPU can be selected independently. A complete update installs Main first
so older devices gain the verified wifiCPU protocol.

wifiCPU requires Main v08 or newer and an RP SD card owned by Main. The GUI
checks the merged ESP32-C5 image and transfers only bootloader, partition table,
application and storage. NVS and PHY regions holding saved settings are left
untouched. Keep USB power connected until completion. A local merged `.bin`
can also be used after Main has been upgraded.

## Validation and limitations

Main v08 was installed through the fused loader and its application response
checked on FREE-WILi2 hardware. The GUI transferred the wifiCPU image with CRC
checks, flashed it, verified all four regions by MD5 read-back and requested
restart. Corrupt images, wrong targets/layouts, stale results and partial
verification are covered by automated checks.

Only the standard FREE-WILi2 ESP32-C5 factory layout is supported. Arbitrary
ESP32 binaries and OTA layouts are refused. Main installation requires Windows;
wifiCPU flashing uses Main's onboard connection and does not need an ESP USB
driver. Use a current GUI that understands schema 2. Main v07 does not support
verified wifiCPU flashing. Main restart verification is not a raw flash read-back.
