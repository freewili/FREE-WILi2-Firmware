# v07 - Day Zero DEFCON release

The initial complete FREE-WILi2 firmware bundle. These are the existing
Day Zero firmware images, packaged together without modifying their bytes.

| Component | Embedded version | File |
| --- | --- | --- |
| Main | v07 | `firmware/FW2Main-v07.uf2` |
| Display | v07 | `firmware/FW2Display-v07.uf2` |
| Bottlenose (ESP32-C5) | spartahackFw1final-1743-g349128 | `bottlenose/bottlenose-spartahackFw1final-1743-g349128-merged.bin` |

The Display UF2 includes its asset partition. Bottlenose is a merged image
for flash offset `0x0`, including the bootloader, partition table,
application, and storage partition. Its application was built August 7,
2026 with ESP-IDF v6.0.1.

`manifest.json` records every component's filename, embedded version, byte
size, and SHA-256. `bottlenose/flasher_args.json` retains the original build's
flashing metadata. Its split-image paths describe the source build; those
individual files are already combined into the merged binary.

Use FreeWili GUI's Firmware Updater to choose **Stable** and update Main and
Display from this bundle. Bottlenose is included for separate installation;
it is not installed by the Main/Display updater. Local UF2 selection remains
available for individual firmware images.

This is the baseline for future release notes. No additional firmware fixes
or hardware compatibility changes are claimed by this packaging release.
