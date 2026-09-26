#!/usr/bin/env python3
"""Validate and package one complete, versioned FREE-WILi2 release folder."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile


def uf2_version(data, component):
    if not data or len(data) % 512:
        raise ValueError("Incomplete UF2")
    blocks = {}
    for start in range(0, len(data), 512):
        block = data[start:start + 512]
        magic1, magic2, flags, address, size, index, count, family = struct.unpack_from('<8I', block)
        if (magic1, magic2, struct.unpack_from('<I', block, 508)[0]) != (0x0a324655, 0x9e5d5157, 0x0ab16f30) or size != 256:
            raise ValueError("Invalid UF2 block")
        expected = 0xe48bff59 if component == 'main' else 0x46574432
        if family == expected and address < 0x10800000:
            blocks[address] = block[32:32 + size]
    payload = b''.join(blocks[address] for address in sorted(blocks))
    prefix = b'FW2 v' if component == 'main' else b'FW2Display v'
    versions = set(re.findall(re.escape(prefix) + rb'([0-9]+(?:\.[0-9]+)*)\x00', payload))
    if len(versions) != 1:
        raise ValueError(f"Cannot identify {component} firmware version")
    return 'v' + versions.pop().decode('ascii')


def bottlenose_version(data):
    # ESP-IDF esp_app_desc_t immediately follows the app image header/segment.
    start = 0x10020
    if data[start:start + 4] != struct.pack('<I', 0xabcd5432):
        raise ValueError('Missing Bottlenose ESP-IDF app descriptor')
    if data[start + 48:start + 80].split(b'\0')[0] != b'bottlenose':
        raise ValueError('Wrong Bottlenose project identity')
    return data[start + 16:start + 48].split(b'\0')[0].decode('ascii')


def validate(folder):
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    version = manifest['release']
    if not re.fullmatch(r'v[0-9][A-Za-z0-9.-]*', version) or version != folder.name:
        raise ValueError('Release name must match its folder and start with v + a number')
    if manifest['schema'] != 1 or manifest['product'] != 'FREE-WILi2':
        raise ValueError('Unsupported manifest')
    files = {}
    components = set()
    for entry in manifest['files']:
        name, component = entry['file'], entry['component']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', name) or '..' in name:
            raise ValueError('Unsafe package path')
        if name in files or component in components:
            raise ValueError('Duplicate package component or path')
        data = (folder / name).read_bytes()
        if len(data) != entry['size'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError(f'Checksum/size mismatch: {name}')
        component_version = entry['version']
        if component in ('main', 'display'):
            if uf2_version(data, component) != component_version or not name.endswith(f'-{component_version}.uf2'):
                raise ValueError(f'UF2 filename/version mismatch: {name}')
        elif component == 'bottlenose':
            if bottlenose_version(data) != component_version or not name.endswith(f'-{component_version}-merged.bin'):
                raise ValueError('Bottlenose filename/version mismatch')
        elif component == 'bottlenose-flasher-args':
            if json.loads(data)['extra_esptool_args']['chip'] != 'esp32c5':
                raise ValueError('Wrong Bottlenose chip')
        files[name] = data
        components.add(component)
    if components != {'main', 'display', 'bottlenose', 'bottlenose-flasher-args'}:
        raise ValueError('Release needs Main, Display, Bottlenose, and its original flasher arguments')
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    if actual != set(files) | {'manifest.json', 'README.md'}:
        raise ValueError('Unlisted or missing release files')
    files['manifest.json'] = (folder / 'manifest.json').read_bytes()
    files['README.md'] = (folder / 'README.md').read_bytes()
    if not files['README.md'] or len(files['README.md']) > 65536:
        raise ValueError('Release README must contain notes and be at most 64 KiB')
    return manifest, files


def package(folder, output):
    manifest, files = validate(folder)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"FREE-WILi2-{manifest['release']}.zip"
    # Fixed metadata makes independent builds byte-for-byte reproducible.
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{checksum}  {archive.name}\n', encoding='ascii')
    print(f'{archive}: {archive.stat().st_size} bytes, SHA-256 {checksum}')
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('release', help='Release folder, for example releases/v07')
    parser.add_argument('--output', default='dist')
    args = parser.parse_args()
    package(Path(args.release), Path(args.output))
