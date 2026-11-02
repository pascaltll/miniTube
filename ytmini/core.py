"""Estado compartido entre módulos (diccionarios mutables, cola de órdenes, cerrojo, log). Sin lógica."""
import collections
import queue
import threading
import time


REWRITE = {"on": False}


CFGV = {}


stats = collections.Counter()


LOCK = threading.RLock()


S = {"dfl": None, "conn": None, "vid": None}


def log(*x):
    print(time.strftime("%H:%M:%S"), *x, flush=True)


CMDQ = queue.Queue()
