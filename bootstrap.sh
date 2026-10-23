#!/usr/bin/env bash
# Clones the fork into portfolio/ and adds the upstream remote.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
FORK_URL="${FORK_URL:-git@github.com:ulrichlehner/portfolio.git}"
UPSTREAM_URL="https://github.com/portfolio-performance/portfolio.git"

if [ ! -d "$ROOT/portfolio/.git" ]; then
    git clone "$FORK_URL" "$ROOT/portfolio"
fi

cd "$ROOT/portfolio"
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "$UPSTREAM_URL"
git fetch upstream
git remote -v
