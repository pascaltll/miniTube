"""Crash capture: unhandled exceptions (also in threads) and hard crashes (faulthandler) are kept in crashes/
so they can be attached to a report. Nothing is sent anywhere."""
import faulthandler
import os
import sys
import threading
import time
import traceback

from . import __version__
from .config import ROOT

CRASH_DIR = os.path.join(ROOT, "crashes")
_fh = None


def _escribir(titulo, texto):
    try:
        os.makedirs(CRASH_DIR, exist_ok=True)
        p = os.path.join(CRASH_DIR, time.strftime("%Y%m%d_%H%M%S") + ".txt")
        with open(p, "a", encoding="utf-8") as f:
            f.write("MiniTube v%s | python %s | %s\n%s\n\n%s\n" % (__version__, sys.version.split()[0], time.strftime("%Y-%m-%d %H:%M:%S"), titulo, texto))
        print("crash recorded in", p, flush=True)
    except Exception:
        pass


def instalar():
    """Hook the exception handlers. Call once at startup."""
    global _fh

    def hook(tp, v, tb):
        _escribir("unhandled exception", "".join(traceback.format_exception(tp, v, tb)))
        sys.__excepthook__(tp, v, tb)

    def thook(a):
        if a.exc_type is SystemExit:
            return
        _escribir("exception in thread %s" % (a.thread.name if a.thread else "?"), "".join(traceback.format_exception(a.exc_type, a.exc_value, a.exc_traceback)))

    sys.excepthook = hook
    threading.excepthook = thook
    try:
        os.makedirs(CRASH_DIR, exist_ok=True)
        _fh = open(os.path.join(CRASH_DIR, "faulthandler.log"), "a")
        faulthandler.enable(file=_fh)
    except Exception:
        pass
