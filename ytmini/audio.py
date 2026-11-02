"""Volumen: YouTube (video.volume en la página) y juego (pactl sobre sink-inputs)."""
import json
from .core import S


def vol_juego(mode, val):
    """Volumen del juego: flujos de audio de aplicaciones que no son Steam (misma idea que usa Hooandee: pactl sobre sink-inputs)."""
    import subprocess
    try:
        o = subprocess.run(["pactl", "-f", "json", "list", "sink-inputs"], capture_output=True, text=True, timeout=5)
        arr = json.loads(o.stdout or "[]")
    except Exception as e:
        return "pactl no disponible: %r" % (e,)
    fl = []
    for x in arr:
        pr = x.get("properties") or {}
        if pr.get("application.process.binary") in ("steamwebhelper", "steam"):
            continue
        if str(pr.get("node.name", "")).startswith("effect_") or not pr.get("application.name") or str(pr.get("application.process.binary", "")).startswith("opengamepad-ui"):
            continue
        pc = [int(str(c.get("value_percent", "100")).rstrip("%") or 100) for c in (x.get("volume") or {}).values() if isinstance(c, dict)]
        fl.append((x.get("index"), pr.get("application.name"), max(pc) if pc else 100))
    if not fl:
        return json.dumps({"canal": "juego", "flujos": 0, "nota": "no hay flujos de audio de un juego ahora mismo"}, ensure_ascii=False)
    out = []
    for idx, app, cur in fl:
        if mode == "lista":
            out.append({"app": app, "vol": cur})
            continue
        t = max(0, min(100, cur + val if mode == "rel" else val))
        r = subprocess.run(["pactl", "set-sink-input-volume", str(idx), "%d%%" % t], capture_output=True, text=True, timeout=5)
        out.append({"app": app, "antes": cur, "despues": t, "ok": r.returncode == 0})
    return json.dumps({"canal": "juego", "flujos": out}, ensure_ascii=False)


def vol_youtube(mode, val):
    """Volumen de YouTube: el del elemento video dentro de la pagina (0-100)."""
    if not S["conn"]:
        return "ERROR: no hay vista"
    js = ("(()=>{const v=document.querySelector('video');if(!v)return JSON.stringify({canal:'youtube',nota:'sin video'});const a=Math.round(v.volume*100);"
          "const m=%s,x=%d;if(m!=='lista'){const t=Math.max(0,Math.min(100,m==='rel'?a+x:x));v.volume=t/100;v.muted=false}"
          "return JSON.stringify({canal:'youtube',antes:a,despues:Math.round(v.volume*100)})})()") % (json.dumps(mode), val)
    return str(S["conn"].val(js, 3))


def push_game():
    """Deja en window.__bvgame el volumen del juego (o -1 si no hay flujo de juego) para la barra del modal."""
    val = -1
    try:
        r = json.loads(vol_juego("lista"))
        fl = r.get("flujos")
        if isinstance(fl, list) and fl:
            val = max(int(x["vol"]) for x in fl)
    except Exception:
        pass
    try:
        if S["dfl"]:
            S["dfl"].val("window.__bvgame=%d" % val, 2)
        if S["conn"] and S["conn"].alive:
            S["conn"].val("window.__ytmGame=%d;0" % val, 2)
    except Exception:
        pass
