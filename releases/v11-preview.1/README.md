# v11-preview.1 - FPGA designs, ZoomIO FIFOs and Power Cycle Reboot

Preview build of Main and Display with embedded version v11, from one source
revision. It adds support for your own FPGA designs, a FIFO-based ZoomIO
engine, and a Power Cycle Reboot command. wifiCPU is the unchanged v10
image.

| Component | Embedded version |
| --- | --- |
| Main | v11 |
| Display | v11 |
| wifiCPU (ESP32-C5) | v10 (unchanged) |

## New since v10

- **Your own FPGA designs.** A new **Hardware > FPGA** menu (`h\f`) loads
  designs built with the open-source FreeWili 2 FPGA board support package
  ([freewili/wilifpga](https://github.com/freewili/wilifpga)). A design is a
  `.fwfpga` file that carries the bitstream and the direction of every header
  pin. Main sets all pin directions from the file before the FPGA is
  programmed, and enables the design only after its ID block matches.
  - Load Design (`h\f\l`), Restore Stock (`h\f\t`) and Status (`h\f\s`).
  - Register read and write (`h\f\r`, `h\f\w`).
  - Data paths: stream read (`h\f\x`) and capture to a file (`h\f\c`)
    through the stream FIFO, PIO link capture (`h\f\p`, about 15.6 MB/s
    bursts), and the RP2350-clocked link stream (`h\f\k`, about 5 MB/s,
    lossless, in either direction).
  - Each design sets its own FPGA clock. **Settings > FPGA Clock** now shows
    the clock in use and is read-only.
  - The Files app loads a `.fwfpga` file directly, and the **Default FPGA**
    setting (`h\s\e\c`) boots one.
- **ZoomIO** runs on new transmit and receive FIFOs:
  - Load, Run and Stop a `.zio` program (`s\b\l` and the ZoomIO menu).
    Programs can use the input FIFO, packet waits and nanosecond timing.
  - A message queue for scripts (`s\b\e`, `s\b\m`) and a ZoomIO messages
    panel on the display.
  - Binary `zoomioReport` frames on the FTDI stream, and chunked `zoomio`
    console events (64 data bytes each, with length and offset for
    reassembly). Status bits report Overflow and Oversize.
  - The CAN API's ZoomIO commands use the new FIFOs and accept multi-frame
    writes.
- **Power Cycle Reboot** (`h\p\r [seconds]`, 1-30 s, default 2) switches off
  every rail Main and Display can reach, including the USB-A host ports,
  then brings them back. Use it to recover a board without removing the
  battery.
- **Function blocks**: set the execution step, run to a step, force values,
  and resume after an error halt.
- **OneWili**: command IDs 0-689 are unchanged. New commands were appended as
  690-702: Power Cycle Reboot is 690, the ZoomIO script commands are
  691-693, and the FPGA commands are 694-702. The C, Python, Rust, WASM and
  rTHON bindings include them.

## Changes and fixes since v10

- **Default FPGA accepts only `.fwfpga` files.** A raw bitstream named in
  the Default FPGA setting (`h\s\e\c`) is refused at boot, and the stock
  image stays loaded. Rebuild the design as a `.fwfpga` with the FPGA board
  support package.
- Ethernet Test no longer uses a 500 us timer interrupt; its work runs from
  the main loop, with time-based pacing for Line Rate and Burst.

Firmware source revision: `b254d67cd7c7b45b95c099987d181b4ff14db02d`
(branch `release/v11-preview.1`: `main` at `a2178d8c` plus the v11 version
bump). The Display ROM asset pack is byte-identical to v10.

## Install

In a current FreeWili GUI, open **Setup > Firmware Updater**, choose
**GitHub release > Preview**, and press **Refresh**. Confirm
**v11-preview.1 - FPGA designs, ZoomIO FIFOs and Power Cycle Reboot**, then
**Update and verify**. Keep USB power connected until completion. The
updater installs Main first. wifiCPU is the same image as v10, so a board
already on v10 does not need it again.

## Validation

Release builds, embedded versions (`FW2 v11`, `FW2Display v11`), the Display
asset pack check, and complete Display UF2 packaging (Display and absolute
asset families preserved) were run before packaging. The wifiCPU files are
byte-identical to v10. The ZIP manifest contains sizes and SHA-256 hashes
for every component.

The exact packaged images were installed on FREE-WILi2 hardware:

- **Main** through its fused recovery loader, the same path the updater
  uses. Main reported `FW2 v11`.
- **Display**, the complete image with assets, was programmed over the
  on-board debug probe (code and asset pack) and passed flash read-back
  verification. It ran the v11 interface and showed live battery data from
  Main.
- **FPGA**, with designs built from wilifpga v0.1.0 and a board whose IO
  direction settings differ from the defaults: `hello_blink` loaded, its ID
  block matched and register write/read-back worked. The stream FIFO
  (`logic_capture`) captured 4 KB. The FPGA-clocked PIO link (`pio_link`)
  captured 1 MB at 15.6 MB/s with the counter pattern intact in every burst.
  The RP2350-clocked link captured 4 MB continuously (`pio_stream`) and sent
  4 MB to the FPGA (`pio_sink`) with no pattern errors at PIO divider 2,
  and 8 MB each way at divider 1 (4.76 MB/s from the FPGA, 5.36 MB/s to
  it). Every load reported clean contention self-checks, and Restore Stock
  returned to the stock image.
- wifiCPU was not reinstalled; it is the v10 image.

## Known limitations

FPGA designs need power zone 6 on (`h\p\s 6 1`). In one of about ten link
transfers on the test bench, the status read after the transfer reported a
contention finding on a pin that the loaded design does not check. It did
not recur, and the transfer itself was error-free. Header GPIO26 and GPIO27
go high for up to about 250 ms while a design loads. Main has little free
RAM in this build (about 2.6 KiB). Main installation and the Display
debug-probe fallback currently require Windows. Only the standard onboard
ESP32-C5 factory partition layout is supported. No separate debug-probe,
PIC, LoRa module, or Linux OS images are included.
