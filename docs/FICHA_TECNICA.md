# MiniTube (ytmini) — Ficha técnica

Cómo funciona, qué se descubrió y **qué está verificado y qué no**. Para instalar y usar, ver `README.md`.
Convención: **[V]** verificado en la máquina de Carlos o por salida de un comando · **[H]** hipótesis sin comprobar · **[X]** descartado.

## 1. Resumen de arquitectura

```
 launcher.sh ──► ytmini_tv.py ──► ytmini.main
      │                              │  (demonio: systemd-run --user, fuera del árbol del atajo)
      ▼                              ▼
 Steam (CEF :8080) ◄──CDP──  ytmini/  ──► 127.0.0.1:8799 (órdenes: open|close|mini|vol …)
  ├─ pestaña SharedJSContext  (DFL, SP_REACT)   ← aquí se ejecuta modal.js / mini.js
  ├─ vista propia (BrowserView)  = YouTube TV   ← aquí se inyecta page.js
  └─ QuickAccess (QAM), MainMenu, notificaciones…
```

- El programa es un **demonio Python** que habla CDP (WebSocket) con dos objetivos del CEF de Steam: la pestaña de **Decky/SharedJSContext** (para crear y colocar la vista y los componentes React) y la **pestaña de YouTube** de la vista (para inyectar controles, reescribir User-Agent y leer el estado).
- No es un fork de VacuumTube (Electron): comparte solo la idea Leanback + User-Agent de TV. Arquitectura propia.

## 2. Flujo de arranque (`do("open")`)

1. `get_dfl()` encuentra la pestaña de Decky y ejecuta `probe.js` (ubica `DFL`, `SP_REACT` y `BrowserContainer`).
2. `make_view()` carga una vista nueva con `data:text/plain,<id>` para localizar su target CDP, luego `LoadURL("https://www.youtube.com/tv")`.
3. `attach()` abre CDP a esa pestaña: `Page.enable`, `Runtime.enable`, `Runtime.addBinding`, `arm()` (User-Agent) y `Page.addScriptToEvaluateOnNewDocument(page.js)`.
4. Se espera a Leanback (`state.js`: ruta `/tv` y >100 nodos). Si la vista cambia de target se reconecta.
5. Se muestra el modal (`modal.js`) o la tarjeta mini (`mini.js`).

## 3. Canales de comunicación

| Canal | Sentido | Detalle |
|---|---|---|
| CDP `Runtime.evaluate` | demonio → Steam/página | `Conn.val(js)`; bajo `LOCK` |
| `console.debug('__ytmcmd__'+cmd@ts)` + `Runtime.consoleAPICalled` | página → demonio | **Canal real de órdenes de la página** [V]: `window.ytminiCmd` (binding) llega `undefined` tras la carga. Por eso `Runtime.enable` es imprescindible |
| `window.__bvreq` (sondeo `poll()`) | UI de Steam → demonio | botones táctiles del modal/tarjeta |
| Socket `127.0.0.1:8799` | terminal → demonio | `launcher.sh <orden>` → `client()` → `do()` |
| Cola `CMDQ` + `cmd_worker()` | página → demonio | serializa las órdenes: `mini`, `full`, `bar`, `size`, `pp`, `vgopen`, `vg:NN`, `swbar`… |

## 4. Hallazgos verificados

### 4.1 Vista, ventana y persistencia
- [X] `NavigateToExternalWeb`: ventana transitoria, se cierra con el menú de Steam y corta el audio.
- [V] **BrowserView propia** (`GamepadUIMainWindowInstance.CreateBrowserView`) + `BrowserContainer` en un modal de Decky: persiste con el modal cerrado, con el menú de Steam abierto y dentro de un juego (audio siguió; video avanzó 50,1 s en 50,1 s).
- [V] `BrowserContainer` necesita la clase `ExternalBrowserContainer` (`findClassModule`) o se ve vacío.
- [V] `BrowserContainer` reserva una banda de ~40 px arriba y recorta la vista nativa. La vista expone `SetBounds(x,y,w,h)` (px CSS), `GetBounds()`, `SetVisible`, `SetFocus`. Solución: vigilar el hueco cada 40–60 ms y llamar `SetBounds` solo si cambia; verificar con `GetBounds` cada 1 s.
- [V] Pantalla completa: `SetBounds(0,0,innerWidth,innerHeight)` de la ventana **donde está el modal** (`wrapper.ownerDocument.defaultView`), no del contexto 1×1 de Decky.
- [V] La vista nativa se dibuja **siempre por encima** del DOM de Steam: los controles sobre el video viven dentro de la página de YouTube (`#ytm-ov`).
- [V] Había una imagen de fondo del `BrowserContainer` (clase `Rz1j`) que asomaba como destello azul; se elimina con `background-image:none` (confirmado con `azul`).

### 4.2 User-Agent y carga de Leanback
- [V] Solo `Fetch.enable` + `Fetch.continueRequest` con la cabecera `User-Agent` reescrita cambia el UA **real en la red**; `Emulation/Network.setUserAgentOverride` no. Con eso `/tv` devuelve Leanback real. **Por eso `Fetch.enable` no puede quitarse.** (`fetch_solo_documento` es una prueba opcional, no verificada.)
- [V] Flag `enable_touch_support` inyectada vía `window.environment` (idea de VacuumTube, MIT): activa el scroll táctil nativo.
- [V] Se fuerza `document.hidden=false` / `visibilityState=visible` y se bloquean `visibilitychange`/`pagehide` para que no se pause.

### 4.3 Entrada
- [V] `Focusable` con `onGamepadFocus` → `BChildTakeFocus()` + `m_browserView.SetFocus(true)`; luego `SteamClient.Input.ControllerKeyboardSetKeyState` (HID 79 der, 80 izq, 81 abajo, 82 arriba, 88 enter, 41 esc) llega como teclas reales. Cruceta, A, B y scroll táctil funcionaron.
- [V] Los toques sí llegan a la página (`isTrusted`; pointer/touch/mouse/click).
- [V] `diag` mostró que las filas de Leanback son elementos `yt-virtual-list` con `overflow-x:auto` (v47, 2026-11-02).

### 4.4 Sobre juegos y composición
- [V] Gancho `AddMinimumCompositionStateRequest` (hallado con `findModuleChild` por el código de la función; misma idea que decky-steam-pip y Hooandee). **Nivel 1** (Notification) solo dibuja: toque y mando van al juego. **Nivel 2** (Overlay) acepta toques pero quita el mando al juego.
- [V] Con el QAM abierto la tarjeta se puede arrastrar.

### 4.5 QAM
- [V] La ventana se halla con `DFL.getGamepadNavigationTrees()` (árbol cuyo id empieza por `QuickAccess`); visible = `doc.visibilityState==='visible'`; ancho del panel medido: **351 px**. La tarjeta se aparta con `translateX` animado a 16 ms y `SetBounds` en la misma pasada (confirmado suave).
- [V] Bug corregido: `qamW()` cacheaba un elemento erróneo (ancho 0 con el QAM visible); ahora se vuelve a buscar cuando da 0.

### 4.6 Audio y medidas
- [V] Volumen YouTube = `video.volume` en la página (instantáneo). Volumen del juego = `pactl` sobre *sink-inputs* que no son Steam (2 procesos por orden; el JS limita a 1 orden cada 300 ms).
- [V] Latencia toque→orden ≈ 15–45 ms (medido en versiones anteriores).
- [V] Micrófono: la página ve 2 entradas pero `getUserMedia` da `NotAllowedError`; `Browser.grantPermissions` no sirve (sin contexto / «Failed to find browser context»). Búsqueda por voz **no disponible**; usar teclado.

### 4.7 Red
- [V] `error code -7` en la vista = timeout de red al cargar `youtube.com/tv`. Con `curl` YouTube respondía (200 en 3 s) y al **reiniciar el sistema** volvió a funcionar. La causa raíz no se identificó.
- [V] Un proceso suspendido con **Ctrl+Z** conserva el puerto 8799 (`Address already in use`) y `stop` no responde. Usar `launcher.sh kill`.

## 5. Dominios CDP: qué se activa y por qué

| Llamada | Estado | Motivo |
|---|---|---|
| `Runtime.enable` + `addBinding` | **necesaria** | canal de órdenes por consola (§3) |
| `Fetch.enable` (Document, XHR, Fetch de `youtube.com`) | **necesaria** | reescribir User-Agent (§4.2) |
| `Page.enable`, `Emulation.setFocusEmulationEnabled` | activas | scripts en documento nuevo y emulación de foco |
| `Network.enable` | **opcional** (`cdp_network`, apagada desde v47) | ningún código lee eventos `Network.*`; el efecto de quitarla sobre CPU/latencia **no está medido** [H] |
| `Network.setBypassServiceWorker` | activa | motivo supuesto [H]: que un service worker no responda sin pasar por la red (no se probó quitarla) |

Estimaciones de ahorro de energía o latencia de análisis externos **no cuentan como medidas**. Para medir: pulsar mini 5 veces y comparar las líneas `tiempos …: toque→cola` del log, más `perf` antes/después.

## 6. Estados de la interfaz

| Estado | Implementación |
|---|---|
| Normal / Completa | modal de Decky (`showModal`) con `BrowserContainer`; `modal: completo` usa `position:fixed` a pantalla completa |
| Mini video | componente global `routerHook.addGlobalComponent('ytmini-mini', Mini)`; marco de 6 px (22 arriba) arrastrable, la vista nativa cubre el interior |
| Mini audio (barra) | ancho fijo 380×56; calidad `tiny` (144p) |
| Píldora | `mode:'pill'`, 60×34 px, icono expandir; toque corto (<10 px, <700 ms) → `__bvreq='full'`; también se pinta sobre juegos |

`minimizar_auto()` decide: si hay video y no está en pausa → `mini_modo:"bar"` (se guarda en `ytmini.json`); si no → píldora.

## 7. Calidad de video

`CAL_JS` usa `movie_player.setPlaybackQualityRange(q,q)`. `aplicar_calidad(q, retardos)` corre en un hilo: mini video = `medium` (360p), barra = `tiny`; clave `mini_calidad` (`"auto"` la desactiva).

**Problema observado por Carlos (2026-11-02, v48):** al pasar de mini a ventana normal o pantalla completa el video se quedaba en baja resolución. Causa **[H]**: `auto` solo pone el rango `tiny..highres` (un permiso, no una orden) y la adaptación de YouTube sube despacio y puede quedarse abajo; además la calidad depende del tamaño de la vista y esta cambia con retraso. **Cambio v49:** `ventana_calidad` (`"ajustada"` por defecto) fija, tras la animación de tamaño (0,4 s, 1,5 s y 4 s), la calidad más baja disponible cuyo alto ≥ 90 % del alto físico de la vista (`innerHeight × devicePixelRatio`): en pruebas con un reproductor simulado, vista 607×369 @2,13 → 720p; 902×508 @2,13 → 1080p; mini 420×236 → 480p. Aún **sin verificar en YouTube real**: comprobar con `./launcher.sh calidad` (`actual`, `video:[w,h]`). Fija la calidad (no hay adaptación a red lenta); `"auto"` restaura el comportamiento anterior.

**[H]** Que la calidad reducida alivie los tirones del juego no está medido.

## 8. Gestos y estado de verificación (v45–v48)

| Función | Estado |
|---|---|
| Deslizar dentro del video (franja superior) | [V] funciona con animación |
| Deslizar fuera del video (marco) con eventos táctiles | [H] reescrito en v45 por `pointercancel` en táctil; pendiente de confirmar |
| Dos dedos hacia abajo en cualquier punto | [H] v46, sin probar |
| Tocar fuera ya no minimiza | [H] guardia en `closeModal` (v44); a veces con dos toques cerraba |
| Píldora (minimizar sin video) | [H] v46 |
| Modo control sobre un juego (7 s, aro azul, captor de gamepad) | [H] `geo` muestra `ca:1` (captor registrado); **sin probar en juego real**. Riesgo: quitar el mando al juego |
| `fix_filas` | [V] confirmado por Carlos (2026-11-02, v48): el scroll con el dedo sobre las filas ya funciona; `diag` → `rowfix` listó 3 `yt-virtual-list` con desborde de 8–9 px (alto 186–190 px) |
| Arrastre táctil en el modo mover (`mini_mover_tactil`) | [H] v49: el video se oculta mientras dura el modo para que la tarjeta entera reciba el dedo (la vista nativa está por encima del DOM y se quedaba con los toques); sin probar |
| Parpadeo al terminar el modo control (nivel 2→1) | [H] causa supuesta; abierto |
| Tirones del juego con mini video | [H] decodificación 1080p + composición nivel 1; abierto |

Detalle del gesto del modal: eventos en el documento del modal (`__bvwrap.ownerDocument`), zona muerta 36 px, `dx<dy*0.7`, suelta con dy>90 (o dy>40 y v>0,5) → `__bvreq='autobar'`. Perro guardián de 700 ms contra estados atascados. En la página (`mode 'full'`): un dedo desde `clientY<120` y >90 px abajo, o dos dedos (`SW2`) → orden `swbar`.

## 9. Scroll de Leanback con el dedo

- Leanback está pensado para mando: mueve la pantalla al cambiar el foco con flechas; el scroll nativo solo aparece con `enable_touch_support`.
- **Causa del «mini scroll»** [V: `rowfix` mostró filas con 8–9 px de desborde; el arreglo lo resolvió]: una fila (`yt-virtual-list`, `overflow` propio) con desborde vertical de unos píxeles se queda con el gesto táctil (Chrome fija el contenedor al empezar el gesto), así que el arrastre que empieza sobre una fila no llega a la lista principal. Un arrastre que empieza entre filas sí.
- **Mitigación v47** (`fix_filas`): en `touchstart`, a los ancestros con scroll vertical de desborde ≤ max(80 px, 30 % de su alto) se les pone `overflow-y:hidden`. La lista principal (desborde grande) no se toca. `diag` → `rowfix` lista lo tocado.
- **Plan B** (no hizo falta; queda por si Leanback cambia): traducir el arrastre a teclas ↑↓←→ (como hace VacuumTube con la rueda: `keydown` simulado con `keyCode` sobre `document`, freno de 100 ms).
- VacuumTube además pone `overflow:hidden` a `yt-virtual-list` y `.ogHbMc` cuando la última entrada **no** fue táctil (clase `vt-touch-input` en `<html>`); aquí no se aplica porque la lista principal también es `yt-virtual-list`.
- `zoom` no influye: Leanback fija su escala con `font-size` del `html` según el tamaño de la ventana.

## 10. Comandos de diagnóstico

| Comando | Qué muestra |
|---|---|
| `doctor` | dependencias, JSON, CEF, demonio, red (en el lanzador) |
| `diag` | CSS cargado, overlay, últimos eventos, elementos desplazables, `rowfix` |
| `geo` | geometría de la tarjeta, vista nativa, QAM (`w`, `ca` = captor de mando) |
| `trace` | rastro del mini (`__bvtr`) para ver desfases |
| `azul` | qué elementos hay detrás de la tarjeta (`elementsFromPoint`) |
| `eventos` | 40 últimos eventos del documento del modal/mini |
| `perf` | CPU por proceso, GPU, vatios, durante 6 s |
| `calidad [q]` | fuerza o consulta la calidad |
| `bvapi`, `bvopts`, `inspect`, `targets`, `mic`, `audio`, `setb`, `shot` | exploración de la API de Steam, objetivos CEF, micrófono, audio, zip de capturas |

## 11. Reglas de seguridad del proyecto

- **Nunca** `Storage.clearDataForOrigin` ni borrar cookies/almacenamiento de `youtube.com`.
- No imprimir valores de cookies ni tokens.
- Código de GPL-3.0 (DeckWebBrowser, Hooandee): solo ideas, no copiar.
- Conservar el aviso MIT de VacuumTube si se copia código suyo.

## 12. Mapa del código (generado del propio código en v48)

**`config.py`** — Configuración: constantes, ytmini.json (cargar/guardar), User-Agent de TV y bloqueo de red.
- `load_cfg()`
- `save_cfg()`

**`core.py`** — Estado compartido entre módulos (diccionarios mutables, cola de órdenes, cerrojo, log). Sin lógica.
- `log()`

**`cdp.py`** — Cliente CDP (Chrome DevTools Protocol) hacia el CEF de Steam: conexión, reescritura de User-Agent (Fetch), pestañas.
- `Conn`
- `on_paused()`
- `arm()`
- `disarm()`
- `tabs()`
- `is_browser_tab()`
- `wait_tab()`
- `find_dfl()`
- `state()`

**`steam.py`** — Lado Steam/Decky: crear y mantener la BrowserView, adjuntar la pestaña de YouTube, modo de controles, JS inyectado.
- `aplicar_calidad()` — Baja (o restaura) la calidad de YouTube en segundo plano: la tarjeta pequeña no necesita 1080p.
- `get_dfl()`
- `view_alive()`
- `on_binding()`
- `set_mode()` — Modo de los controles dentro de la pagina de YouTube: full | mini | none (solo si botones=pagina).
- `page_js()`
- `show_js()`
- `mini_js()`
- `attach()`
- `grant_mic()` — Concede el microfono al contexto de navegacion de la vista (el permiso por defecto no le llega).
- `make_view()`
- `ensure_view()` — Devuelve None si la vista esta lista; si no, un texto con el motivo.
- `modal_open()`

**`audio.py`** — Volumen: YouTube (video.volume en la página) y juego (pactl sobre sink-inputs).
- `vol_juego()` — Volumen del juego: flujos de audio de aplicaciones que no son Steam (misma idea que usa Hooandee: pactl sobre sink-inputs).
- `vol_youtube()` — Volumen de YouTube: el del elemento video dentro de la pagina (0-100).
- `push_game()` — Deja en window.__bvgame el volumen del juego (o -1 si no hay flujo de juego) para la barra del modal.

**`metrics.py`** — Medición de consumo (CPU, GPU, vatios) para el comando perf.
- `_leer_pids()`
- `_watts()`
- `_gpu()`
- `perf()` — CPU por proceso, GPU y vatios de bateria durante unos segundos (para ver el coste de cada modo).

**`commands.py`** — Orden central do(): todos los comandos, cola de órdenes de la página, sondeos y vigilante.
- `cmd_worker()`
- `minimizar_auto()` — Minimiza: con video sonando -> barra de audio; si no -> pildora minima para poder volver.
- `do()`
- `poll()` — Atiende los botones tactiles de la interfaz (modal/tarjeta) que dejan una peticion en window.__bvreq.
- `watch()`

**`server.py`** — Servidor local 127.0.0.1:PORT, consola (run), demonio (serve) y cliente (órdenes desde otra terminal).
- `H`
- `Srv`
- `run()`
- `serve()` — Sin consola (para launcher.sh / systemd): servidor + vigilante; SIGTERM limpia la vista.
- `client()`

**`js/`** — texto exacto inyectado por CDP (los marcadores `__CFG__`, `__UI__`, `%s`… los rellena Python):
`page.js` (YouTube: adblock, overlay, gestos, volumen), `modal.js` (modal y gesto de minimizar), `mini.js` (tarjeta, píldora, QAM, modo control) y utilidades: `probe`, `create`, `open`, `state`, `meta`, `cal`, `pp`, `pause`, `close`, `destroy`, `remove_mini`, `vol`, `audio`, `kb`, `mic`, `diag`, `mini_geo`, `azul`, `evt`, `bvapi`, `bvopts`, `inspect`.

Estado compartido (en `core.py`): `S` (conexiones y vista), `CFGV` (config activa), `REWRITE`, `stats`, `CMDQ`, `LOCK` (RLock que serializa las llamadas a Steam).

## 13. Pendientes conocidos

- Confirmar en el dispositivo las filas de §8 que siguen marcadas [H] (gestos fuera del video, dos dedos, píldora, modo control sobre juego).
- Medir `Network.enable` (con `cdp_network` true/false) y `fetch_solo_documento`.
- Posibles mejoras de rendimiento (sin medir): `qamW`/sincronización del mini con `ResizeObserver`, evitar el recorrido `querySelectorAll`+`getComputedStyle` cada 40 ms en `modal.js`, sacar `ensure_view`/`vol`/`escribir` del `LOCK`.
- Reiniciar el estado `S["pill"]` si `do("mini")` falla (riesgo bajo); borrar el código muerto `swDown/swMove/swUp`.
- Ideas: SponsorBlock, DeArrow, Return YouTube Dislike, ocultar Shorts, filtro de códecs, atajos de velocidad/subtítulos, búsqueda con yt-dlp, teclado en pantalla dentro de la página.

## 14. Historial

| Versión | Cambios |
|---|---|
| v36–v44 | volumen (panel y fila horizontal), QAM suave, azul del fondo, transición barra→video, gesto de minimizar, `mini_calidad`, modo control |
| v45 | gesto del modal con eventos táctiles (causa: `pointercancel`) |
| v46 | gesto de dos dedos, píldora |
| v47 | `fix_filas`, `Network.enable` opcional, `fetch_solo_documento`, aviso de página de error |
| **v49** | `ventana_calidad` (calidad ajustada al volver de mini), `mini_mover_tactil` (arrastre con el dedo en el modo mover), `calidad fit` |
| **v48** (confirmado en el dispositivo: instalación, `doctor`, arranque en 1 s, scroll de filas) | **reestructuración en paquete `ytmini/` + `js/`; lanzador con `doctor`/`kill`/`install`; README; arte para Steam. Sin cambios de comportamiento: las 42 funciones y las 25 plantillas JS son idénticas a v47, salvo el texto de un aviso** |

## Novedades 0.50 (resumen técnico)
- **Cierre:** la X de la página envía `stop` al demonio: pausa (`PAUSE_JS`), quita el mini, destruye la vista (`DESTROY_JS`), restaura el UA y sale.
- **Estado de apertura:** `ultimo` devuelve `{c, estado, msg, t}`; el lanzador lo sondea para mostrar avisos de error. `ping` se atiende fuera de `LOCK`.
- **Tarjeta de carga** (`load.js`, componente global de Decky) y splash en la página (`#ytm-splash`).
- **Modelo de interacción del mini (experimental):** con juego abierto y QAM cerrado, el mini pide nivel 1 (solo dibuja); con QAM abierto, nivel 2 (táctil). Detección de juego: `SteamUIStore.MainRunningAppID` (`window.__bvgame`, sin verificar en dispositivo). Con el QAM abierto se registra `SetCatchAllGamepadInput`, que deja pasar todo salvo Izquierda cuando el foco del QAM (`.gpfocus`) está en la franja izquierda (columna principal): entonces `__bvpf=1` y el mini consume la cruceta (mover), A, L1/R1 (tamaño) y B (salir). Al abrir/cerrar el QAM se suelta el foco.
- **Shorts:** `pagina` vuelca ruta, vídeo (`videoWidth/Height`), estado y foco; `tecla` envía `Input.dispatchKeyEvent` (verificado: `up/down` cambian de Short). En mini con vídeo vertical, botones ▲▼ (`kup/kdown`); `mini_shorts` activa el recuadro vertical (experimental).
- **Informes:** `report.py` (Markdown local con datos ocultados), `crash.py` (excepthook, threading.excepthook, faulthandler → `crashes/`).
- **Actualización:** `update.py` aplica un zip o la última release de GitHub, con copia en `respaldos/`, protección contra zip-slip y conservación de `ytmini.json`, `.venv` y registros.
