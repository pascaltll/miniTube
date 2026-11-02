"""Orden central do(): todos los comandos, cola de órdenes de la página, sondeos y vigilante."""
from urllib.parse import urlparse
import json
import os
import threading
import time
from .audio import push_game, vol_juego, vol_youtube
from .cdp import Conn, arm, disarm, state, tabs
from .config import ROOT, load_cfg, save_cfg
from .core import CFGV, CMDQ, LOCK, REWRITE, S, log, stats
from .js import AUDIO_JS, AZUL_JS, BVAPI_JS, BVOPTS_JS, CAL_JS, CLOSE_JS, DESTROY_JS, DIAG_JS, EVT_JS, INSPECT_JS, KB_JS, META_JS, MIC_JS, MINI_GEO_JS, PAGINA_JS, PAUSE_JS, PP_JS, REMOVE_MINI_JS, VOL_JS
from .metrics import perf
from .steam import aplicar_calidad, calidad_ventana, ensure_view, get_dfl, grant_mic, mini_js, modal_open, page_js, quitar_tarjeta, set_mode, show_js, view_alive


def cmd_worker():
    sizes = [320, 420, 560]
    while True:
        c, t_rx = CMDQ.get()
        t_tap = None
        if "@" in c:
            c, ts = c.split("@", 1)
            try:
                t_tap = int(ts) / 1000.0
            except ValueError:
                pass
        t_go = time.time()
        try:
            if c == "close":
                log("page: close and quit →", do("stop"))
            elif c == "mini":
                log("page: minimize →", do("mini"))
            elif c == "vgopen":
                push_game()
            elif c.startswith("vg:"):
                vol_juego("abs", int(c[3:]))
            elif c == "kb":
                log("page: Steam keyboard →", do("teclado"))
            elif c == "fs":
                log("page: fullscreen →", do("fs"))
            elif c == "full":
                log("page: expand →", do("open"))
            elif c == "pp":
                do("pp")
            elif c == "stopmini":
                if S["conn"]:
                    S["conn"].val(PAUSE_JS, 3)
                log("page: close card →", do("unmini"))
            elif c == "size":
                cur = int(load_cfg()["mini_ancho"])
                nxt = sizes[(sizes.index(cur) + 1) % len(sizes)] if cur in sizes else sizes[1]
                save_cfg({"mini_ancho": nxt})
                if S["dfl"]:
                    S["dfl"].val("(()=>{if(window.__bvui)window.__bvui.w=%d;return 0})()" % nxt, 3)
            elif c in ("kup", "kdown"):
                do("tecla " + ("up" if c == "kup" else "down"))
            elif c == "swbar":
                minimizar_auto("página: deslizar abajo")
            elif c == "bar":
                save_cfg({"mini_modo": "bar"})
                if S["dfl"]:
                    S["dfl"].val("(()=>{if(window.__bvui)window.__bvui.mode='bar';return 0})()", 3)
        except Exception as e:
            log("error en la orden de la página:", repr(e))
        t_end = time.time()
        if t_tap:
            log("tiempos %s: toque→cola %d ms, cola→ejecutar %d ms, ejecutar %d ms, total %d ms" % (
                c, (t_rx - t_tap) * 1000, (t_go - t_rx) * 1000, (t_end - t_go) * 1000, (t_end - t_tap) * 1000))


def _trabajo(c):
    """Ejecuta una orden de apertura en segundo plano y deja el resultado en S["ultimo"] (lo lee launcher.sh para avisar de errores)."""
    S["ultimo"] = {"c": c, "estado": "abriendo", "msg": "", "t": time.time()}
    try:
        r = str(do(c))
    except Exception as e:
        r = "ERROR: %r" % (e,)
    S["ultimo"] = {"c": c, "estado": "error" if r.startswith("ERROR") else "listo", "msg": r, "t": time.time()}


def minimizar_auto(motivo):
    """Minimiza: con video sonando -> barra de audio; si no -> pildora minima para poder volver."""
    try:
        m = S["conn"].val(META_JS, 2) if S["conn"] and S["conn"].alive else None
        mj = json.loads(m) if m else {}
    except Exception:
        mj = {}
    if mj.get("has") and not mj.get("paused"):
        save_cfg({"mini_modo": "bar"})
    else:
        S["pill"] = True
    log(motivo, "→", do("mini"))


ALIAS = {"type": "escribir", "keyboard": "teclado", "reload": "recargar", "level1": "nivel1", "level2": "nivel2",
         "quality": "calidad", "key": "tecla", "page": "pagina", "capture": "captura"}


def do(cmd):
    _p = cmd.split(" ", 1)
    if _p[0] in ALIAS:
        cmd = ALIAS[_p[0]] + (" " + _p[1] if len(_p) > 1 else "")
    if cmd.startswith("vol game"):
        cmd = "vol juego" + cmd[8:]
    if cmd == "perf":
        return perf()
    if cmd == "ping":
        return "pong"
    if cmd == "ultimo":  # resultado de la última apertura asíncrona (sin tomar LOCK: open puede tardar segundos)
        return json.dumps(S.get("ultimo") or {}, ensure_ascii=False)
    with LOCK:
        if cmd == "status":
            ok = view_alive()
            s = state(S["conn"], 4) if ok else None
            return json.dumps({"dfl": bool(S["dfl"]), "vista": ok, "reescritura": REWRITE["on"], "modal": modal_open() if S["dfl"] else False,
                               "peticiones_reescritas": dict(stats), "pagina": s}, ensure_ascii=False)
        if cmd in ("open", "toggle"):
            if cmd == "toggle" and S["dfl"] and modal_open():
                S["dfl"].val(CLOSE_JS, 4)
                set_mode("none")
                return "closed"
            err = ensure_view()
            if err:
                return "ERROR: " + err
            S["dfl"].val(CLOSE_JS, 4)
            S["dfl"].val(REMOVE_MINI_JS, 4)
            calidad_ventana()
            r = S["dfl"].val(show_js(), 8)
            quitar_tarjeta()
            if r == "ok":
                set_mode("full")
                threading.Thread(target=push_game, daemon=True).start()
            return "open" if r == "ok" else "ERROR: " + str(r)
        if cmd == "mini":
            err = ensure_view()
            if err:
                return "ERROR: " + err
            _c = load_cfg()
            if _c.get("mini_calidad", "medium") != "auto":
                aplicar_calidad("tiny" if _c.get("mini_modo") == "bar" else _c.get("mini_calidad", "medium"))
            r = S["dfl"].val(mini_js(), 8)
            quitar_tarjeta()
            if r != "ok":
                return "ERROR: " + str(r)
            set_mode("mini")
            return "mini card active"
        if cmd in ("nivel1", "nivel2"):
            save_cfg({"mini_nivel": int(cmd[-1])})
            if S["dfl"] and S["dfl"].val("!!window.__bvmini", 3) is True:
                S["dfl"].val(mini_js(), 8)
            return "card level over games = " + cmd[-1]
        if cmd == "fs":
            if not (S["dfl"] and modal_open()):
                return "ERROR: open the modal first"
            on = S["dfl"].val("(()=>{window.__bvfs=!window.__bvfs;return window.__bvfs})()", 3)
            calidad_ventana()
            return "fullscreen " + ("yes" if on else "no")
        if cmd == "tecla" or cmd.startswith("tecla "):
            if not S["conn"]:
                return "ERROR: no view"
            k = cmd[5:].strip().lower()
            teclas = {"up": ("ArrowUp", 38), "down": ("ArrowDown", 40), "left": ("ArrowLeft", 37), "right": ("ArrowRight", 39),
                      "enter": ("Enter", 13), "back": ("Escape", 27), "pgup": ("PageUp", 33), "pgdn": ("PageDown", 34)}
            if k not in teclas:
                return "usage: key <%s>" % "|".join(teclas)
            key, vk = teclas[k]
            ev = {"key": key, "code": key, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk}
            S["conn"].call("Input.dispatchKeyEvent", dict(ev, type="rawKeyDown"), 2)
            S["conn"].call("Input.dispatchKeyEvent", dict(ev, type="keyUp"), 2)
            return "key " + k
        if cmd == "pagina":
            if not S["conn"]:
                return "ERROR: no view"
            return str(S["conn"].val(PAGINA_JS, 4))
        if cmd == "trace":
            if not S["dfl"]:
                return "ERROR: no Decky"
            return str(S["dfl"].val("JSON.stringify((window.__bvtr||[]).slice(-60))", 3))
        if cmd.startswith("calidad"):
            if not S["conn"]:
                return "ERROR: no view"
            q = cmd[7:].strip()
            if q and q not in ("auto", "fit", "tiny", "small", "medium", "large", "hd720", "hd1080"):
                return "usage: quality [auto|fit|tiny|small|medium|large|hd720|hd1080]  (tiny=144p small=240p medium=360p large=480p; fit = highest that fits the view)"
            return str(S["conn"].val(CAL_JS.replace("__Q__", q), 4))
        if cmd == "eventos":
            if not S["dfl"]:
                return "ERROR: no Decky"
            return str(S["dfl"].val(EVT_JS, 3))
        if cmd == "azul":
            if not S["dfl"]:
                return "ERROR: no Decky"
            return str(S["dfl"].val(AZUL_JS, 3))
        if cmd == "geo":
            if not S["dfl"]:
                return "ERROR: no Decky"
            S["dfl"].val("(()=>{try{Promise.resolve(window.__bv.m_browserView.GetBounds()).then(x=>{window.__bvb=JSON.stringify(x)})}catch(e){window.__bvb=String(e)}return 0})()", 3)
            time.sleep(0.3)
            return str(S["dfl"].val(MINI_GEO_JS, 4)) + " vista_nativa=" + str(S["dfl"].val("window.__bvb", 3)) + " sobre_juego_gancho=" + str(S["dfl"].val("window.__bvch", 3)) + " err=" + str(S["dfl"].val("window.__bvcherr||''", 3)) + " qam=" + str(S["dfl"].val("JSON.stringify({doc:!!window.__bvqd,vis:window.__bvqd&&window.__bvqd.visibilityState,w:window.__bvqw,err:window.__bvqerr||null,arboles:window.__bvtrees||null,cur:window.__bvqcur,ca:window.__bvca,caerr:window.__bvcaerr||null,info:window.__bvqinfo||null,api:typeof DFL.getGamepadNavigationTrees})", 3)) + " pantalla=" + str(S["dfl"].val("JSON.stringify(window.__bvfst||null)", 3))
        if cmd == "unmini":
            if S["dfl"]:
                S["dfl"].val(REMOVE_MINI_JS, 4)
            set_mode("none")
            return "mini card removed"
        if cmd == "pp":
            return str(S["conn"].val(PP_JS, 3)) if S["conn"] else "ERROR: no view"
        if cmd == "setb":
            d = S["dfl"]
            if not d:
                return "ERROR: no Decky"
            rd = "(()=>{try{Promise.resolve(window.__bv.m_browserView.GetBounds()).then(x=>{window.__bvb=JSON.stringify(x)})}catch(e){window.__bvb=String(e)}return 0})()"
            def leer():
                d.val(rd, 3)
                time.sleep(0.4)
                return str(d.val("window.__bvb", 3))
            antes = leer()
            objetivo = d.val("(()=>{const w=window.__bvmwrap;if(!w)return null;const r=w.getBoundingClientRect();return JSON.stringify([r.x,r.y,r.width,r.height])})()", 3)
            if not objetivo:
                return "ERROR: no mini card in video mode (use 'mini' first). before=" + antes
            a = d.val("(()=>{const [x,y,w,h]=JSON.parse(%s);try{window.__bv.m_browserView.SetBounds(x,y,w,h);return 'ok'}catch(e){return String(e)}})()" % json.dumps(objetivo), 3)
            r1 = leer()
            r2 = ""
            if r1 == antes:
                b = d.val("(()=>{const [x,y,w,h]=JSON.parse(%s);try{window.__bv.m_browserView.SetBounds({x:x,y:y,width:w,height:h});return 'ok'}catch(e){return String(e)}})()" % json.dumps(objetivo), 3)
                r2 = " | forma objeto: " + str(b) + " -> " + leer()
            return "objetivo=%s | antes=%s | forma (x,y,w,h): %s -> %s%s" % (objetivo, antes, a, r1, r2)
        if cmd == "mic":
            if not S["conn"]:
                return "ERROR: no view"
            out = ["permiso: " + grant_mic()]
            S["conn"].val("window.__ytmmic='';0", 2)
            S["conn"].call("Runtime.evaluate", {"expression": MIC_JS, "awaitPromise": True, "returnByValue": True}, 15)
            out.append("página: " + str(S["conn"].val("window.__ytmmic", 3)))
            return " | ".join(out)
        if cmd == "bvopts":
            return str(S["dfl"].val(BVOPTS_JS, 6)) if get_dfl() else "ERROR: no Decky"
        if cmd == "teclado":
            return str(S["dfl"].val(KB_JS, 4)) if get_dfl() else "ERROR: no Decky"
        if cmd == "audio":
            import subprocess
            res = {}
            try:
                d = get_dfl()
                d.val(AUDIO_JS, 3)
                time.sleep(0.5)
                res["steam"] = str(d.val("window.__bva", 3))
            except Exception as e:
                res["steam"] = "fallo %r" % (e,)
            try:
                o = subprocess.run(["pactl", "-f", "json", "list", "sink-inputs"], capture_output=True, text=True, timeout=5)
                arr = json.loads(o.stdout or "[]")
                names = {}
                try:
                    sk = subprocess.run(["pactl", "-f", "json", "list", "sinks"], capture_output=True, text=True, timeout=5)
                    names = {x.get("index"): x.get("name") for x in json.loads(sk.stdout or "[]")}
                except Exception:
                    pass
                res["flujos"] = [{"id": x.get("index"), "destino": names.get(x.get("sink"), x.get("sink")), "app": (x.get("properties") or {}).get("application.name"),
                                  "bin": (x.get("properties") or {}).get("application.process.binary"),
                                  "vol%": [v.get("value_percent") for v in (x.get("volume") or {}).values()][:1],
                                  "pausado": x.get("corked")} for x in arr]
                if o.returncode:
                    res["pactl_error"] = o.stderr[:120]
            except Exception as e:
                res["flujos"] = "pactl no disponible: %r" % (e,)
            return json.dumps(res, ensure_ascii=False)
        if cmd.startswith("vol"):
            parts = cmd.split()
            canales = {"steamjuego": "game_output", "steamyoutube": "browser_output", "musica": "music_output", "general": "*def"}
            if len(parts) >= 2 and parts[1] in ("juego", "youtube", "yt"):
                mode, val = "lista", 0
                if len(parts) > 2:
                    v = parts[2]
                    try:
                        mode, val = ("rel", int(v)) if v[0] in "+-" else ("abs", int(v))
                    except ValueError:
                        return "invalid value: " + v
                if parts[1] == "juego":
                    return vol_juego(mode, val)
                return vol_youtube(mode, val)
            if len(parts) == 2 and parts[1] == "todo":
                return " ; ".join(do("vol " + c) for c in ("juego", "youtube", "general"))
            if len(parts) < 2 or parts[1] not in canales:
                return "usage: vol <game|youtube|general|all> [N | +N | -N]   (steamjuego/steamyoutube/musica = Steam channels)"
            mode, val = "lista", 0
            if len(parts) > 2:
                v = parts[2]
                try:
                    mode, val = ("rel", int(v)) if v[0] in "+-" else ("abs", int(v))
                except ValueError:
                    return "invalid value: " + v
            d = get_dfl()
            if not d:
                return "ERROR: no Decky"
            js = VOL_JS.replace("__NOM__", json.dumps(canales[parts[1]])).replace("__MODE__", json.dumps(mode)).replace("__VAL__", str(val))
            d.val(js, 3)
            for _ in range(10):
                time.sleep(0.15)
                r = d.val("window.__bvvol", 3)
                if r:
                    return str(r)
            return "no answer from Steam"
        if cmd.startswith("escribir "):
            if not S["conn"]:
                return "ERROR: no view"
            AE = ("(()=>{const e=document.activeElement;return JSON.stringify({tag:e&&e.tagName,cls:e&&String(e.className).slice(0,40),"
                  "editable:!!(e&&(/^(INPUT|TEXTAREA)$/.test(e.tagName)||e.isContentEditable)),val:e&&String(e.value||e.textContent||'').slice(0,40)})})()")
            antes = str(S["conn"].val(AE, 2))
            # Leanback descarta la primera tecla tras un toque (pasa del modo puntero al de teclado): una tecla neutra la "despierta".
            S["conn"].call("Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": "Shift", "code": "ShiftLeft", "windowsVirtualKeyCode": 16}, 2)
            S["conn"].call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Shift", "code": "ShiftLeft", "windowsVirtualKeyCode": 16}, 2)
            time.sleep(0.25)
            for ch in cmd[9:]:
                if ch.isalpha():
                    code, vk = "Key" + ch.upper(), ord(ch.upper())
                elif ch.isdigit():
                    code, vk = "Digit" + ch, ord(ch)
                elif ch == " ":
                    code, vk = "Space", 32
                else:
                    code, vk = "", 0
                ev = {"key": ch, "code": code, "windowsVirtualKeyCode": vk, "nativeVirtualKeyCode": vk}
                S["conn"].call("Input.dispatchKeyEvent", dict(ev, type="keyDown", text=ch, unmodifiedText=ch), 2)
                S["conn"].call("Input.dispatchKeyEvent", dict(ev, type="keyUp"), 2)
            time.sleep(0.2)
            medio = str(S["conn"].val(AE, 2))
            extra = ""
            if '"editable":true' in medio and medio == antes:
                S["conn"].call("Input.insertText", {"text": cmd[9:]}, 2)
                time.sleep(0.2)
                extra = " | tras insertText=" + str(S["conn"].val(AE, 2))
            return "foco antes=%s | despues=%s%s" % (antes, medio, extra)
        if cmd == "bvapi":
            return str(S["dfl"].val(BVAPI_JS, 6)) if get_dfl() else "ERROR: no Decky"
        if cmd == "diag":
            return str(S["conn"].val(DIAG_JS, 6)) if S["conn"] else "ERROR: no view"
        if cmd == "inspect":
            return str(S["dfl"].val(INSPECT_JS, 5)) if get_dfl() else "ERROR: no Decky"
        if cmd == "targets":
            return json.dumps([{"tipo": t.get("type"), "titulo": (t.get("title") or "")[:40],
                                "destino": "%s://%s" % (urlparse(t.get("url", "")).scheme, urlparse(t.get("url", "")).hostname or "")}
                               for t in tabs()], ensure_ascii=False)
        if cmd in ("shot", "captura"):
            import base64, zipfile
            carpeta = os.path.join(ROOT, "capturas", time.strftime("%Y%m%d_%H%M%S"))
            os.makedirs(carpeta, exist_ok=True)
            indice = []
            try:
                lista = tabs()
            except Exception as e:
                return "ERROR: CEF not responding: %r" % e
            for n, t in enumerate(lista):
                if t.get("type") != "page" or not t.get("webSocketDebuggerUrl"):
                    continue
                es_vista = t["id"] == S.get("vid")
                u = t.get("url", "")
                es_ui = ("createflags=" in u and "browserviewpopup" not in u)
                if not (es_vista or es_ui):
                    continue
                propia = None
                try:
                    c = S["conn"] if (es_vista and S["conn"] and S["conn"].alive) else Conn(t["webSocketDebuggerUrl"])
                    propia = c is not S["conn"]
                    r = c.call("Page.captureScreenshot", {"format": "png"}, timeout=8)
                    data = (r.get("result") or {}).get("data")
                    dim = c.val("[innerWidth,innerHeight,devicePixelRatio,document.visibilityState]", 3)
                    if data:
                        nombre = "%02d_%s.png" % (n, "vista_youtube" if es_vista else "ventana_steam")
                        open(os.path.join(carpeta, nombre), "wb").write(base64.b64decode(data))
                    else:
                        nombre = None
                    indice.append({"archivo": nombre, "tipo": "vista_youtube" if es_vista else "ventana_steam", "titulo": (t.get("title") or "")[:50],
                                   "ruta": urlparse(t.get("url", "")).path[:60], "ventana_y_visibilidad": dim,
                                   "error": None if data else str(r.get("error") or r)[:80]})
                except Exception as e:
                    indice.append({"archivo": None, "tipo": "vista_youtube" if es_vista else "ventana_steam", "error": repr(e)[:80]})
                finally:
                    if propia:
                        c.close()
            if S["dfl"]:
                try:
                    indice.append({"tarjeta_mini": S["dfl"].val(MINI_GEO_JS, 3), "estado_ui": S["dfl"].val("JSON.stringify(window.__bvui||null)", 3)})
                except Exception:
                    pass
            json.dump(indice, open(os.path.join(carpeta, "indice.json"), "w"), indent=1, ensure_ascii=False)
            zp = carpeta + ".zip"
            with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
                for f in sorted(os.listdir(carpeta)):
                    z.write(os.path.join(carpeta, f), f)
            return "capturas: %d imagen(es) -> %s" % (sum(1 for i in indice if i.get("archivo")), zp)
        if cmd == "recargar":
            c = S["conn"]
            if not (c and c.alive):
                return "ERROR: no active view"
            if S.get("sid"):
                c.call("Page.removeScriptToEvaluateOnNewDocument", {"identifier": S["sid"]})
            CFGV.clear()
            CFGV.update(load_cfg())
            arm(c)
            r = c.call("Page.addScriptToEvaluateOnNewDocument", {"source": page_js()})
            S["sid"] = (r.get("result") or {}).get("identifier")
            c.call("Page.reload")
            return "config reloaded: " + json.dumps(CFGV, ensure_ascii=False)
        if cmd in ("aopen", "atoggle", "amini"):
            threading.Thread(target=_trabajo, args=(cmd[1:],), daemon=True).start()
            return "running"
        if cmd == "close":
            if S["dfl"]:
                S["dfl"].val(CLOSE_JS, 4)
            set_mode("none")
            return "closed"
        if cmd == "stop":
            try:
                try:
                    if S["conn"]:
                        S["conn"].val(PAUSE_JS, 3)
                except Exception:
                    pass
                if S["dfl"]:
                    S["dfl"].val(REMOVE_MINI_JS, 4)
                    S["dfl"].val(DESTROY_JS, 4)
                if S["conn"]:
                    disarm(S["conn"])
            finally:
                threading.Timer(0.5, lambda: os._exit(0)).start()
            return "stopped (view destroyed, UA restored)"
        return "unknown command: " + cmd


def poll():
    """Atiende los botones tactiles de la interfaz (modal/tarjeta) que dejan una peticion en window.__bvreq."""
    n = 0
    while True:
        time.sleep(0.4)
        n += 1
        try:
            d = S["dfl"]
            if not d or not d.alive:
                continue
            req = d.val("(()=>{const r=window.__bvreq||'';window.__bvreq='';return r})()", 2)
            if req.startswith("vol:") and "=" in req:
                k, v = req[4:].split("=", 1)
                try:
                    vv = int(v)
                except ValueError:
                    vv = None
                if vv is not None and k == "yt":
                    vol_youtube("abs", vv)
                elif vv is not None and k == "game":
                    vol_juego("abs", vv)
            elif req == "autobar":
                minimizar_auto("modal cerrado deslizando/fuera del recuadro")
            elif req == "mini":
                log("botón: minimizar →", do("mini"))
            elif req == "full":
                log("botón: ampliar →", do("open"))
            elif req == "pp":
                log("botón: play/pausa →", do("pp"))
            elif req == "stopmini":
                if S["conn"]:
                    S["conn"].val(PAUSE_JS, 3)
                log("botón: cerrar tarjeta →", do("unmini"))
            elif req.startswith("set:") and "=" in req:
                k, v = req[4:].split("=", 1)
                if k in ("mini_esquina", "mini_modo", "mini_ancho"):
                    save_cfg({k: int(v) if k == "mini_ancho" else v})
                    log("guardado", k, "=", v)
            if S["conn"] and S["conn"].alive and n % 3 == 0:
                m = S["conn"].val(META_JS, 2)
                if m:
                    d.val("window.__bvmeta=" + m, 2)
        except Exception as e:
            if time.time() - S.get("pollerr", 0) > 30:
                S["pollerr"] = time.time()
                log("sondeo de botones (se reintenta):", repr(e))


def watch():
    fails = 0
    while True:
        try:
            with LOCK:
                if S["conn"] is None or not view_alive():
                    fails += 1
                    if fails == 1 or fails % 6 == 0:
                        err = ensure_view()
                        if err:
                            log("aún no:", err)
                        else:
                            fails = 0
                else:
                    fails = 0
                    st = state(S["conn"], 3)
                    S["bad"] = 0 if st else S.get("bad", 0) + 1
                    if S["bad"] >= 4 and REWRITE["on"]:
                        log("la vista no responde: desarmo la reescritura por seguridad")
                        disarm(S["conn"])
        except Exception as e:
            log("error en el vigilante:", repr(e))
        time.sleep(5)
