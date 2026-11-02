"""Configuración: constantes, ytmini.json (cargar/guardar), User-Agent de TV y bloqueo de red."""
import json
import os
import re
import time


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # carpeta del proyecto (donde viven ytmini.json, capturas/, ytmini.log)
PORT = 8799


URL = "https://www.youtube.com/tv"


CFG_FILE = os.path.join(ROOT, "ytmini.json")


CFG_DEF = {"adblock": True, "ocultar_shorts": False, "sin_pausa_inactividad": True, "ocultar_barras": True,
           "zoom": 1.0, "bloqueo_red": False, "modal": "normal",
           "botones": "pagina", "mini_esquina": "abajo-derecha", "mini_modo": "video", "mini_ancho": 420, "mini_margen": 16, "mini_margen_inferior": 64, "mini_nivel": 1, "mini_calidad": "medium", "ventana_calidad": "ajustada", "mini_mover_tactil": True, "mini_shorts": False,
           "fix_filas": True, "cdp_network": False, "fetch_solo_documento": False}


BLOCK_RE = re.compile(r"^https://([^/]+\.)?(doubleclick\.net|googlesyndication\.com|googleadservices\.com)/"
                                     r"|^https://www\.youtube\.com/(pagead/|api/stats/ads|ptracking)")


BLOCK_PATTERNS = ["https://*.doubleclick.net/*", "https://*.googlesyndication.com/*", "https://*.googleadservices.com/*",
                  "https://www.youtube.com/pagead/*", "https://www.youtube.com/api/stats/ads*", "https://www.youtube.com/ptracking*"]


def load_cfg():
    cfg = dict(CFG_DEF)
    try:
        cfg.update(json.load(open(CFG_FILE)))
    except FileNotFoundError:
        try:
            json.dump(CFG_DEF, open(CFG_FILE, "w"), indent=2, ensure_ascii=False)
        except Exception:
            pass
    except Exception as e:
        print("ytmini.json ilegible, uso valores por defecto:", e, flush=True)
    return cfg


YEAR, COBALT, FULL, B = time.gmtime().tm_year, "27.lts.3.1040976-gold", "27.lts.3", "SteamMiniTube"


UA = ("Mozilla/5.0 (X11; Linux x86_64) Cobalt/%s (unlike Gecko) v8/13.8.258.54-jit gles Starboard/18, "
      "%s_DESKTOP_x8664_%d/0.1 (%s, Linux) steamminitube/0.1") % (COBALT, B, YEAR, B)


META = {"brands": [{"brand": B, "version": "27"}], "fullVersionList": [{"brand": B, "version": FULL}],
        "fullVersion": FULL, "platform": "Starboard", "platformVersion": "", "architecture": "x86", "model": "",
        "mobile": False, "bitness": "64", "wow64": False}


def save_cfg(upd):
    try:
        cur = json.load(open(CFG_FILE))
    except Exception:
        cur = {}
    cur.update(upd)
    json.dump(cur, open(CFG_FILE, "w"), indent=2, ensure_ascii=False)
