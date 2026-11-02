#!/usr/bin/env bash
# tools/migrar.sh - ordena una carpeta con versiones antiguas: MUEVE (no borra) lo viejo a old/.
# Nunca toca: .venv, ytmini.json, ytmini.log, capturas/, ni los archivos de la versión actual.
# Uso:  tools/migrar.sh            (solo muestra qué movería)
#       tools/migrar.sh --aplicar  (lo mueve a old/)
HERE="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
cd "$HERE"
mapfile -t cand < <(ls -1d ytmini_tv_v*.py ytmini_tv_v*.py.bak launcher_v*.sh ytmini.py ytmini_daemon.py ytmini.js app.html pack.b64 \
  ytv_*.py bv_lab*.py fake_*.py patch_*.py __pycache__ informes 2>/dev/null)
if [ ${#cand[@]} -eq 0 ]; then echo "nada que mover: la carpeta ya está limpia"; exit 0; fi
printf 'se moverían a old/ (%d elementos):\n' "${#cand[@]}"; printf '  %s\n' "${cand[@]}"
if [ "$1" != "--aplicar" ]; then echo; echo "(simulación) vuelve a correr con --aplicar para moverlos"; exit 0; fi
mkdir -p old
for f in "${cand[@]}"; do mv -n -- "$f" old/; done
echo "hecho. Si todo funciona, old/ se puede borrar a mano cuando quieras."
