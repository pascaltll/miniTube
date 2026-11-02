"""Servidor local 127.0.0.1:PORT, consola (run), demonio (serve) y cliente (órdenes desde otra terminal)."""
import os
import socket
import socketserver
import threading
import time
from .commands import cmd_worker, do, poll, watch
from .config import PORT
from .core import log


class H(socketserver.StreamRequestHandler):
    def handle(self):
        cmd = self.rfile.readline().decode().strip()
        try:
            out = do(cmd)
        except Exception as e:
            out = "ERROR: %r" % e
        self.wfile.write((out + "\n").encode())


class Srv(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


AYUDA = "  f = screenshots (zip)   m = mini card   o = open   c = close   t = toggle   r = reload config (ytmini.json)   s = status   q = quit"


def run():
    srv = Srv(("127.0.0.1", PORT), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    log("YouTube TV para Steam. Control extra desde otra terminal: python ytmini_tv.py open|close|toggle|status|stop")
    threading.Thread(target=watch, daemon=True).start()
    threading.Thread(target=poll, daemon=True).start()
    threading.Thread(target=cmd_worker, daemon=True).start()
    print("Preparing the view (a few seconds)…")
    print(do("open"))
    print(AYUDA)
    try:
        while True:
            try:
                c = input("ytmini> ").strip().lower()
            except EOFError:
                time.sleep(3600)
                continue
            m = {"f": "shot", "m": "mini", "o": "open", "c": "close", "t": "toggle", "r": "recargar", "s": "status", "q": "stop"}.get(c, "")
            if not m:
                print(AYUDA)
                continue
            print(do(m))
    except KeyboardInterrupt:
        print("\nExiting…")
        do("stop")
        time.sleep(1)


def serve():
    """Sin consola (para launcher.sh / systemd): servidor + vigilante; SIGTERM limpia la vista."""
    import signal
    srv = Srv(("127.0.0.1", PORT), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    threading.Thread(target=watch, daemon=True).start()
    threading.Thread(target=poll, daemon=True).start()
    threading.Thread(target=cmd_worker, daemon=True).start()
    log("demonio (sin consola) listo en 127.0.0.1:%d" % PORT)

    def bye(*_):
        log("SIGTERM: limpiando")
        try:
            do("stop")
        finally:
            os._exit(0)
    signal.signal(signal.SIGTERM, bye)
    while True:
        time.sleep(3600)


def client(cmd):
    try:
        s = socket.create_connection(("127.0.0.1", PORT), timeout=45)
    except OSError:
        print("the daemon is not running (run ./launcher.sh)")
        return 2
    s.sendall((cmd + "\n").encode())
    out = s.makefile().readline().strip()
    print(out)
    return 0 if not out.startswith("ERROR") else 1
