#!/usr/bin/env python3
"""Private local testing support. Executed only in the development container."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


class DevError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def git(pp, *args):
    return subprocess.check_output(['git', '-C', str(pp), *args])


def source_state(pp):
    digest = hashlib.sha256()
    paths = git(pp, 'ls-files', '-z', '--cached', '--others', '--exclude-standard')
    for name in sorted(set(paths.split(b'\0')) - {b''}):
        path = pp / os.fsdecode(name)
        digest.update(name + b'\0')
        if path.is_symlink():
            digest.update(b'link\0' + os.fsencode(os.readlink(path)))
        elif path.is_file():
            digest.update(str(stat.S_IMODE(path.stat().st_mode)).encode() + b'\0')
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
        else:
            digest.update(b'deleted')
        digest.update(b'\0')
    return {'revision': git(pp, 'rev-parse', 'HEAD').decode().strip(),
            'dirty': bool(git(pp, 'status', '--porcelain', '--untracked-files=all')),
            'fingerprint': digest.hexdigest()}


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.manifest-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def app_path(pp, arch):
    if arch not in ('aarch64', 'x86_64'):
        raise DevError('Unsupported macOS architecture.')
    return pp / ('portfolio-product/target/products/'
                 'name.abuchen.portfolio.distro.product/macosx/cocoa') / arch / 'PortfolioPerformance.app'


def macho_arch(path):
    with path.open('rb') as stream:
        header = stream.read(8)
    if len(header) != 8 or header[:4] not in (b'\xcf\xfa\xed\xfe', b'\xfe\xed\xfa\xcf'):
        raise DevError('Packaged executable is not a supported Mach-O binary.')
    order = '<' if header[:4] == b'\xcf\xfa\xed\xfe' else '>'
    return {0x100000C: 'aarch64', 0x1000007: 'x86_64'}.get(struct.unpack(order + 'I', header[4:])[0])


def artifact_state(pp, arch):
    app = app_path(pp, arch)
    launcher = app / 'Contents/MacOS/PortfolioPerformance'
    runtimes = list(app.glob('**/bin/java'))
    if not launcher.is_file() or not os.access(launcher, os.X_OK) or len(runtimes) != 1:
        raise DevError('Missing app or bundled Java runtime; run scripts/dev.sh app.')
    for executable in [launcher, runtimes[0]]:
        if not os.access(executable, os.X_OK) or macho_arch(executable) != arch:
            raise DevError('Packaged launcher/runtime architecture mismatch; rebuild the app.')
    digest = hashlib.sha256()
    for path in sorted(app.rglob('*')):
        digest.update(os.fsencode(str(path.relative_to(app))) + b'\0')
        if path.is_symlink():
            digest.update(b'link\0' + os.fsencode(os.readlink(path)))
        elif path.is_file():
            digest.update(str(stat.S_IMODE(path.stat().st_mode)).encode() + b'\0')
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
        digest.update(b'\0')
    return digest.hexdigest()


def build_command(args):
    if args.action == 'before':
        # Invalidate a previous successful build before Maven can replace it.
        atomic_json(args.manifest, {'schema': 1, 'pending': source_state(args.pp)})
    elif args.action == 'after':
        previous = json.loads(args.manifest.read_text())
        current = source_state(args.pp)
        if previous.get('pending') != current:
            raise DevError('Sources changed during build; rebuild the app.')
        atomic_json(args.manifest, {'schema': 1, 'source': current, 'architecture': args.arch,
                                   'artifact': artifact_state(args.pp, args.arch), 'built_at': now()})
    else:
        try:
            manifest = json.loads(args.manifest.read_text())
        except (OSError, ValueError):
            raise DevError('Build manifest missing or invalid; run scripts/dev.sh app.') from None
        if (manifest.get('schema') != 1 or manifest.get('architecture') != args.arch
                or manifest.get('source') != source_state(args.pp)):
            raise DevError('Build is stale or incompatible; run scripts/dev.sh app.')
        if manifest.get('artifact') != artifact_state(args.pp, args.arch):
            raise DevError('Built app differs from its manifest; run scripts/dev.sh app.')
        source = manifest['source']
        print('Build: ' + source['revision'][:12] + (' dirty' if source['dirty'] else ' clean')
              + ' source=' + source['fingerprint'][:16] + ' arch=' + args.arch)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build')
    build.add_argument('action', choices=['before', 'after', 'check'])
    build.add_argument('--pp', type=Path, required=True)
    build.add_argument('--manifest', type=Path, required=True)
    build.add_argument('--arch', required=True)
    args = parser.parse_args()
    try:
        build_command(args)
    except DevError as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 1
    except Exception:
        # Paths, remote identifiers and exception bodies can contain private data.
        print('ERROR: Local testing operation failed; check private setup and rebuild if needed.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
