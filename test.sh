#!/bin/bash
set -euo pipefail

# Run from the project directory even when invoked from another directory.
cd "$(dirname "$0")"

# Keep drafts on the same filesystem as static/ for hard_link_static builds.
# The trap also removes temporary output when a later check fails.
draft_directory="$(mktemp -d "$PWD/.zola-drafts.XXXXXX")"
draft_output="$draft_directory/public"
trap 'rm -rf "$draft_directory"' EXIT

echo "=== 1/5 Building production site ==="
zola build
echo "  ✓"

echo "=== 2/5 Building drafts separately ==="
zola build --drafts --output-dir "$draft_output"
echo "  ✓"

echo "=== 3/5 Verifying production and draft pages ==="
for page in about research teaching; do
    [ -f "public/$page/index.html" ] || { echo "  ✗ Missing: $page"; exit 1; }
done
for lang in cn ja; do
    [ -f "public/$lang/about/index.html" ] || { echo "  ✗ Missing: $lang/about"; exit 1; }
done
[ ! -e "public/test" ] || { echo "  ✗ Draft test page found in production output"; exit 1; }
[ -f "$draft_output/test/index.html" ] || { echo "  ✗ Missing draft test page"; exit 1; }
echo "  ✓"

# Discover every suite so newly merged navigation/theme tests also run in CI.
echo "=== 4/5 Checking regressions ==="
python3 -B -m unittest discover --start-directory tests --pattern 'test_*.py' --verbose
echo "  ✓"

echo "=== 5/5 Checking internal and external links ==="
zola check
echo "  ✓"

echo "=== All tests passed ==="
