#!/bin/bash
set -e

echo "=== 1/4 Building production site ==="
zola build
echo "  ✓"

echo "=== 2/4 Building with drafts ==="
zola build --drafts
echo "  ✓"

echo "=== 3/4 Checking internal links ==="
zola check
echo "  ✓"

echo "=== 4/4 Verifying key pages ==="
for page in about research teaching; do
    [ -f "public/$page/index.html" ] || { echo "  ✗ Missing: $page"; exit 1; }
done
for lang in cn ja; do
    [ -f "public/$lang/about/index.html" ] || { echo "  ✗ Missing: $lang/about"; exit 1; }
done
echo "  ✓"

echo "=== All tests passed ==="
