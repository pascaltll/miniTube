"""Medición de consumo (CPU, GPU, vatios) para el comando perf."""
import collections
import json
import os
import time


def _leer_pids():
    out = {}
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            st = open("/proc/%s/stat" % pid).read()
            rp = st.rindex(")")
            f = st[rp + 2:].split()
            t = int(f[11]) + int(f[12])
            cmd = open("/proc/%s/cmdline" % pid, "rb").read().replace(b"\0", b" ").decode("utf8", "replace")
            name = st[st.index("(") + 1:rp]
            if "steamwebhelper" in name or "steamwebhelper" in cmd:
                import re as _re
                m = _re.search(r"--type=([a-z-]+)", cmd)
                name = "steamwebhelper:" + (m.group(1) if m else "main")
            elif "ytmini_tv" in cmd:
                name = "ytmini-daemon"
            out[pid] = (name, t)
        except Exception:
            continue
    return out


def _watts():
    try:
        for d in sorted(os.listdir("/sys/class/power_supply")):
            b = "/sys/class/power_supply/" + d
            if open(b + "/type").read().strip() != "Battery":
                continue
            try:
                return int(open(b + "/power_now").read()) / 1e6
            except Exception:
                return int(open(b + "/current_now").read()) * int(open(b + "/voltage_now").read()) / 1e12
    except Exception:
        pass
    return None


def _gpu():
    try:
        for d in sorted(os.listdir("/sys/class/drm")):
            p = "/sys/class/drm/%s/device/gpu_busy_percent" % d
            if os.path.exists(p):
                return int(open(p).read())
    except Exception:
        pass
    return None


def perf(secs=6):
    """CPU por proceso, GPU y vatios de bateria durante unos segundos (para ver el coste de cada modo)."""
    hz = os.sysconf("SC_CLK_TCK")
    a = _leer_pids()
    watts, gpus = [], []
    t0 = time.time()
    while time.time() - t0 < secs:
        w, g = _watts(), _gpu()
        if w is not None:
            watts.append(w)
        if g is not None:
            gpus.append(g)
        time.sleep(0.5)
    dt = time.time() - t0
    b = _leer_pids()
    agg = collections.Counter()
    for pid, (name, t) in b.items():
        if pid in a:
            agg[name] += (t - a[pid][1]) / hz / dt * 100
    top = [(n, round(v)) for n, v in agg.most_common(7) if v >= 1]
    res = {"cpu_%_de_un_nucleo": top, "total_cpu_%": round(sum(agg.values())),
           "gpu_%": round(sum(gpus) / len(gpus)) if gpus else None,
           "bateria_W": round(sum(watts) / len(watts), 1) if watts else None, "segundos": round(dt, 1)}
    return json.dumps(res, ensure_ascii=False)
