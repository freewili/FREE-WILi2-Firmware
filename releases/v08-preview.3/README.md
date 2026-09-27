# v08-preview.3 - ISO-TP transport and Linux updates

Fresh builds of the current FREE-WILi2 Main and Display firmware, with the
wifiCPU image carried over unchanged from v08-preview.2. This is an explicitly
published Preview snapshot.

| Component | Embedded version |
| --- | --- |
| Main | v08 |
| Display | v08 |
| wifiCPU (ESP32-C5) | v08 (same image as v08-preview.2) |

## Changes

- **ISO 15765-2 (ISO-TP) transport layer** on Main, under **CAN FD > ISO-TP
  Transport** (`i\c\t`): single frame, first frame / consecutive frames with
  flow control, classic CAN and CAN FD (escape forms, 32-bit first-frame
  length), normal and extended addressing, padding. Messages up to 256 bytes
  travel inline through the console/OneWili API; larger messages are sent from
  a file on the SD card and long received messages land in a configurable
  receive file. STmin is followed from the controller's transmit-complete
  event with a user trim in signed microseconds and an optional override.
  OneWili bindings include the ten new commands (stable IDs 614-623).
- **CAN rail hold**: an enabled ISO-TP transport or an armed polled CAN
  receive queue now keeps the CAN power zone up. Previously the rail dropped
  about two seconds after the host CAN stream was switched off and every
  later transfer timed out against an unpowered controller.
- **Console input line** raised from 512 to 1024 characters so a 256-byte
  payload fits on one command.
- **Linux (CM0)**: capability-checked USB mode command, framed shell sessions,
  SD app browsers, cancellable file copies between Linux and the Main SD card
  (carried from the feat/wificpu-update line since v08-preview.2).
- Main retains the verified wifiCPU update protocol from v08-preview.1/2.
- Display: rebuilt from the same source revision with the regenerated ROM
  asset pack (asset pack bytes unchanged from v08-preview.2).

Firmware source revision: `81a1832386faca87b3a6c909252547fcb1162368`
(branch `release/v08-preview.3` = `feat/wificpu-update` at `9a4f0f99` merged
with `feat/isotp` at `ae07782c`). The wifiCPU binary and its flashing metadata
are byte-identical to v08-preview.2 (source unchanged since that build).

## Install

In a current FreeWili GUI, open **Setup > Firmware Updater**, choose
**GitHub release > Preview**, and press **Refresh**. Confirm
**v08-preview.3 - ISO-TP transport and Linux updates**, then
**Update and verify**. Keep USB power connected until completion. The
updater installs Main first. wifiCPU is unchanged from v08-preview.2 and may
be skipped on a device that already runs it.

wifiCPU installation requires an RP SD card owned by Main. The updater
checks the merged ESP32-C5 image and writes only its bootloader, partition
table, application, and storage regions. It preserves NVS and PHY settings.

Preview selects the newest explicitly published Preview package. It does
not track a GitLab branch or automatically publish new commits. Stable
remains the separate v07 Day Zero DEFCON release.

## Validation and limitations

Release builds, embedded versions (`FW2 v08`, `FW2Display v08`), the Display
asset pack check, the complete Display UF2 packaging (Display and absolute
asset families preserved), the ISO-TP engine host tests (30 cases), and the
menutool binding checks were run before packaging. The ZIP manifest contains
sizes and SHA-256 hashes for every component.

The ISO-TP transport was verified end to end on FREE-WILi2 hardware against a
ValueCAN 4-2 through Vehicle Spy AI (10 of 10 scenarios: single frames,
segmented messages both directions, 4095-byte and 20480-byte sends from the SD
card, receive into a file, and an STmin trim sweep whose measured bus gaps
match STmin + trim within a few microseconds plus a constant ~330 us of frame
and SPI time). That verification used the ISO-TP development build; the exact
packaged images in this ZIP were produced from the merged release revision and
checked structurally (versions, UF2 families, manifest hashes) but had not yet
been installed through the FreeWili GUI updater at publication time. Run
**Update and verify** and record the result before any Stable promotion.

This is development firmware for testing, not a Stable promotion. Known
limitations: an ISO-TP transfer blocks the Main application loop for its
duration (up to the configured maximum); a CAN controller that has gone
bus-off while a peer keeps retrying an unacknowledged frame does not recover
until the CAN mode is re-applied; the STmin reference uses the polled
transmit-complete read rather than the controller's hardware timestamp.
Main and the Display debug-probe fallback currently require Windows. Only the
standard onboard ESP32-C5 factory partition layout is supported. No separate
debug-probe, PIC, LoRa module, or Linux OS images are included.
