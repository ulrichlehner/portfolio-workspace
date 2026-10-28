#!/usr/bin/env python3
"""Extract Portfolio Performance's OAuth client registration for local builds.

The registration is deliberately not part of the public repository. The official
build embeds it and verifies its SHA-256 checksum while signing, so only signed
release artifacts carry it. A self-built application therefore cannot use the
built-in quote feed unless it is given a copy.

This tool reads the registration from an installed official PP application,
verifies it against the checksum pinned in the core pom.xml and writes it outside
the source tree. The launcher passes only the path of that file to the
application; the contents are never printed, committed or added to a build.

This is a local development convenience. It does not grant any right to the
registration or to the data service; see docs/local-testing.md.
"""
import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ENTRY = 'name/abuchen/portfolio/oauth/impl/config.json'
SOURCE_ENTRY = 'name.abuchen.portfolio/src/' + ENTRY


def expected_sha256(pom):
    match = re.search(r'arg2="([0-9a-f]{64})"', pom.read_text(encoding='utf-8'))
    if not match:
        raise ValueError('OAuth checksum not found in pom.xml')
    return match.group(1)


def install(jar, destination, expected):
    """Extract and verify one registration. Return True when it changed."""
    with zipfile.ZipFile(jar) as archive:
        data = archive.read(ENTRY)
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected:
        raise ValueError('OAuth registration checksum mismatch; refusing to install')
    if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() == digest:
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    destination.chmod(0o600)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path, help='Explicit official PP core jar')
    parser.add_argument('--app', type=Path, default=Path('/Applications/PortfolioPerformance.app'))
    parser.add_argument('--pp', type=Path, required=True, help='PP source checkout')
    parser.add_argument('--destination', type=Path, required=True,
                        help='Private file outside the source tree')
    args = parser.parse_args()

    expected = expected_sha256(args.pp / 'name.abuchen.portfolio/pom.xml')
    jars = [args.jar] if args.jar else sorted((args.app / 'Contents/Eclipse/plugins').glob(
        'name.abuchen.portfolio_*.jar'))

    if not jars:
        print('No official PP application found; the built-in quote feed stays unconfigured.',
              file=sys.stderr)
        return 1

    changed = install(jars[0], args.destination, expected)
    print('OAuth registration installed outside the source tree.'
          if changed else 'OAuth registration already up to date.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, KeyError, ValueError, zipfile.BadZipFile) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
