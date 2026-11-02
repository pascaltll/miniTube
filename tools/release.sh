#!/usr/bin/env bash
# Uso: tools/release.sh 0.51.0 → comprueba versión, hace commit de etiqueta y la sube (dispara la release en GitHub)
set -e
cd "$(dirname "$0")/.."
V="$1"; [ -n "$V" ] || { echo "uso: $0 <version>"; exit 1; }
grep -q "__version__ = \"$V\"" ytmini/__init__.py || { echo "ytmini/__init__.py no tiene la versión $V"; exit 1; }
grep -q "^## $V" CHANGELOG.md || { echo "CHANGELOG.md no tiene sección '## $V'"; exit 1; }
git tag "v$V" && git push origin HEAD "v$V"
