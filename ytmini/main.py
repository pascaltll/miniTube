"""Punto de entrada: python ytmini_tv.py [run|serve|<orden>]"""
import sys

from .crash import instalar
from .server import client, run, serve


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    c = " ".join(argv) if argv else "status"
    if argv and argv[0] in ("reporte", "report"):
        from .report import main as informe
        sys.exit(informe(argv[1:]))
    if argv and argv[0] in ("actualizar", "update"):
        from .update import main as actualizar
        sys.exit(actualizar(argv[1:]))
    if c in ("run", "serve"):
        instalar()
    if c == "run":
        run()
    elif c == "serve":
        serve()
    else:
        sys.exit(client(c))
