#!/usr/bin/env python3
"""Regenerate release SHA-256 manifests for repository source and evidence."""
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    '.git', '.pytest_cache', '.venv', 'node_modules', '.gltest-artifacts',
    '__pycache__', 'coverage',
}
EXCLUDED_FILES = {'checksums.sha256', 'SOURCE_SHA256_MANIFEST.json'}


def files():
    for directory, names, filenames in os.walk(ROOT, topdown=True):
        names[:] = sorted(name for name in names if name not in EXCLUDED_DIRS)
        base = Path(directory)
        for filename in sorted(filenames):
            path = base / filename
            relative = path.relative_to(ROOT)
            if relative.name in EXCLUDED_FILES or (
                relative.name.startswith('.env.') and relative.name != '.env.example'
            ):
                continue
            yield relative.as_posix(), path.read_bytes()


entries = {name: hashlib.sha256(data).hexdigest() for name, data in files()}
manifest = {'algorithm': 'sha256', 'files': entries}
(ROOT / 'SOURCE_SHA256_MANIFEST.json').write_text(
    json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n'
)
(ROOT / 'checksums.sha256').write_text(
    ''.join(f'{value}  {name}\n' for name, value in sorted(entries.items())),
    encoding='utf-8', newline='\n'
)
print(f'Updated {len(entries)} file hashes')
