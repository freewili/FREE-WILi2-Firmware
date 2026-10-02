# v09 - Stable firmware release

The first Stable FREE-WILi2 firmware since the v07 Day Zero DEFCON release.
Fresh builds of all three processors from one source revision, with the v08
Preview work and the latest Main and Display fixes.

| Component | Embedded version |
| --- | --- |
| Main | v09 |
| Display | v09 |
| wifiCPU (ESP32-C5) | v09 |

## New since v08-preview.3

- **RFID rebuild** (125 kHz, Joey plug-in): reads EM4100, Indala and
  HID/FSK-family credentials with a latched tag readout. Write & Save stores
  read cards on the SD card and writes EM4100, HID Prox or Indala to a T5577.
  A new Wave view shows the reader's ASK/FSK/PSK signal with zoom,
  decode-anchored capture, histogram/spectrogram views, and screenshots.
- **Display blanking fix**: every LCD recovery now pulses the panel's hardware
  reset, and a tearing-signal watchdog detects a panel that has stopped
  refreshing. A wedged sensor I2C bus is recovered at runtime. I2C transfers
  no longer report spurious timeouts when a core was briefly preempted.
- **OneWili over the wifiCPU**: new **Wireless > ESP32 Mode** setting.
  **Default Firmware** runs the stock wifiCPU application. **OneWili API**
  hands the link to an app running on the ESP32-C5: Main answers its OneWili
  commands and mirrors events to it. The OneWili bridge is shared by Display
  and ESP32 clients. Raw binary capture frames are preserved in the generated
  bindings.
- **OneWili stable command IDs**: ISO-TP uses IDs 613-622 (v08-preview.3
  used 614-623). Linux CM0 USB Mode is 633 and ESP32 Mode is 634.
  Regenerate any client built against the v08-preview.3 bindings.

## Changes since v07 (Stable)

- **wifiCPU updater**: one-button wifiCPU installation through Main. Every
  written flash region is checked by MD5 and saved Wi-Fi settings are
  preserved (v08-preview.1).
- **Current Display application** with regenerated ROM assets, including
  display power recovery, screenshot controls, persistent volume, and LED
  brightness settings (v08-preview.2).
- **Current wifiCPU firmware** with its Wi-Fi/BLE and terminal services,
  built for the ESP32-C5 with ESP-IDF 6.0.1 (v08-preview.2).
- **ISO 15765-2 (ISO-TP) transport** under **CAN FD > ISO-TP Transport**:
  inline messages up to 256 bytes, larger messages sent from and received
  into files on the SD card, and an STmin trim in microseconds. An armed
  ISO-TP transport or CAN receive queue keeps the CAN rail powered. The
  console input line is 1024 characters (v08-preview.3).
- **Linux (CM0)**: framed shell sessions, SD app browsers, cancellable file
  copies between Linux and the Main SD card, and a capability-checked USB
  mode command.

Firmware source revision: `fdbeaf8c1ccae1fc1ef6f9919e973c0a1e809e5b`
(branch `release/v09`: `main` at `023d9316` merged with `feat/wificpu-update`
at `2f62de35`, then the v09 version bump). The Display ROM asset pack is
byte-identical to v08-preview.2 and v08-preview.3.

## Install

In a current FreeWili GUI, open **Setup > Firmware Updater**, choose
**GitHub release > Stable**, and press **Refresh**. Confirm
**v09 - Stable firmware release**, then **Update and verify**. Keep USB
power connected until completion. Install all three components for the
matching firmware set. The updater installs Main first, so a device on v07
gains the verified wifiCPU update protocol before wifiCPU is written.

wifiCPU installation requires an RP SD card owned by Main. The updater
checks the merged ESP32-C5 image and writes only its bootloader, partition
table, application, and storage regions. It preserves NVS and PHY settings.
Use a GUI that supports schema 2 packages and verified wifiCPU updates.

## Validation

Release builds, embedded versions (`FW2 v09`, `FW2Display v09`, wifiCPU
`v09`), the Display asset pack, complete Display UF2 packaging (Display and
absolute asset families preserved), the ESP32-C5 image and partition
checksums, and the OneWili stable command-ID check were run before
packaging. The ZIP manifest contains sizes and SHA-256 hashes for every
component.

The exact packaged images were installed on FREE-WILi2 hardware:

- **Main** through its partition-aware recovery loader, the same path the
  updater uses. The application flash was read back over SWD and matched
  the UF2 byte for byte. Main restarted and answered requests.
- **Display**, the complete image with assets, was programmed over the
  on-board debug probe, the updater's fallback path, and passed full flash
  read-back verification. The home screen rendered and Main's display link
  answered.
- **wifiCPU** through Main's verified update command, from this package's
  merged image split into its four regions. All four regions passed MD5
  verification and the restart completed. The ESP32-C5 then powered up,
  answered Main, and completed a Wi-Fi scan.

## Known limitations

An ISO-TP transfer blocks the Main application loop for its duration (up to
the configured maximum). A CAN controller that has gone bus-off while a peer
keeps retrying an unacknowledged frame does not recover until the CAN mode is
re-applied. The STmin reference uses the polled transmit-complete read rather
than the controller's hardware timestamp. Main installation and the Display
debug-probe fallback currently require Windows. Only the standard onboard
ESP32-C5 factory partition layout is supported. No separate debug-probe, PIC,
LoRa module, or Linux OS images are included.
