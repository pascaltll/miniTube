#!/usr/bin/env bash
# launcher.sh - MiniTube (ytmini): YouTube TV inside Steam. Meant for a Steam shortcut ("non-Steam game"):
# one tap = open/close. With no arguments it behaves like "toggle". See ./launcher.sh help.
# The daemon is started OUTSIDE the shortcut's process tree (systemd-run --user) so Steam does not think "the game is still running".
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
PY="$HERE/.venv/bin/python"; [ -x "$PY" ] || PY="$(command -v python3)"
APP="$HERE/ytmini_tv.py"; LOG="$HERE/ytmini.log"; PORT=8799
cmd="${1:-toggle}"
# English command names -> internal names (the Spanish ones keep working)
case "$cmd" in
  type) cmd=escribir;; keyboard) cmd=teclado;; reload) cmd=recargar;; level1) cmd=nivel1;; level2) cmd=nivel2;;
  quality) cmd=calidad;; report) cmd=reporte;; update) cmd=actualizar;; test-notice) cmd=probar-aviso;;
  key) cmd=tecla;; page) cmd=pagina;;
esac
alive() { "$PY" "$APP" ping >/dev/null 2>&1; }

ayuda() {
cat <<'TXT'
MiniTube - usage: ./launcher.sh [command] [arguments]

Daily use
  (no command) | toggle  open YouTube TV, or close it if already open (starts the daemon if needed)
  open | close           open / close (close ends playback and stops the daemon)
  mini | unmini          small card / back to normal size
  pp                     play / pause
  fs                     fullscreen
  vol <game|youtube|general> [N|+N|-N]    volume
  type <text>            type text into the Leanback search box   (alias: escribir)
  keyboard               open Steam's on-screen keyboard           (alias: teclado)
  status                 daemon status
  stop                   stop the daemon and restore the view and the User-Agent
  run                    daemon in the foreground, with console (quit with Ctrl+C; NEVER Ctrl+Z)
  logs                   last 40 lines of ytmini.log

Settings
  reload                 re-read ytmini.json without restarting   (alias: recargar)
  level1 | level2        mini over a game: draw only (1) / accepts touch and gamepad (2)   (aliases: nivel1, nivel2)
  quality [auto|fit|tiny|small|medium|large|hd720|hd1080]   show or force quality (fit = highest that fits)   (alias: calidad)

Maintenance and diagnostics
  install                create .venv, install dependencies and register the desktop launcher
  doctor                 check Python, dependencies, ytmini.json, Steam (CEF :8080), daemon and network
  report [--open]        write a report to paste into a GitHub issue (sends nothing; see README)   (alias: reporte)
  update [file.zip|--install]   apply a zip, or check/install the latest GitHub release   (alias: actualizar)
  test-notice            show what the desktop-mode notice looks like   (alias: probar-aviso)
  kill                   kill any stale daemon process (for example one suspended with Ctrl+Z)
  version                installed version
  key <up|down|left|right|enter|back|pgup|pgdn>   send a key to YouTube (Shorts/scroll experiments in mini)   (alias: tecla)
  page                   player and page state (Shorts, video size, focus)   (alias: pagina)
  diag geo trace azul eventos perf bvapi bvopts inspect targets mic audio setb shot
                         see docs/FICHA_TECNICA.md for what each one measures
TXT
}

en_game_mode() { pgrep -f gamescope-session >/dev/null 2>&1 || [ "${XDG_SESSION_DESKTOP:-}" = gamescope ]; }

# aviso "text": dialog with the MiniTube icon on the desktop (kdialog/zenity/notify-send);
# in Game Mode it opens no windows (Steam's card notifies there) and it always writes to the terminal.
aviso() {
  local ic="$HERE/assets/icon_512.png" t="MiniTube" m="$1"
  printf '%s: %s\n' "$t" "$m" >&2
  en_game_mode && return 0
  [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ] || return 0
  if command -v kdialog >/dev/null 2>&1; then ( setsid kdialog --title "$t" --icon "$ic" --msgbox "${m//$'\n'/<br>}" >/dev/null 2>&1 & ); return 0; fi
  if command -v zenity >/dev/null 2>&1; then ( setsid zenity --info --title="$t" --window-icon="$ic" --width=440 --text="$m" >/dev/null 2>&1 & ); return 0; fi
  command -v notify-send >/dev/null 2>&1 && notify-send -i "$ic" "$t" "$m"
  return 0
}

MSG_SIN_STEAM="MiniTube runs inside Steam in Game Mode (Big Picture with Decky Loader and developer mode enabled).\n\nSteam does not seem to be in that mode right now. Switch to Game Mode and open MiniTube again from your library.\n\nMore information: ./launcher.sh doctor"

# wait for the open result (the daemon's S["ultimo"]) and notify if it failed
esperar_apertura() {
  local i r est msg
  for i in $(seq 1 60); do
    r="$("$PY" "$APP" ultimo 2>/dev/null)"
    est="$("$PY" -c "import json,sys;d=json.loads(sys.argv[1] or '{}');print(d.get('estado',''))" "$r" 2>/dev/null)"
    case "$est" in
      error) msg="$("$PY" -c "import json,sys;print(json.loads(sys.argv[1]).get('msg',''))" "$r")"
             case "$msg" in *Steam/Decky*|*CEF*) aviso "$MSG_SIN_STEAM";;
               *) aviso "MiniTube could not open:\n$msg\n\nTry ./launcher.sh doctor, or write a report with ./launcher.sh report";; esac
             return 1;;
      listo) return 0;;
    esac
    sleep 0.5
  done
  return 0
}

start_daemon() {
  alive && return 0
  if command -v systemd-run >/dev/null 2>&1 && \
     systemd-run --user --quiet --collect --unit=ytmini-tv \
       -p StandardOutput=append:"$LOG" -p StandardError=append:"$LOG" \
       -p WorkingDirectory="$HERE" "$PY" -u "$APP" serve 2>>"$LOG"; then :
  else
    echo "$(date +%T) systemd-run not available: using setsid" >>"$LOG"
    setsid nohup "$PY" -u "$APP" serve >>"$LOG" 2>&1 < /dev/null &
  fi
  for _ in $(seq 1 120); do alive && return 0; sleep 0.25; done
  echo "ERROR: the daemon did not start. Last lines of $LOG:" >&2; tail -n 15 "$LOG" >&2; return 1
}

doctor() {
  ok() { echo "  [ok]   $*"; }; mal() { echo "  [FAIL] $*"; fallos=1; }; fallos=0
  echo "MiniTube $(sed -n 's/^__version__ = "\(.*\)"/\1/p' "$HERE/ytmini/__init__.py")  ($HERE)"
  [ -x "$PY" ] && ok "Python: $PY ($("$PY" -V 2>&1))" || mal "no Python found (run ./launcher.sh install)"
  "$PY" -c "import websocket" 2>/dev/null && ok "websocket-client installed" || mal "websocket-client missing (./launcher.sh install)"
  if [ -f "$HERE/ytmini.json" ]; then
    e="$("$PY" -c "import json,sys;json.load(open(sys.argv[1]))" "$HERE/ytmini.json" 2>&1)" && ok "ytmini.json valid" \
      || mal "ytmini.json unreadable: ${e##*: } (decimals with a dot, no trailing commas)"
  else ok "no ytmini.json (defaults in use)"; fi
  if curl -s -m 4 http://localhost:8080/json/version >/dev/null; then ok "Steam CEF answers on localhost:8080"
  else mal "CEF does not answer on :8080 (is Steam open in Big Picture with Decky Loader and developer mode?)"; fi
  if alive; then ok "daemon running on 127.0.0.1:$PORT"
  else
    pgrep -f "ytmini_tv.py (run|serve)" >/dev/null && mal "a daemon process is not responding (suspended or hung): ./launcher.sh kill" \
      || ok "daemon stopped (it starts by itself on open)"
  fi
  c="$(curl -s -o /dev/null -m 15 -w '%{http_code}/%{time_total}s' https://www.youtube.com/tv)"
  case "$c" in 200*) ok "YouTube TV reachable ($c)";; *) mal "YouTube TV not reachable ($c): network, VPN or blocking; if the view says 'error code -7' it is a network timeout";; esac
  return $fallos
}

case "$cmd" in
  toggle|open|mini)
    if ! curl -s -m 3 http://localhost:8080/json/version >/dev/null 2>&1; then aviso "$MSG_SIN_STEAM"; exit 3; fi
    start_daemon || { aviso "The MiniTube daemon did not start. Check ./launcher.sh logs or write a report with ./launcher.sh report"; exit 1; }
    "$PY" "$APP" "a$cmd"; esperar_apertura ;;
  close|status|unmini|pp|inspect|targets|recargar|shot|captura|diag|bvapi|geo|trace|azul|eventos|calidad|setb|perf|fs|nivel1|nivel2|mic|bvopts|teclado|tecla|pagina|audio|vol|escribir)  shift; "$PY" "$APP" "$cmd" "$@" ;;
  stop)          "$PY" "$APP" stop; systemctl --user stop ytmini-tv 2>/dev/null; true ;;
  kill)          systemctl --user stop ytmini-tv 2>/dev/null; pkill -CONT -f "ytmini_tv.py" 2>/dev/null; pkill -f "ytmini_tv.py (run|serve)" 2>/dev/null; sleep 1
                 pgrep -af "ytmini_tv.py" || echo "no daemon processes" ;;
  run)           exec "$PY" -u "$APP" run ;;
  logs)          tail -n 40 "$LOG" ;;
  doctor)        doctor ;;
  reporte|actualizar) shift; exec "$PY" "$APP" "$cmd" "$@" ;;
  probar-aviso)  aviso "This is what a MiniTube notice looks like.\n\n$(printf '%b' "$MSG_SIN_STEAM")" ;;
  install)       exec bash "$HERE/install.sh" ;;
  version)       sed -n 's/^__version__ = "\(.*\)"/MiniTube v\1/p' "$HERE/ytmini/__init__.py" ;;
  help|-h|--help|"") ayuda ;;
  *)             echo "unknown command: $cmd" >&2; ayuda; exit 2 ;;
esac
