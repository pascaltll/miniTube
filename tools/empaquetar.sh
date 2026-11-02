#!/usr/bin/env bash
# Uso: tools/empaquetar.sh [version]  → dist/steam-ytmini-<version>.zip + .sha256
set -e
cd "$(dirname "$0")/.."
V="${1:-$(sed -n 's/^__version__ = "\(.*\)"/\1/p' ytmini/__init__.py)}"
mkdir -p dist
N="steam-ytmini-$V"
rm -f "dist/$N.zip"
TMP="$(mktemp -d)"; mkdir "$TMP/steam-ytmini"
cp -r LICENSE ytmini ytmini_tv.py launcher.sh install.sh requirements.txt assets docs tools README.md README.es.md CHANGELOG.md ytmini.json.example "$TMP/steam-ytmini/" 
find "$TMP" -name __pycache__ -prune -exec rm -rf {} +
(cd "$TMP" && zip -qr "$OLDPWD/dist/$N.zip" steam-ytmini)
(cd dist && sha256sum "$N.zip" > "$N.zip.sha256")
rm -rf "$TMP"
echo "dist/$N.zip"
