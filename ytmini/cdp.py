"""Cliente CDP (Chrome DevTools Protocol) hacia el CEF de Steam: conexión, reescritura de User-Agent (Fetch), pestañas."""
from urllib.parse import urlparse
from websocket import create_connection, WebSocketTimeoutException
import json
import queue
import threading
import time
import urllib.request
from .config import BLOCK_PATTERNS, BLOCK_RE, META, UA
from .core import CFGV, CMDQ, REWRITE, stats
from .js import STATE


class Conn:
    """Conexion CDP con hilo lector. El lector atiende las peticiones pausadas SIN esperar a nadie."""

    def __init__(self, url, on_paused=None, on_event=None):
        self.ws = create_connection(url, timeout=1)
        self.n, self.lock, self.waiters, self.on_paused, self.alive = 0, threading.Lock(), {}, on_paused, True
        self.on_event = on_event
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        while self.alive:
            try:
                raw = self.ws.recv()
            except WebSocketTimeoutException:
                continue
            except Exception:
                self.alive = False
                return
            if not raw:
                continue
            m = json.loads(raw)
            if "id" in m:
                q = self.waiters.pop(m["id"], None)
                if q:
                    q.put(m)
            elif m.get("method") == "Runtime.consoleAPICalled":
                try:
                    a = (m["params"].get("args") or [{}])[0].get("value")
                    if isinstance(a, str) and a.startswith("__ytmcmd__"):
                        CMDQ.put((a[10:], time.time()))
                except Exception:
                    pass
            elif m.get("method") == "Runtime.bindingCalled" and self.on_event:
                try:
                    self.on_event(m["params"])
                except Exception:
                    pass
            elif m.get("method") == "Fetch.requestPaused" and self.on_paused:
                try:
                    self.on_paused(self, m["params"])
                except Exception:
                    pass

    def send(self, method, params=None, q=None):
        with self.lock:
            self.n += 1
            i = self.n
        if q is not None:
            self.waiters[i] = q
        self.ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        return i

    def call(self, method, params=None, timeout=5):
        q = queue.Queue(1)
        i = self.send(method, params, q)
        try:
            return q.get(timeout=timeout)
        except queue.Empty:
            self.waiters.pop(i, None)
            return {"error": "timeout"}

    def val(self, expr, timeout=3):
        return self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True}, timeout).get(
            "result", {}).get("result", {}).get("value")

    def close(self):
        self.alive = False
        try:
            self.ws.close()
        except Exception:
            pass


def on_paused(conn, q):
    url = q["request"].get("url", "")
    if REWRITE["on"] and CFGV.get("bloqueo_red") and BLOCK_RE.search(url):
        conn.send("Fetch.failRequest", {"requestId": q["requestId"], "errorReason": "BlockedByClient"})
        stats["bloqueadas"] += 1
    elif REWRITE["on"] and (urlparse(url).hostname or "").endswith("youtube.com"):
        hh = [{"name": k, "value": (UA if k.lower() == "user-agent" else v)} for k, v in q["request"]["headers"].items()]
        conn.send("Fetch.continueRequest", {"requestId": q["requestId"], "headers": hh})
        stats[q.get("resourceType", "?")] += 1
    else:
        conn.send("Fetch.continueRequest", {"requestId": q["requestId"]})


def arm(conn):
    if CFGV.get("cdp_network"):  # v47: nadie lee eventos Network.*; solo se activa si se pide
        conn.call("Network.enable")
    conn.call("Network.setBypassServiceWorker", {"bypass": True})
    conn.call("Emulation.setUserAgentOverride", {"userAgent": UA, "userAgentMetadata": META})
    REWRITE["on"] = True
    pats = [{"urlPattern": "https://*.youtube.com/*", "resourceType": t, "requestStage": "Request"}
            for t in (("Document",) if CFGV.get("fetch_solo_documento") else ("Document", "XHR", "Fetch"))]
    if CFGV.get("bloqueo_red"):
        pats += [{"urlPattern": p, "requestStage": "Request"} for p in BLOCK_PATTERNS]
    conn.call("Fetch.enable", {"patterns": pats})


def disarm(conn):
    REWRITE["on"] = False
    for m, p in (("Fetch.disable", None), ("Emulation.setUserAgentOverride", {"userAgent": ""}),
                 ("Network.setBypassServiceWorker", {"bypass": False})):
        try:
            conn.call(m, p, timeout=2)
        except Exception:
            pass


def tabs():
    return json.load(urllib.request.urlopen("http://localhost:8080/json", timeout=5))


def is_browser_tab(t):
    u = urlparse(t.get("url", ""))
    return (t.get("type") == "page" and u.scheme in ("http", "https") and u.hostname != "steamloopback.host"
            and bool(t.get("webSocketDebuggerUrl")))


def wait_tab(pred, secs):
    end = time.time() + secs
    while time.time() < end:
        for t in tabs():
            if pred(t):
                return t
        time.sleep(0.5)


def find_dfl():
    for t in tabs():
        if not t.get("webSocketDebuggerUrl"):
            continue
        try:
            c = Conn(t["webSocketDebuggerUrl"])
            if c.val("typeof window.DFL!=='undefined'&&typeof window.SP_REACT!=='undefined'", 3) is True:
                return c
            c.close()
        except Exception:
            continue


def state(conn, timeout=3):
    try:
        return json.loads(conn.val(STATE, timeout) or "null")
    except Exception:
        return None
