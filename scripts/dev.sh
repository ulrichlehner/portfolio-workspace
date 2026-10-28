#!/usr/bin/env bash
# Runs Portfolio Performance builds and tests in Docker. Nothing is installed on the host.
set -euo pipefail
umask 077

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PP="${PORTFOLIO_DIR:-$ROOT/portfolio}"
SCRATCH="$ROOT/scratch"
IMAGE=portfolio-dev
VOLUME=portfolio-m2
CORE=":portfolio-target-definition,:name.abuchen.portfolio.pdfbox1,:name.abuchen.portfolio.pdfbox3,:name.abuchen.portfolio,:name.abuchen.portfolio.junit,:name.abuchen.portfolio.tests"
case "$(uname -m)" in
    arm64|aarch64) ARCH=aarch64 ;;
    x86_64) ARCH=x86_64 ;;
    *) ARCH=unsupported ;;
esac
APP="$PP/portfolio-product/target/products/name.abuchen.portfolio.distro.product/macosx/cocoa/$ARCH/PortfolioPerformance.app"

usage() {
    cat <<EOF
Usage: scripts/dev.sh <command>

  test [TestClass]   core tests and Checkstyle, optionally only one test class
  app                build the macOS app with bundled Java (for manual tests)
  run-app            start that app with its own workspace in scratch/
                     --webdav-copy refresh and open a private WebDAV copy
                     --webdav-copy --offline use retained local data explicitly
  keep-data          keep the current generation across later refreshes
  recover-data       select the previous generation for an offline launch
  clean-data         explicitly delete managed private portfolios and backups
  test-tools         synthetic workspace tooling tests in Docker
  oauth-config       install the OAuth client config from an official PP app
  pdftext FILE.pdf   print the text of a PDF as PP converts it (PDFBox 3)
  shell              interactive shell in the container
  clean              delete the build output in portfolio/
  purge              clean, then remove the Docker image and volume
EOF
}

require_fork() {
    [ -d "$PP/portfolio-app" ] || { echo "Fork not found at $PP, run ./bootstrap.sh first" >&2; exit 1; }
}

image() {
    docker image inspect "$IMAGE" >/dev/null 2>&1 || docker build -t "$IMAGE" "$ROOT/.devcontainer"
}

mvn_in_docker() {
    require_fork
    image
    docker run --rm -v "$VOLUME":/root/.m2 -v "$PP":/src -w /src "$IMAGE" mvn -B -f portfolio-app/pom.xml "$@"
}

build_metadata() {
    image
    mkdir -p "$SCRATCH/pp-dev-build"
    docker run --rm -v "$PP":/src:ro -v "$ROOT/scripts":/tools:ro \
        -v "$SCRATCH/pp-dev-build":/build "$IMAGE" python3 /tools/pp_dev.py \
        build "$1" --pp /src --manifest /build/manifest.json --arch "$ARCH"
}

safe_scratch() {
    [ ! -L "$SCRATCH" ] || { echo "Unsafe scratch link" >&2; exit 1; }
    mkdir -p "$SCRATCH"
    for name in pp-dev-data pp-dev-build pp-dev-workspace pp-dev-config pp-dev-home pp-dev-secrets pp-dev-provider-state pp-dev.lock; do
        [ ! -L "$SCRATCH/$name" ] || { echo "Unsafe managed storage link" >&2; exit 1; }
    done
}

acquire_lock() {
    safe_scratch
    local links
    if [ -e "$SCRATCH/pp-dev.lock" ]; then
        [ -f "$SCRATCH/pp-dev.lock" ] || { echo "Unsafe launcher lock" >&2; exit 1; }
        if [ "$(uname -s)" = Darwin ]; then
            links="$(stat -f %l "$SCRATCH/pp-dev.lock")"
        else
            links="$(stat -c %h "$SCRATCH/pp-dev.lock")"
        fi
        [ "$links" = 1 ] || { echo "Unsafe launcher lock link" >&2; exit 1; }
    fi
    # Keep the descriptor in this shell and its children, including the native
    # launcher. Kernel locks recover on exit without trusting a stored PID.
    exec 9>>"$SCRATCH/pp-dev.lock"
    if [ "$(uname -s)" = Darwin ]; then
        /usr/bin/lockf -s -t 0 9 || { echo "Development app/build/refresh is already running" >&2; exit 1; }
    else
        flock -n 9 || { echo "Development app/build/refresh is already running" >&2; exit 1; }
    fi
}

private_data() {
    local action="$1"
    local mounts=(--network none)
    safe_scratch
    mkdir -p "$SCRATCH/pp-dev-data" "$SCRATCH/pp-dev-build"
    if [ "$action" = refresh ]; then
        [ -f "$SCRATCH/pp-dev-secrets/webdav.json" ] && [ ! -L "$SCRATCH/pp-dev-secrets/webdav.json" ] \
            || { echo "Private read-only WebDAV setup missing; see docs/local-testing.md" >&2; exit 1; }
        mounts=(-v "$SCRATCH/pp-dev-secrets/webdav.json:/secret/config.json:ro")
    fi
    image
    docker run --rm "${mounts[@]}" -v "$PP":/src:ro -v "$ROOT/scripts":/tools:ro \
        -v "$SCRATCH/pp-dev-build":/build:ro -v "$SCRATCH/pp-dev-data":/data \
        "$IMAGE" python3 /tools/pp_dev_data.py "$action" --data /data --host-data "$SCRATCH/pp-dev-data"
    if [ "$action" = cleanup ]; then
        rmdir "$SCRATCH/pp-dev-data"
        rm -rf "$SCRATCH/pp-dev-provider-state"
    fi
}

# The managed workspace is recreated on each launch. Provider caches and the
# Breakdown's own preferences (lookthrough.*) are carried over, so repeated
# launches do not fetch every composition and company again.
UI_STATE=.metadata/.plugins/name.abuchen.portfolio.ui
UI_PREFS=.metadata/.plugins/org.eclipse.core.runtime/.settings/name.abuchen.portfolio.ui.prefs

save_provider_state() {
    local workspace="$SCRATCH/pp-dev-workspace" state="$SCRATCH/pp-dev-provider-state" name
    [ -d "$workspace" ] || return 0
    mkdir -p "$state" && chmod 700 "$state"
    for name in lookthrough-cache lookthrough-companies; do
        if [ -d "$workspace/$UI_STATE/$name" ] && [ ! -L "$workspace/$UI_STATE/$name" ]; then
            rm -rf "${state:?}/$name"
            mv "$workspace/$UI_STATE/$name" "$state/$name"
        fi
    done
    if [ -f "$workspace/$UI_PREFS" ]; then
        grep '^lookthrough\.' "$workspace/$UI_PREFS" > "$state/prefs" || true
    fi
}

restore_provider_state() {
    local workspace="$SCRATCH/pp-dev-workspace" state="$SCRATCH/pp-dev-provider-state" name
    [ -d "$state" ] || return 0
    mkdir -p "$workspace/$UI_STATE"
    for name in lookthrough-cache lookthrough-companies; do
        [ -d "$state/$name" ] && mv "$state/$name" "$workspace/$UI_STATE/$name"
    done
    if [ -s "$state/prefs" ]; then
        mkdir -p "$(dirname "$workspace/$UI_PREFS")"
        { echo "eclipse.preferences.version=1"; cat "$state/prefs"; } > "$workspace/$UI_PREFS"
    fi
}

case "${1:-}" in
    test)
        acquire_lock
        if [ -n "${2:-}" ]; then
            mvn_in_docker clean verify -Plocal-dev -Dcheckstyle.skip=false -pl "$CORE" -am -amd "-Dtest=$2"
        else
            mvn_in_docker clean verify -Plocal-dev -Dcheckstyle.skip=false -pl "$CORE" -am -amd
        fi
        ;;
    app)
        acquire_lock
        python3 "$ROOT/scripts/pp_oauth_config.py" --pp "$PP"
        build_metadata before
        mvn_in_docker clean verify -DskipTests -Pdefault,package-distro
        build_metadata after
        echo "App: $APP"
        ;;
    run-app)
        [ "$(uname -s)" = Darwin ] || { echo "run-app requires macOS" >&2; exit 1; }
        acquire_lock
        build_metadata check
        launch_args=(-clearPersistedState)
        case "${2:-}" in
            "") [ "$#" = 1 ] || { usage; exit 1; } ;;
            --webdav-copy)
                if [ "$#" = 2 ]; then
                    private_data refresh
                elif [ "$#" = 3 ] && [ "$3" = --offline ]; then
                    private_data offline
                else
                    usage; exit 1
                fi
                launch_args=(-applicationXMI "$(cat "$SCRATCH/pp-dev-data/startup-uri")" -clearPersistedState)
                # No recent-file history from any earlier manual session.
                save_provider_state
                rm -rf "$SCRATCH/pp-dev-workspace"
                ;;
            *) usage; exit 1 ;;
        esac
        mkdir -p "$SCRATCH/pp-dev-workspace"
        restore_provider_state
        rm -rf "$SCRATCH/pp-dev-config"
        cp -R "$APP/Contents/Eclipse/configuration" "$SCRATCH/pp-dev-config"
        if [ "${2:-}" = --webdav-copy ]; then
            cat "$SCRATCH/pp-dev-data/startup-bundle" >> "$SCRATCH/pp-dev-config/org.eclipse.equinox.simpleconfigurator/bundles.info"
        fi
        mkdir -p "$SCRATCH/pp-dev-home"
        # Development convenience: hand the app the path of the private key file,
        # never the key itself. The app installs it as a session key only when no
        # key is configured, and a link is refused.
        dev_key_args=()
        dev_key="$SCRATCH/eulerpool-api-key.txt"
        if [ -f "$dev_key" ] && [ ! -L "$dev_key" ]; then
            dev_key_args=("-Dportfolio.lookthrough.developmentKeyFile=$dev_key")
        fi
        echo "Starting isolated development app; quit it to release the launcher lock."
        # Direct execution targets this build and keeps descriptor 9 alive.
        # WebDAV secrets were mounted only in the finished downloader container.
        exec "$APP/Contents/MacOS/PortfolioPerformance" -data "$SCRATCH/pp-dev-workspace" \
            -configuration "$SCRATCH/pp-dev-config" "${launch_args[@]}" \
            --launcher.appendVmargs -vmargs "-Duser.home=$SCRATCH/pp-dev-home" "${dev_key_args[@]}" \
            "-Declipse.p2.data.area=$SCRATCH/pp-dev-config/p2" \
            >"$SCRATCH/pp-dev-workspace/launcher.log" 2>&1
        ;;
    keep-data|recover-data|clean-data)
        acquire_lock
        case "$1" in
            keep-data) private_data keep ;;
            recover-data) private_data recover ;;
            clean-data) private_data cleanup ;;
        esac
        ;;
    oauth-config)
        python3 "$ROOT/scripts/pp_oauth_config.py" --pp "$PP"
        ;;
    test-tools)
        image
        docker run --rm --network none -v "$ROOT/scripts":/tools:ro -w /tools \
            "$IMAGE" python3 -m unittest discover -s tests -v
        ;;
    pdftext)
        pdf="${2:?Usage: scripts/dev.sh pdftext FILE.pdf}"
        require_fork
        image
        # use the PDFBox 3 version of the fork's target platform
        version="$(grep -A1 '<artifactId>pdfbox</artifactId>' "$PP/portfolio-target-definition/portfolio-target-definition.target" \
            | grep -o '3\.[0-9][0-9.]*' | head -1)"
        dir="$(cd "$(dirname "$pdf")" && pwd)"
        docker run --rm -v "$VOLUME":/root/.m2 -v "$ROOT/scripts":/tools:ro -v "$dir":/pdf:ro "$IMAGE" bash -c "
            mvn -q dependency:get -Dartifact=org.apache.pdfbox:pdfbox:$version >/dev/null
            R=/root/.m2/repository
            CP=\$R/org/apache/pdfbox/pdfbox/$version/pdfbox-$version.jar
            CP=\$CP:\$R/org/apache/pdfbox/pdfbox-io/$version/pdfbox-io-$version.jar
            CP=\$CP:\$R/org/apache/pdfbox/fontbox/$version/fontbox-$version.jar
            CP=\$CP:\$(ls \$R/commons-logging/commons-logging/*/commons-logging-*.jar | head -1)
            java -cp \$CP /tools/PdfToText.java '/pdf/$(basename "$pdf")'"
        ;;
    shell)
        require_fork
        image
        docker run --rm -it -v "$VOLUME":/root/.m2 -v "$ROOT":/workspace -w /workspace/portfolio "$IMAGE" bash
        ;;
    clean)
        acquire_lock
        require_fork
        find "$PP" -mindepth 2 -maxdepth 3 -type d -name target -prune -exec rm -rf {} +
        # Provider caches survive an ordinary clean; clean-data removes them.
        save_provider_state
        rm -rf "$SCRATCH/pp-dev-workspace"
        rm -rf "$SCRATCH/pp-dev-config"
        rm -rf "$SCRATCH/pp-dev-home"
        ;;
    purge)
        "$0" clean
        docker volume rm "$VOLUME" 2>/dev/null || true
        docker image rm "$IMAGE" 2>/dev/null || true
        ;;
    *)
        usage
        ;;
esac
