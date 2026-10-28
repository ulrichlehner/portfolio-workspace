#!/usr/bin/env python3
"""Install the OAuth client configuration for local PP builds.

The official release embeds an OAuth client registration that is deliberately not
committed to the repository, so a self-built app cannot use the built-in quote
feed. This tool copies that registration from an installed official PP
application, verifies its SHA-256 against the checksum pinned in the core
pom.xml, and writes it to the gitignored source path. Only paths and status are
printed, never the configuration contents.
"""
import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ENTRY = 'name/abuchen/portfolio/oauth/impl/config.json'


def expected_sha256(pom):
    match = re.search(r'arg2="([0-9a-f]{64})"', pom.read_text(encoding='utf-8'))
    if not match:
        raise ValueError('OAuth checksum not found in pom.xml')
    return match.group(1)


def install(jar, destination, expected):
    """Extract and verify one config file. Return True when it changed."""
    with zipfile.ZipFile(jar) as archive:
        data = archive.read(ENTRY)
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected:
        raise ValueError('OAuth configuration checksum mismatch; refusing to install')
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
    args = parser.parse_args()

    expected = expected_sha256(args.pp / 'name.abuchen.portfolio/pom.xml')
    jars = [args.jar] if args.jar else sorted((args.app / 'Contents/Eclipse/plugins').glob(
        'name.abuchen.portfolio_*.jar'))
    destination = args.pp / 'name.abuchen.portfolio/src' / ENTRY

    if not jars:
        # A build without the configuration still works, only the built-in feed
        # stays unconfigured. Do not fail the build for that.
        print('No official PP application found; built-in quote feed stays unconfigured.')
        return 0

    changed = install(jars[0], destination, expected)
    print('OAuth configuration installed from official PP application.'
          if changed else 'OAuth configuration already up to date.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, KeyError, ValueError, zipfile.BadZipFile) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
