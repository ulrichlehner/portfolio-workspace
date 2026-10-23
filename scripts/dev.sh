#!/usr/bin/env bash
# Runs Portfolio Performance builds and tests in Docker. Nothing is installed on the host.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PP="${PORTFOLIO_DIR:-$ROOT/portfolio}"
SCRATCH="$ROOT/scratch"
IMAGE=portfolio-dev
VOLUME=portfolio-m2
CORE=":portfolio-target-definition,:name.abuchen.portfolio.pdfbox1,:name.abuchen.portfolio.pdfbox3,:name.abuchen.portfolio,:name.abuchen.portfolio.junit,:name.abuchen.portfolio.tests"
APP="$PP/portfolio-product/target/products/name.abuchen.portfolio.distro.product/macosx/cocoa/aarch64/PortfolioPerformance.app"

usage() {
    cat <<EOF
Usage: scripts/dev.sh <command>

  test [TestClass]   core tests and Checkstyle, optionally only one test class
  app                build the macOS app with bundled Java (for manual tests)
  run-app            start that app with its own workspace in scratch/
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

case "${1:-}" in
    test)
        if [ -n "${2:-}" ]; then
            mvn_in_docker clean verify -Plocal-dev -Dcheckstyle.skip=false -pl "$CORE" -am -amd "-Dtest=$2"
        else
            mvn_in_docker clean verify -Plocal-dev -Dcheckstyle.skip=false -pl "$CORE" -am -amd
        fi
        ;;
    app)
        mvn_in_docker clean verify -DskipTests -Pdefault,package-distro
        echo "App: $APP"
        ;;
    run-app)
        [ -d "$APP" ] || { echo "No app built yet, run scripts/dev.sh app first" >&2; exit 1; }
        mkdir -p "$SCRATCH/pp-dev-workspace"
        open -n "$APP" --args -data "$SCRATCH/pp-dev-workspace"
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
        require_fork
        find "$PP" -mindepth 2 -maxdepth 3 -type d -name target -prune -exec rm -rf {} +
        rm -rf "$SCRATCH/pp-dev-workspace"
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
