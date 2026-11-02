"""Lado Steam/Decky: crear y mantener la BrowserView, adjuntar la pestaña de YouTube, modo de controles, JS inyectado."""
from urllib.parse import urlparse
import json
import threading
import time
import urllib.request
from .cdp import Conn, arm, find_dfl, on_paused, state, tabs, wait_tab
from .config import URL, load_cfg
from .core import CFGV, CMDQ, REWRITE, S, log
from .js import CAL_JS, CREATE_JS, LOAD_JS, MINI_JS, PAGE_JS, PROBE_JS, REMOVE_LOAD_JS, SHOW_JS


def aplicar_calidad(q, retardos=(0,)):
    """Baja (o restaura) la calidad de YouTube en segundo plano: la tarjeta pequeña no necesita 1080p.
    retardos: segundos tras los que se (re)aplica; "fit" necesita esperar a que la vista termine de cambiar de tamaño."""
    def _w():
        t0 = time.time()
        for d in retardos:
            time.sleep(max(0, d - (time.time() - t0)))
            try:
                if S["conn"] and S["conn"].alive:
                    S["conn"].val(CAL_JS.replace("__Q__", q), 4)
            except Exception:
                pass
    threading.Thread(target=_w, daemon=True).start()


def calidad_ventana():
    """Calidad al volver a ventana normal o pantalla completa (clave ventana_calidad):
    "ajustada" = la más alta que cabe en la vista (por defecto), "auto" = decide YouTube, o un nivel concreto (hd720, hd1080…)."""
    v = load_cfg().get("ventana_calidad", "ajustada")
    if v == "auto":
        aplicar_calidad("auto")
    elif v == "ajustada":
        aplicar_calidad("fit", (0.4, 1.5, 4.0))
    else:
        aplicar_calidad(v)


def tarjeta(msg, error=False):
    """Tarjeta de carga/aviso dentro de Steam (componente global de Decky). Si Decky no responde, no hace nada."""
    try:
        d = S["dfl"]
        if d and d.alive:
            d.val(LOAD_JS.replace("__MSG__", json.dumps(msg)).replace("__ERR__", "true" if error else "false"), 3)
    except Exception:
        pass


def quitar_tarjeta():
    try:
        d = S["dfl"]
        if d and d.alive:
            d.val(REMOVE_LOAD_JS, 3)
    except Exception:
        pass


def get_dfl():
    d = S["dfl"]
    try:
        if d and d.alive and d.val("1+1", 3) == 2:
            return d
    except Exception:
        pass
    if d:
        d.close()
    S["dfl"] = find_dfl()
    if S["dfl"]:
        S["dfl"].val(PROBE_JS, 20)
        log("pestaña de Decky encontrada")
    return S["dfl"]


def view_alive():
    c, d = S["conn"], S["dfl"]
    try:
        return bool(c and c.alive and c.val("1+1", 3) == 2 and d and d.val("!!window.__bv", 3) is True)
    except Exception:
        return False


def on_binding(p):
    if p.get("name") == "ytminiCmd":
        CMDQ.put((str(p.get("payload", "")), time.time()))


def set_mode(m):
    """Modo de los controles dentro de la pagina de YouTube: full | mini | none (solo si botones=pagina)."""
    if load_cfg().get("botones") != "pagina":
        m = "none"
    try:
        if S["conn"]:
            S["conn"].val("window.__ytmMode=%s;0" % json.dumps(m), 2)
    except Exception:
        pass


def page_js():
    return PAGE_JS.replace("__CFG__", json.dumps(load_cfg()))


def show_js():
    fijo = load_cfg().get("modal") == "completo"
    outer = ("{position:'fixed',top:0,left:0,width:'100vw',height:'100vh',zIndex:5}" if fijo
             else "{width:'100%',height:'84vh',position:'relative'}")
    return SHOW_JS.replace("__OUTER__", outer).replace("__STEAMBTN__", "true" if load_cfg().get("botones") == "steam" else "false")


def mini_js():
    c = load_cfg()
    ui = {"mode": "pill" if S.pop("pill", False) else (c["mini_modo"] if c["mini_modo"] in ("video", "bar") else "video"), "w": int(c["mini_ancho"]),
          "corner": c["mini_esquina"] if c["mini_esquina"] in ("abajo-derecha", "abajo-izquierda", "arriba-derecha", "arriba-izquierda") else "abajo-derecha"}
    marg = {"m": int(c["mini_margen"]), "mb": int(c["mini_margen_inferior"]), "nivel": int(c.get("mini_nivel", 1)), "mt": bool(c.get("mini_mover_tactil", True)), "sh": bool(c.get("mini_shorts", False))}
    return MINI_JS.replace("__UI__", json.dumps(ui)).replace("__MARG__", json.dumps(marg)).replace("__STEAMBTN__", "true" if c.get("botones") == "steam" else "false")


def attach(t):
    if S["conn"]:
        S["conn"].close()
    conn = Conn(t["webSocketDebuggerUrl"], on_paused, on_binding)
    conn.call("Page.enable")
    conn.call("Runtime.enable")
    conn.call("Runtime.addBinding", {"name": "ytminiCmd"})
    CFGV.clear()
    CFGV.update(load_cfg())
    arm(conn)
    CFGV.clear()
    CFGV.update(load_cfg())
    r = conn.call("Page.addScriptToEvaluateOnNewDocument", {"source": page_js()})
    S["sid"] = (r.get("result") or {}).get("identifier")
    conn.call("Emulation.setFocusEmulationEnabled", {"enabled": True})
    S["conn"], S["vid"] = conn, t["id"]


def grant_mic():
    """Concede el microfono al contexto de navegacion de la vista (el permiso por defecto no le llega)."""
    res = []
    try:
        ver = json.load(urllib.request.urlopen("http://localhost:8080/json/version", timeout=5))
        bc = Conn(ver["webSocketDebuggerUrl"])
        try:
            ctx = None
            tg = bc.call("Target.getTargets").get("result", {}).get("targetInfos", [])
            for t in tg:
                if t.get("targetId") == S.get("vid"):
                    ctx = t.get("browserContextId")
            res.append("contexto=" + ("sí" if ctx else "no"))
            for origin in ("https://www.youtube.com", None):
                prm = {"permissions": ["audioCapture"]}
                if origin:
                    prm["origin"] = origin
                if ctx:
                    prm["browserContextId"] = ctx
                r = bc.call("Browser.grantPermissions", prm)
                res.append("%s: %s" % (origin or "todos", "ok" if "error" not in r else str(r["error"])[:60]))
        finally:
            bc.close()
    except Exception as e:
        res.append("fallo %r" % (e,))
    return ", ".join(res)


def make_view(dfl):
    before = {t["id"] for t in tabs()}
    r = dfl.val(CREATE_JS % json.dumps("ytmini-%d" % int(time.time())), 8)
    if r != "ok":
        return "could not create the view (%s)" % r
    t = wait_tab(lambda x: x["id"] not in before and x.get("type") == "page" and x.get("webSocketDebuggerUrl"), 10)
    if not t:
        return "the view did not show up in CEF"
    attach(t)
    dfl.val("window.__bv.LoadURL(%s)" % json.dumps(URL), 5)
    tarjeta("Loading YouTube TV…")
    for _ in range(36):
        time.sleep(0.5)
        s = state(S["conn"], 5) if S["conn"] and S["conn"].alive else None
        if _ % 3 == 2:
            log("esperando a Leanback…", "(vista cambiada, reconectando)" if not s else "(%s nodos)" % s.get("n"))
        if s and _ == 17 and s.get("n", 999) < 20 and not s["path"].startswith("/tv"):
            log("aviso: la vista parece una página de error (pocos nodos). Si dice 'error code -7', es un timeout de red: prueba curl -I https://www.youtube.com/tv y, si responde, reinicia el sistema.")
        if not s:
            t2 = wait_tab(lambda x: x["id"] not in before and x.get("type") == "page"
                          and (urlparse(x.get("url", "")).hostname or "").endswith("youtube.com")
                          and x.get("webSocketDebuggerUrl"), 3)
            if t2:
                attach(t2)
            continue
        if s["path"].startswith("/tv") and s["n"] > 100:
            log("Leanback cargado en la vista (%s)" % s["title"])
            log("micrófono:", grant_mic())
            return None
    return "Leanback did not finish loading"


def ensure_view():
    """Devuelve None si la vista esta lista; si no, un texto con el motivo."""
    try:
        dfl = get_dfl()
    except Exception:
        dfl = None
    if not dfl:
        return "Steam/Decky is not ready (Big Picture with Decky? CEF on localhost:8080?)"
    dfl.val(PROBE_JS, 20)
    if view_alive():
        if not REWRITE["on"]:
            arm(S["conn"])
            log("reescritura de UA rearmada")
        return None
    log("creando la vista…")
    tarjeta("Preparing the view…")
    err = make_view(dfl)
    if err:
        tarjeta(err, True)
        threading.Timer(6.0, quitar_tarjeta).start()
    return err


def modal_open():
    d = S["dfl"]
    return bool(d and d.val("!!window.__bvm", 3) is True)
