# v10 - Stable firmware release

Fresh builds of all three processors from one source revision. v10 fixes
Main running its program from flash far below full speed, and Main
reformatting its internal flash on every boot without a microSD card. It also
adds per-port USB-A power control, 10BASE-T1L, SAE J1708, Modbus RTU/TCP, and
a capture mode in the wifiCPU.

| Component | Embedded version |
| --- | --- |
| Main | v10 |
| Display | v10 |
| wifiCPU (ESP32-C5) | v10 |

## Fixes since v09

- **Main runs at full flash speed.** After its second-stage bootloader handed
  over, Main read its program from flash in the slowest single-bit mode at
  about 0.6 MHz, so every flash cache miss stalled the processor. Main now sets
  up quad-SPI execute-in-place at boot, and keeps it after every flash write
  (settings saves, `flsh:` writes). Main is faster across the board. An rTHON
  loop went from about 6 to about 84,000 statements per second, and a
  `dev.*` call such as `device_state()` went from about 800 ms to 0.6 ms.
- **Internal flash is no longer erased at boot.** With no microSD card fitted,
  every Main boot reformatted the internal flash volume (`flsh:`), which wiped
  files and left a card-less board with no saved settings. Main now formats
  that volume only when it holds no file system at all.
- **Settings are stored in internal flash again** (`flsh:settings`). Settings
  that earlier firmware saved on the SD card (`1:/settings`) are still read
  when no copy exists in flash and the card is mounted. The next save writes
  them to flash, so your existing settings carry over.
- **Scripts and files on internal flash:**
  - A path that names a volume (`flsh:`, `0:`, `1:`) or starts at `/` is
    treated as absolute, so rTHON scripts on internal flash can be run.
  - An rTHON script on the SD card no longer runs a flash file that has the
    same name.
  - Sending a file to a `flsh:` path (for example OneWili `files.put`) no
    longer hangs the console.
- **Battery stream** (`h\a\o`) sends an empty record instead of uninitialised
  data on FREE-WILi2.
- **10BASE-T1S**: transmit/receive buffers moved to PSRAM, so re-initialising
  T1S no longer runs out of memory. The header SPI path is restored when the
  FPGA leaves it tri-stated after a register-transport window. This fixes
  periodic ~100 ms link drops when the Linux CPU is powered.

## New since v09

- **Per-port USB-A host power**: **Hardware > Power Management > Set USB
  Host Port Power** (`h\p\u <port> <on>`) and **Get USB Host Port Power**
  (`h\p\p`). Each of the three USB-A host ports can be switched on or off.
  The commanded state survives a sensor-rail power cycle. A Display reboot
  turns all three ports back on. The reading is the commanded state; VBUS is
  not measured.
- **10BASE-T1L** (ADIN1110, with the San Diego Orca IO board): the **i\t**
  menu with link, SQI, test generator and counters. The T1L port has its own
  network interface (IP and netmask under **i\w**), so ping, UDP and the
  network services run over T1L as they do over T1S. A USB-network to T1L
  bridge is available, along with Ethernet Test port selection (USB, T1S or
  T1L). A **10BaseT1L** status panel runs on the display.
- **SAE J1708** transmit and receive on the Orca's RS-485 port (**i\v**),
  with priority arbitration, periodic messages, and a **Bias 5V Pin 13**
  setting that supplies the bus bias from DB15 pin 13.
- **Modbus RTU** master, slave and monitor on the Orca's RS-485 port
  (**i\x**): 1200-115200 baud, parity, and stop bits. The **Modbus TCP**
  setting adds a server/gateway on TCP port 502, reachable over USB
  networking, T1S and T1L.
- **OneWili**:
  - Every on/off setting accepts an explicit value (`<key> 1` / `<key> 0`,
    also on/off and true/false) as well as the bare toggle.
  - The Python bindings add `set_<name>(on)` / `get_<name>()` and a public
    events API (`dev.next_event()`, `dev.listen()`, `dev.clear_events()`).
  - New generated Python examples: `modbus_read.py`, `waveshare_io8.py`
    (Waveshare Modbus RTU IO 8CH) and `j1708_monitor.py`.
  - Command IDs 0-634 are unchanged. New commands were appended as 635-689;
    Set/Get USB Host Port Power are 688/689.
- **rTHON example `halloween_usb.rtn`**: a USB-A port light show built on
  the new port power commands, with its own panel and button controls.
- **wifiCPU v10**: built-in capture mode for FreeWili GUI's **Protocol >
  Wi-Fi & BT** view. It captures BLE advertisements, or Wi-Fi management
  frames on a selected 2.4 or 5 GHz channel, over the ESP32-C5's USB port.
  It ships in the normal wifiCPU update, with no separate install.

Firmware source revision: `5d14ee4084d5f860373d1ff4ae84b1886d90a364`
(branch `release/v10`: `main` at `ef0c15c4` plus the v10 version bump). The
Display ROM asset pack is byte-identical to v09.

## Install

In a current FreeWili GUI, open **Setup > Firmware Updater**, choose
**GitHub release > Stable**, and press **Refresh**. Confirm
**v10 - Stable firmware release**, then **Update and verify**. Keep USB
power connected until completion. Install all three components for the
matching firmware set. The updater installs Main first.

wifiCPU installation requires an RP SD card owned by Main. The updater
checks the merged ESP32-C5 image and writes only its bootloader, partition
table, application, and storage regions. It preserves NVS and PHY settings.

After updating from v09 or earlier, Main's settings are read from internal
flash. Settings that earlier firmware kept on the SD card are picked up from
`1:/settings` until each one is saved again.

## Validation

Release builds, embedded versions (`FW2 v10`, `FW2Display v10`, wifiCPU
`v10`), the Display asset pack, complete Display UF2 packaging (Display and
absolute asset families preserved), and the ESP32-C5 image checks were run
before packaging. The four regions in the merged image are identical to the
build's split files. The ZIP manifest contains sizes and SHA-256 hashes for
every component.

The exact packaged images were installed on FREE-WILi2 hardware:

- **Main** through its fused recovery loader, the same path the updater
  uses. The application flash was read back over SWD and matched the UF2
  byte for byte. Main reported `FW2 v10`. Its flash interface was confirmed
  in quad mode, and an rTHON benchmark ran 10,000 loop iterations in 253 ms,
  with `device_state()` at 0.66 ms per call. A setting changed before a Main
  reset was still there after it.
- **Display**, the complete image with assets, was programmed over the
  on-board debug probe and passed full flash read-back verification. The
  display rail was on and Main's display link answered.
- **wifiCPU** through Main's verified update command, from this package's
  merged image split into its four regions. All four regions passed MD5
  verification and the restart completed. The ESP32-C5 then answered Main
  and enumerated on USB.

## Known limitations

10BASE-T1L, J1708 and Modbus RTU require the San Diego Orca IO board on the
20-pin header. USB-A port power reports the commanded state, not measured
VBUS. Main installation and the Display debug-probe fallback currently
require Windows. Only the standard onboard ESP32-C5 factory partition layout
is supported. No separate debug-probe, PIC, LoRa module, or Linux OS images
are included.
