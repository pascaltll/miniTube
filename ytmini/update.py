"""Update: look for a new version on GitHub and apply a zip (downloaded or local) without touching the configuration.
It backs up the code in respaldos/ (backups/), keeps ytmini.json, logs, screenshots and the .venv, and only reinstalls
dependencies if requirements.txt changed. So install.sh does NOT need to be run again on every update."""
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile

from . import REPO, __version__
from .config import PORT, ROOT

PROTEGIDOS = {"ytmini.json", "ytmini.log", "capturas", "crashes", "reportes", "respaldos", ".venv", "desarrollo", "old"}
CODIGO = ["ytmini", "ytmini_tv.py", "launcher.sh", "install.sh", "requirements.txt", "assets", "docs", "tools", "README.md", "CHANGELOG.md", "ytmini.json.example"]


def _ver(s):
    return tuple(int(x) for x in re.findall(r"\d+", str(s).split("-")[0])[:3])


def ultima():
    """(tag, zip_url, sha256_url, notes_url) of the latest published release."""
    if REPO.startswith("TU_USUARIO") or "/" not in REPO:
        raise RuntimeError("REPO is not set in ytmini/__init__.py (there is no repository to ask yet)")
    req = urllib.request.Request("https://api.github.com/repos/%s/releases/latest" % REPO,
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "minitube-updater"})
    d = json.load(urllib.request.urlopen(req, timeout=10))
    zipu = sha = None
    for a in d.get("assets", []):
        n = a.get("name", "")
        if n.endswith(".zip") and not zipu:
            zipu = a["browser_download_url"]
        elif n.endswith(".sha256"):
            sha = a["browser_download_url"]
    return d.get("tag_name", "?"), zipu, sha, d.get("html_url", "")


def _descargar(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "minitube-updater"})
    with urllib.request.urlopen(req, timeout=60) as r, open(destino, "wb") as f:
        while True:
            b = r.read(1 << 16)
            if not b:
                break
            f.write(b)


def _parar():
    try:
        s = socket.create_connection(("127.0.0.1", PORT), timeout=3)
        s.sendall(b"stop\n")
        s.makefile().readline()
    except Exception:
        pass
    try:
        subprocess.run(["systemctl", "--user", "stop", "ytmini-tv"], capture_output=True, timeout=8)
    except Exception:
        pass
    time.sleep(1.2)


def aplicar(ruta_zip, sha_esperado=None):
    ruta_zip = os.path.abspath(ruta_zip)
    if sha_esperado:
        h = hashlib.sha256(open(ruta_zip, "rb").read()).hexdigest()
        if h.lower() != sha_esperado.lower():
            print("ERROR: the sha256 sum does not match; the update is not applied.")
            return 1
        print("sha256 verified")
    with zipfile.ZipFile(ruta_zip) as z:
        nombres = z.namelist()
        init = next((n for n in nombres if n.endswith("ytmini/__init__.py")), None)
        if not init:
            print("ERROR: this zip does not look like a MiniTube release (ytmini/__init__.py is missing).")
            return 1
        prefijo = init[: -len("ytmini/__init__.py")]
        m = re.search(r'__version__\s*=\s*"([^"]+)"', z.read(init).decode("utf-8", "replace"))
        nueva = m.group(1) if m else "?"
        req_viejo = open(os.path.join(ROOT, "requirements.txt")).read() if os.path.exists(os.path.join(ROOT, "requirements.txt")) else ""
        print("Updating %s → %s" % (__version__, nueva))
        _parar()
        # back up the code
        os.makedirs(os.path.join(ROOT, "respaldos"), exist_ok=True)
        resp = os.path.join(ROOT, "respaldos", "v%s_%s.zip" % (__version__, time.strftime("%Y%m%d_%H%M%S")))
        with zipfile.ZipFile(resp, "w", zipfile.ZIP_DEFLATED) as zb:
            for nombre in CODIGO:
                p = os.path.join(ROOT, nombre)
                if os.path.isdir(p):
                    for r, ds, fs in os.walk(p):
                        ds[:] = [d for d in ds if d != "__pycache__"]
                        for f in fs:
                            zb.write(os.path.join(r, f), os.path.relpath(os.path.join(r, f), ROOT))
                elif os.path.isfile(p):
                    zb.write(p, nombre)
        print("backup:", resp)
        # extraer (sin tocar lo protegido y sin salir de ROOT)
        base = os.path.realpath(ROOT)
        n = 0
        for info in z.infolist():
            if info.is_dir() or not info.filename.startswith(prefijo):
                continue
            rel = info.filename[len(prefijo):]
            if not rel or rel.split("/")[0] in PROTEGIDOS or "__pycache__" in rel:
                continue
            dest = os.path.realpath(os.path.join(ROOT, rel))
            if not dest.startswith(base + os.sep):
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(info) as src, open(dest, "wb") as out:
                out.write(src.read())
            modo = (info.external_attr >> 16) & 0o777
            if modo:
                os.chmod(dest, modo)
            n += 1
        req_nuevo = open(os.path.join(ROOT, "requirements.txt")).read() if os.path.exists(os.path.join(ROOT, "requirements.txt")) else ""
    print("%d files updated (ytmini.json, logs, screenshots and .venv untouched)" % n)
    if req_nuevo != req_viejo:
        print("requirements.txt changed: installing dependencies…")
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "-r", os.path.join(ROOT, "requirements.txt")])
    print("Done: MiniTube %s. Open it from Steam or run ./launcher.sh doctor. If anything breaks, the previous code is in %s" % (nueva, resp))
    return 0


def main(args):
    zips = [a for a in args if a.endswith(".zip")]
    if zips:
        return aplicar(zips[0])
    try:
        tag, zipu, shau, notas = ultima()
    except Exception as e:
        print("Could not query GitHub:", e)
        return 1
    if _ver(tag) <= _ver(__version__):
        print("You are up to date: v%s (latest published: %s)." % (__version__, tag))
        return 0
    print("A new version is available: %s (you have v%s)." % (tag, __version__))
    if notas:
        print("What's new:", notas)
    if "--install" not in args and "--instalar" not in args:
        print("To install it: ./launcher.sh update --install")
        return 0
    if not zipu:
        print("The release has no attached .zip.")
        return 1
    tmp = tempfile.mkdtemp(prefix="minitube_")
    z = os.path.join(tmp, "release.zip")
    print("Downloading…")
    _descargar(zipu, z)
    sha = None
    if shau:
        try:
            _descargar(shau, os.path.join(tmp, "sha"))
            sha = open(os.path.join(tmp, "sha")).read().split()[0]
        except Exception:
            sha = None
    if not sha:
        print("(the release has no sha256 sum: applying without verifying)")
    return aplicar(z, sha)
