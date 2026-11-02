"""Plantillas JS que se inyectan en Steam y en la página de YouTube (carpeta js/).
Cada archivo es el texto exacto que se envía por CDP; los marcadores (__CFG__, __UI__, %s, ...) los rellena Python."""
import os

_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "js")


def _load(nombre):
    with open(os.path.join(_DIR, nombre), encoding="utf-8") as f:
        return f.read().rstrip("\n")


AUDIO_JS = _load("audio.js")
AZUL_JS = _load("azul.js")
BVAPI_JS = _load("bvapi.js")
BVOPTS_JS = _load("bvopts.js")
CAL_JS = _load("cal.js")
CLOSE_JS = _load("close.js")
CREATE_JS = _load("create.js")
DESTROY_JS = _load("destroy.js")
DIAG_JS = _load("diag.js")
EVT_JS = _load("evt.js")
INSPECT_JS = _load("inspect.js")
KB_JS = _load("kb.js")
META_JS = _load("meta.js")
MIC_JS = _load("mic.js")
MINI_GEO_JS = _load("mini_geo.js")
MINI_JS = _load("mini.js")
OPEN = _load("open.js")
PAGE_JS = _load("page.js")
PAUSE_JS = _load("pause.js")
PP_JS = _load("pp.js")
PROBE_JS = _load("probe.js")
REMOVE_MINI_JS = _load("remove_mini.js")
SHOW_JS = _load("modal.js")
STATE = _load("state.js")
VOL_JS = _load("vol.js")
LOAD_JS = _load("load.js")
REMOVE_LOAD_JS = _load("remove_load.js")
PAGINA_JS = _load("pagina.js")
