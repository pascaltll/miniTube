"""Diagnostic report to attach to a GitHub issue. It sends NOTHING: it writes a Markdown file in reportes/ (reports/)
with system, Steam and MiniTube data and the recent log, with username, hostname, IPs and tokens hidden."""
import getpass
import glob
import json
import os
import platform
import re
import socket
import subprocess
import time
import urllib.request
from urllib.parse import quote

from . import REPO, __version__
from .config import CFG_FILE, PORT, ROOT

_RE_IPV4 = re.compile(r"\b(?!127\.0\.0\.1\b|0\.0\.0\.0\b)\d{1,3}(?:\.\d{1,3}){3}\b")
_RE_IPV6 = re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){3,7}[0-9a-fA-F]{1,4}\b")
_RE_TOKEN = re.compile(r"[A-Za-z0-9_\-]{32,}")
_RE_SECRET = re.compile(r"(?i)(cookie|authorization|set-cookie|sapisid|apisid|ssid|sid|token)\s*[:=]\s*\S+")


def ocultar(t):
    """Remove what must not leave the machine from a text: home path, username, hostname, IPs, tokens and cookies."""
    try:
        home, user, host = os.path.expanduser("~"), getpass.getuser(), socket.gethostname()
    except Exception:
        home, user, host = "", "", ""
    if home and home != "/":
        t = t.replace(os.path.realpath(home), "~").replace(home, "~")
    if user and len(user) > 2:
        t = re.sub(r"\b%s\b" % re.escape(user), "user", t)
    if host and len(host) > 2:
        t = re.sub(r"\b%s\b" % re.escape(host), "host", t)
    t = _RE_SECRET.sub(lambda m: m.group(1) + ": <oculto>", t)
    t = _RE_IPV6.sub("<ip>", t)
    t = _RE_IPV4.sub("<ip>", t)
    return _RE_TOKEN.sub("<token>", t)


def _leer(p, n=None):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read() if n is None else f.read(n)
    except Exception:
        return ""


def _cmd(args, t=5):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=t).stdout.strip()
    except Exception as e:
        return "(unavailable: %s)" % type(e).__name__


def _os_release():
    d = {}
    for l in _leer("/etc/os-release").splitlines():
        if "=" in l:
            k, v = l.split("=", 1)
            d[k] = v.strip('"')
    return d


def _json_http(url, t=4):
    try:
        return json.load(urllib.request.urlopen(url, timeout=t))
    except Exception as e:
        return {"error": type(e).__name__}


def _demonio(cmd):
    try:
        s = socket.create_connection(("127.0.0.1", PORT), timeout=4)
        s.sendall((cmd + "\n").encode())
        return s.makefile().readline().strip()
    except Exception:
        return None


def generar():
    osr = _os_release()
    cpu = next((l.split(":", 1)[1].strip() for l in _leer("/proc/cpuinfo").splitlines() if l.startswith("model name")), "?")
    mem = next((l.split(":", 1)[1].strip() for l in _leer("/proc/meminfo").splitlines() if l.startswith("MemTotal")), "?")
    dmi = lambda n: _leer("/sys/class/dmi/id/" + n, 80).strip() or "?"
    L = []
    a = L.append
    a("# MiniTube report\n")
    a("- Version: **%s**   ·   Date: %s" % (__version__, time.strftime("%Y-%m-%d %H:%M:%S %z")))
    a("\n## System")
    a("- OS: %s (%s)" % (osr.get("PRETTY_NAME", "?"), osr.get("VARIANT_ID", osr.get("VARIANT", "-"))))
    a("- Kernel: %s" % platform.release())
    a("- Device: %s %s" % (dmi("sys_vendor"), dmi("product_name")))
    a("- CPU: %s   ·   RAM: %s" % (cpu, mem))
    a("- Session: desktop=%s, gamescope=%s" % (os.environ.get("XDG_CURRENT_DESKTOP", "-"), "yes" if _cmd(["pgrep", "-f", "gamescope-session"]) else "no"))
    a("- Python: %s   ·   websocket-client: %s" % (platform.python_version(), _ver_ws()))
    a("\n## Steam")
    ver = _json_http("http://localhost:8080/json/version")
    a("- CEF: %s" % json.dumps({k: ver.get(k) for k in ("Browser", "Protocol-Version", "error")}, ensure_ascii=False))
    try:
        tg = json.load(urllib.request.urlopen("http://localhost:8080/json", timeout=4))
        a("- Targets: " + "; ".join(sorted({(t.get("title") or "?")[:40] for t in tg})))
    except Exception as e:
        a("- Targets: (unavailable: %s)" % type(e).__name__)
    a("\n## MiniTube")
    a("- Daemon: %s" % ("running" if _demonio("ping") == "pong" else "stopped"))
    st = _demonio("status")
    if st:
        a("- Status: `%s`" % st[:600])
    ul = _demonio("ultimo")
    if ul and ul != "{}":
        a("- Last open: `%s`" % ul[:300])
    a("- ytmini.json:\n```json\n%s\n```" % (_leer(CFG_FILE).strip() or "(missing: defaults in use)"))
    fallos = sorted(glob.glob(os.path.join(ROOT, "crashes", "2*.txt")))
    a("- Crashes recorded in crashes/: %d" % len(fallos))
    a("\n## Audio")
    info = _cmd(["pactl", "info"])
    a("```\n%s\n```" % "\n".join(l for l in info.splitlines() if l.startswith(("Server Name", "Default Sink", "Server Version"))))
    a("- Active audio streams: %d" % len(re.findall(r"^Sink Input #", _cmd(["pactl", "list", "sink-inputs"]), re.M)))
    a("\n## Network")
    t0 = time.time()
    try:
        code = urllib.request.urlopen("https://www.youtube.com/tv", timeout=10).status
    except Exception as e:
        code = type(e).__name__
    a("- youtube.com/tv: %s in %.1f s" % (code, time.time() - t0))
    a("\n## Log (last 250 lines of ytmini.log)")
    log = _leer(os.path.join(ROOT, "ytmini.log")).splitlines()[-250:]
    a("```\n%s\n```" % "\n".join(log))
    if fallos:
        a("\n## Last recorded crash (%s)\n```\n%s\n```" % (os.path.basename(fallos[-1]), _leer(fallos[-1])[-4000:]))
    return ocultar("\n".join(L) + "\n")


def main(args):
    texto = generar()
    carpeta = os.path.join(ROOT, "reportes")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, "informe_%s.md" % time.strftime("%Y%m%d_%H%M%S"))
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    print("Report saved to:\n  %s\n" % ruta)
    print("It contains: version, system, Steam, MiniTube status, ytmini.json, audio, network and the recent log.")
    print("Hidden automatically: your username, hostname, personal paths, IPs, tokens and cookies.")
    print("NOTHING was sent. Review it and, if you want, attach it to a GitHub issue.")
    if "--open" in args or "--abrir" in args:
        if REPO.startswith("TU_USUARIO") or "/" not in REPO:
            print("\n(REPO is not set in ytmini/__init__.py: cannot open the issues page.)")
            return 0
        url = "https://github.com/%s/issues/new?template=bug_report.yml&version=%s" % (REPO, quote(__version__))
        print("\nOpening", url)
        try:
            subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            print("(could not open the browser; copy the address)")
    return 0


def _ver_ws():
    try:
        import websocket
        return websocket.__version__
    except Exception:
        return "not installed"
