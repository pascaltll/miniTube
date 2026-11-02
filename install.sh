#!/usr/bin/env bash
# install.sh - prepara MiniTube: entorno Python, permisos y acceso directo del escritorio. Se puede repetir sin riesgo.
set -e
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd "$HERE"
echo "== MiniTube: instalación en $HERE"
if [ ! -x .venv/bin/python ]; then
  echo "-- creando .venv"
  python3 -m venv .venv
fi
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements.txt
echo "-- dependencias listas"
chmod +x launcher.sh install.sh tools/*.sh 2>/dev/null || true
# acceso directo del menú de aplicaciones (modo escritorio); en Steam se añade a mano, ver README
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPS"
cat > "$APPS/minitube.desktop" <<DESK
[Desktop Entry]
Type=Application
Name=MiniTube
Comment=YouTube TV dentro de Steam
Exec=$HERE/launcher.sh toggle
Icon=$HERE/assets/icon_512.png
Terminal=false
Categories=AudioVideo;Video;
DESK
echo "-- acceso directo: $APPS/minitube.desktop"
echo "== listo. Prueba: ./launcher.sh doctor"
