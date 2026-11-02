(()=>{try{if(window.__ytm)return;window.__ytm={keys:[],ev:{}};
const CFG=__CFG__;
const cnt=n=>{window.__ytm.ev[n]=(window.__ytm.ev[n]||0)+1};
const def=(o,p,v)=>{try{Object.defineProperty(o,p,{configurable:true,get:()=>v})}catch(e){}};
def(Document.prototype,'hidden',false);def(Document.prototype,'visibilityState','visible');def(Document.prototype,'webkitHidden',false);
['visibilitychange','webkitvisibilitychange','pagehide','freeze'].forEach(n=>{
 window.addEventListener(n,e=>e.stopImmediatePropagation(),true);document.addEventListener(n,e=>e.stopImmediatePropagation(),true);});
let env;Object.defineProperty(window,'environment',{configurable:true,get(){return env},set(v){
 try{v.flags=Object.assign(v.flags||{},{enable_touch_support:true})}catch(e){}env=v}});
const rec=e=>{cnt(e.type);if(e.type==='keydown'||e.type==='keyup'){const k=window.__ytm.keys;k.push([e.type,e.keyCode,e.key||'',e.isTrusted?1:0]);if(k.length>40)k.shift();}};
['keydown','keyup','wheel','touchstart','touchmove','pointerdown','scroll'].forEach(n=>window.addEventListener(n,rec,{capture:true,passive:true}));
/* filtros de contenido (idea de VacuumTube, MIT; implementacion propia) */
const shortsTitle=r=>{try{return r.shelfRenderer.headerRenderer.shelfHeaderRenderer.avatarLockup.avatarLockupRenderer.title.runs[0].text}catch(e){return null}};
const cleanShelves=list=>{if(!Array.isArray(list))return list;
 const out=list.filter(r=>{if(!r)return true;
  if(CFG.adblock&&(r.adSlotRenderer||r.promoShelfRenderer))return false;
  if(CFG.ocultar_shorts&&shortsTitle(r)==='Shorts')return false;return true;});
 if(CFG.adblock)for(const r of out){const h=r&&r.shelfRenderer&&r.shelfRenderer.content&&r.shelfRenderer.content.horizontalListRenderer;
  if(h&&Array.isArray(h.items))h.items=h.items.filter(i=>!(i&&i.adSlotRenderer));}
 return out;};
const sectionList=j=>{const c=j.contents;
 return (j.continuationContents&&j.continuationContents.sectionListContinuation)||
  (c&&c.tvBrowseRenderer&&c.tvBrowseRenderer.content&&c.tvBrowseRenderer.content.tvSurfaceContentRenderer&&c.tvBrowseRenderer.content.tvSurfaceContentRenderer.content&&c.tvBrowseRenderer.content.tvSurfaceContentRenderer.content.sectionListRenderer)||
  (c&&c.sectionListRenderer)||null;};
const jp=JSON.parse;
JSON.parse=function(...a){const j=jp.apply(this,a);
 try{if(j&&typeof j==='object'){
  if(CFG.adblock){if(j.adPlacements)j.adPlacements=[];if(j.adSlots)j.adSlots=[];
   if(Array.isArray(j.entries))j.entries=j.entries.filter(e=>!(e&&e.command&&e.command.reelWatchEndpoint&&e.command.reelWatchEndpoint.adClientParams&&e.command.reelWatchEndpoint.adClientParams.isAd));}
  const sl=sectionList(j);if(sl&&sl.contents)sl.contents=cleanShelves(sl.contents);
  if(CFG.sin_pausa_inactividad&&j.playabilityStatus&&Array.isArray(j.messages)){j.messages=j.messages.filter(m=>!(m&&m.youThereRenderer));if(!j.messages.length)delete j.messages;}
 }}catch(e){}
 return j;};
/* interfaz tactil: sin barras de desplazamiento visibles + escala */
const css=[];
if(CFG.ocultar_barras)css.push('*::-webkit-scrollbar{display:none!important;width:0!important;height:0!important}*{scrollbar-width:none!important}');
if(CFG.zoom&&CFG.zoom!==1)css.push('html{zoom:'+CFG.zoom+'}');
css.push('*{overscroll-behavior:auto!important}');
const addCss=()=>{const st=document.createElement('style');st.id='ytm-css';st.textContent=css.join('\n');(document.head||document.documentElement).appendChild(st);};
if(css.length){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',addCss);else addCss();}
/* controles superpuestos DENTRO de la pagina de YouTube (la vista nativa tapa cualquier boton dibujado por Steam) */
const PATHS={kb:'M20 5H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zM11 8h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zM7 13H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z',play:'M8 5v14l11-7z',pause:'M6 5h4v14H6zM14 5h4v14h-4z',close:'M19 6.4 17.6 5 12 10.6 6.4 5 5 6.4 10.6 12 5 17.6 6.4 19 12 13.4 17.6 19 19 17.6 13.4 12z',
 expand:'M4 4h6v2H6v4H4zm10 0h6v6h-2V6h-4zM4 14h2v4h4v2H4zm14 0h2v6h-6v-2h4z',note:'M9 3v11.2A3.5 3.5 0 1 0 11 17.5V7h5V3z',
 up:'M7.4 15.4 12 10.8l4.6 4.6L18 14l-6-6-6 6z',down:'M7.4 8.6 12 13.2l4.6-4.6L18 10l-6 6-6-6z',
 more:'M6 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm6 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm6 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z',
 spk:'M3 9v6h4l5 5V4L7 9H3zm13.5 3A4.5 4.5 0 0 0 14 8v8a4.5 4.5 0 0 0 2.5-4zM14 3.2v2.1a7 7 0 0 1 0 13.4v2.1a9 9 0 0 0 0-17.6z',game:'M21 6H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3.5a1 1 0 0 0 .8-.4L9 15h6l1.7 2.6a1 1 0 0 0 .8.4H21a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1zM9 11H8v1H7v-1H6v-1h1V9h1v1h1zm6 1.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm2.5-2a1 1 0 1 1 0-2 1 1 0 0 1 0 2z',size:'M3 15h2v4h4v2H3zM15 3h6v6h-2V5h-4z',pip:'M10 4v6H4V8h4V4zm4 0h2v4h4v2h-6zM4 14h6v6H8v-4H4zm10 0h6v2h-4v4h-2z'};
const OV={open:false,t:0,vol:false,vt:0};let ov=null,lastKey='';let SL=null,lastVg=0;
const svgIcon=(d)=>{const NS='http://www.w3.org/2000/svg',s=document.createElementNS(NS,'svg');s.setAttribute('width','20');s.setAttribute('height','20');s.setAttribute('viewBox','0 0 24 24');
 s.style.cssText='display:block;fill:#fff;pointer-events:none';const p=document.createElementNS(NS,'path');p.setAttribute('d',d);s.appendChild(p);return s;};
const mkBtn=(c,d)=>{const b=document.createElement('div');b.setAttribute('data-c',c);
 b.style.cssText='width:38px;height:38px;border-radius:19px;background:rgba(14,20,27,.42);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.22);opacity:.9;display:flex;align-items:center;justify-content:center;flex:none';
 b.appendChild(svgIcon(d));return b;};
const sendCmd=c=>{const L=(window.__ytm.cmdlog=window.__ytm.cmdlog||[]);L.push([c,typeof window.ytminiCmd]);if(L.length>12)L.shift();c=c+'@'+Date.now();if(typeof window.ytminiCmd==='function'){try{window.ytminiCmd(c);return}catch(e){}}console.debug('__ytmcmd__'+c)};
let lastAct=0;
const inOv=e=>{try{return !!(ov&&e.target&&ov.contains(e.target))}catch(x){return false}};
const act=e=>{const b=e.target.closest&&e.target.closest('[data-c]');if(!b)return;const now=Date.now();if(now-lastAct<350)return;lastAct=now;
 const c=b.getAttribute('data-c');try{b.style.opacity='.45';setTimeout(()=>{try{b.style.opacity=''}catch(x){}},180)}catch(x){}if(c==='more'){OV.open=!OV.open;OV.t=Date.now();lastKey='';buildOv();return}if(c==='vol'){OV.vol=!OV.vol;OV.vt=Date.now();OV.t=OV.vt;if(OV.vol)sendCmd('vgopen');lastKey='';buildOv();return}if(OV.open)OV.t=Date.now();sendCmd(c)};
['pointerdown','pointerup','mousedown','mouseup','touchstart','touchend','click','keydown'].forEach(n=>window.addEventListener(n,e=>{try{const L=(window.__ytm.allev=window.__ytm.allev||[]);const t=(e.touches&&e.touches[0])||(e.changedTouches&&e.changedTouches[0])||e;L.push([n,Math.round(t.clientX||0),Math.round(t.clientY||0),(e.target&&(e.target.id||e.target.tagName))||'?',e.isTrusted]);if(L.length>14)L.shift()}catch(x){}},true));
let SW=null,swEl=null,hintEl=null;
const hint=(on)=>{if(!hintEl){hintEl=document.createElement('div');hintEl.style.cssText='position:fixed;left:50%;top:6px;width:44px;height:4px;margin-left:-22px;border-radius:2px;background:rgba(255,255,255,.55);box-shadow:0 0 4px rgba(0,0,0,.5);z-index:2147483647;pointer-events:none;display:none';(document.body||document.documentElement).appendChild(hintEl)}hintEl.style.display=on?'block':'none'};
const swShow=(dy)=>{if(!swEl){swEl=document.createElement('div');swEl.style.cssText='position:fixed;left:50%;top:0;width:64px;height:30px;margin-left:-32px;border-radius:0 0 16px 16px;background:rgba(14,20,27,.45);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.22);border-top:0;display:none;z-index:2147483647;pointer-events:none;align-items:center;justify-content:center';swEl.appendChild(svgIcon(PATHS.note));(document.body||document.documentElement).appendChild(swEl)}
 if(dy<=0){swEl.style.display='none';return}swEl.style.display='flex';swEl.style.transform='translateY('+Math.min(dy*0.6,80)+'px)';swEl.style.opacity=String(Math.min(1,dy/70))};
let SW2=null;
const avgY=e=>(e.touches[0].clientY+e.touches[1].clientY)/2,avgX=e=>(e.touches[0].clientX+e.touches[1].clientX)/2;
window.addEventListener('touchstart',e=>{try{if(window.__ytmMode!=='full'||inOv(e))return;
 if(e.touches.length===2){SW=null;SW2={x:avgX(e),y:avgY(e),dy:0};return}
 if(e.touches.length!==1)return;const t=e.touches[0];SW=(t.clientY<120)?{x:t.clientX,y:t.clientY}:null}catch(x){}},true);
window.addEventListener('touchmove',e=>{try{
 if(SW2&&e.touches.length>=2){const dy=avgY(e)-SW2.y,dx=Math.abs(avgX(e)-SW2.x);SW2.dy=dx<dy*0.8?dy:0;swShow(SW2.dy);return}
 if(!SW)return;const t=e.touches[0];const dy=t.clientY-SW.y,dx=Math.abs(t.clientX-SW.x);swShow(dx<dy*0.8?dy:0)}catch(x){}},true);
window.addEventListener('touchend',e=>{try{
 if(SW2){const d=SW2.dy;SW2=null;swShow(0);if(d>90)sendCmd('swbar');return}
 if(!SW)return;const t=e.changedTouches[0];const dy=t.clientY-SW.y,dx=Math.abs(t.clientX-SW.x);SW=null;swShow(0);if(dy>90&&dx<dy*0.8)sendCmd('swbar')}catch(x){}},true);
window.addEventListener('touchcancel',()=>{SW=null;SW2=null;try{swShow(0)}catch(x){}},true);
/* v47: filas con scroll propio. Un arrastre vertical que empieza sobre una fila se quedaba con su desborde minimo (unos px) y no llegaba a la lista principal.
   Al tocar, a los ancestros con scroll vertical de desborde pequeno se les quita el scroll vertical (la lista principal tiene desborde grande y no se toca). Desactivar: "fix_filas": false */
window.addEventListener('touchstart',e=>{try{if(!CFG.fix_filas)return;let el=e.target;const L=(window.__ytm.rowfix=window.__ytm.rowfix||[]);
 for(let i=0;el&&el.nodeType===1&&i<14;i++,el=el.parentElement){if(el.__rf)continue;const s=getComputedStyle(el);
  if(!/(auto|scroll|overlay)/.test(s.overflowY))continue;const ex=el.scrollHeight-el.clientHeight;
  if(ex>1&&ex<=Math.max(80,el.clientHeight*0.3)){el.__rf=1;el.style.setProperty('overflow-y','hidden','important');if(L.length<12)L.push([el.tagName.toLowerCase(),String(el.className).slice(0,40),ex,el.clientHeight])}}}catch(x){}},{capture:true,passive:true});
const setVal=(e)=>{try{const r=SL.tr.getBoundingClientRect();const hz=SL.tr._hz;const f=hz?(e.clientX-r.left)/r.width:1-(e.clientY-r.top)/r.height;const v=Math.round(Math.max(0,Math.min(1,f))*100);if(hz){SL.tr._fill.style.width=v+'%';SL.tr._th.style.left=v+'%'}else{SL.tr._fill.style.height=v+'%';SL.tr._th.style.bottom=v+'%'}OV.vt=Date.now();OV.t=OV.vt;SL.v=v;
 if(SL.k==='yt'){const el=document.querySelector('video');if(el){el.volume=v/100;el.muted=false}}else{const n=Date.now();if(n-lastVg>300){lastVg=n;sendCmd('vg:'+v)}}}catch(x){}};
const endSl=()=>{if(SL&&SL.k==='game'&&SL.v!=null)sendCmd('vg:'+SL.v);if(SL)window.__ytmGameV=SL.k==='game'?SL.v:window.__ytmGameV;SL=null};
['pointermove','pointerup','pointercancel','touchmove','touchend'].forEach(n=>window.addEventListener(n,e=>{if(!SL)return;e.stopImmediatePropagation();if(n==='pointermove')setVal(e);else if(n==='pointerup'||n==='pointercancel')endSl()},true));
['pointerdown','pointerup','pointercancel','mousedown','mouseup','touchstart','touchend','touchmove','click'].forEach(n=>window.addEventListener(n,e=>{
 if(!inOv(e))return;if(n==='pointerdown'){const t=e.target.closest&&e.target.closest('[data-s]');if(t){SL={tr:t,k:t.getAttribute('data-s'),v:null};try{t.setPointerCapture(e.pointerId)}catch(x){}setVal(e)}}const o=(window.__ytm.ovev=window.__ytm.ovev||{});o[n]=(o[n]||0)+1;e.stopImmediatePropagation();
 if(n==='pointerup'||n==='touchend'||n==='click')act(e)},true));
const volPanel=()=>{const hz=false;const p=document.createElement('div');p.id='ytm-vol';
 p.style.cssText='position:fixed;top:50%;right:8px;transform:translateY(-50%);display:flex;flex-direction:'+(hz?'column':'row')+';gap:'+(hz?'2px':'4px')+';padding:'+(hz?'4px 10px':'10px 6px 8px')+';border-radius:22px;background:rgba(14,20,27,.42);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.22)';
 const mk=(k,icon,val)=>{const col=document.createElement('div');col.style.cssText=hz?'display:flex;flex-direction:row;align-items:center;gap:8px;height:32px':'display:flex;flex-direction:column;align-items:center;gap:8px;width:34px';
  const tr=document.createElement('div');tr.setAttribute('data-s',k);tr._hz=hz;tr.style.cssText=hz?'position:relative;width:130px;height:32px;touch-action:none':'position:relative;width:34px;height:130px;touch-action:none';
  const rail=document.createElement('div');rail.style.cssText=hz?'position:absolute;top:13px;left:0;right:0;height:6px;border-radius:3px;background:rgba(255,255,255,.22);pointer-events:none':'position:absolute;left:14px;top:0;bottom:0;width:6px;border-radius:3px;background:rgba(255,255,255,.22);pointer-events:none';
  const fill=document.createElement('div');fill.style.cssText=hz?'position:absolute;top:0;bottom:0;left:0;border-radius:3px;background:#fff;width:'+val+'%':'position:absolute;left:0;right:0;bottom:0;border-radius:3px;background:#fff;height:'+val+'%';rail.appendChild(fill);
  const th=document.createElement('div');th.style.cssText=hz?'position:absolute;top:-5px;width:16px;height:16px;border-radius:8px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.5);margin-left:-8px;left:'+val+'%':'position:absolute;left:-5px;width:16px;height:16px;border-radius:8px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.5);margin-bottom:-8px;bottom:'+val+'%';rail.appendChild(th);
  tr.appendChild(rail);tr._fill=fill;tr._th=th;const ic=svgIcon(icon);if(hz){col.appendChild(ic);col.appendChild(tr)}else{col.appendChild(tr);col.appendChild(ic)}return col};
 const v=document.querySelector('video');p.appendChild(mk('yt',PATHS.spk,Math.round(((v&&v.volume)!=null?v.volume:1)*100)));
 const g=window.__ytmGame;if(g!=null&&g>=0)p.appendChild(mk('game',PATHS.game,g));return p};
const volRow=()=>{const p=document.createElement('div');p.id='ytm-vol';
 p.style.cssText='display:flex;gap:8px;align-items:center;height:38px;padding:0 10px;flex:none;border-radius:19px;background:rgba(14,20,27,.42);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.22)';
 const mk=(k,icon,val)=>{const c=document.createElement('div');c.style.cssText='display:flex;align-items:center;gap:6px';c.appendChild(svgIcon(icon));
  const tr=document.createElement('div');tr.setAttribute('data-s',k);tr._hz=true;tr.style.cssText='position:relative;width:64px;height:34px;touch-action:none;flex:none';
  const rail=document.createElement('div');rail.style.cssText='position:absolute;top:14px;left:0;right:0;height:6px;border-radius:3px;background:rgba(255,255,255,.22);pointer-events:none';
  const fill=document.createElement('div');fill.style.cssText='position:absolute;top:0;bottom:0;left:0;border-radius:3px;background:#fff;width:'+val+'%';rail.appendChild(fill);
  const th=document.createElement('div');th.style.cssText='position:absolute;top:-5px;width:16px;height:16px;border-radius:8px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.5);margin-left:-8px;left:'+val+'%';rail.appendChild(th);
  tr.appendChild(rail);tr._fill=fill;tr._th=th;c.appendChild(tr);return c};
 const v=document.querySelector('video');p.appendChild(mk('yt',PATHS.spk,Math.round(((v&&v.volume)!=null?v.volume:1)*100)));
 const g=window.__ytmGame;if(g!=null&&g>=0)p.appendChild(mk('game',PATHS.game,g));return p};
const buildOv=()=>{try{
 if(!document.body)return;try{hint((window.__ytmMode||'none')==='full'&&!SW)}catch(x){}
 if(!ov){ov=document.createElement('div');ov.id='ytm-ov';ov.style.cssText='position:fixed;top:8px;right:8px;z-index:2147483647;display:none;gap:6px;align-items:center';
  document.body.appendChild(ov);}
 const v=document.querySelector('video'),playing=!!(v&&v.currentTime>0.5),mode=window.__ytmMode||'none';
 if(OV.open&&!OV.vol&&Date.now()-OV.t>4000)OV.open=false;
 if(OV.vol&&!SL&&Date.now()-OV.vt>6000){OV.vol=false;OV.t=Date.now()}
 const key=mode+'|'+playing+'|'+OV.open+'|'+(v&&!v.paused)+'|'+OV.vol+'|'+(window.__ytmGame>=0)+'|'+(window.innerHeight<300)+'|'+(v&&v.videoWidth>0&&v.videoHeight>v.videoWidth);if(key===lastKey)return;lastKey=key;
 const items=[];
 if(mode==='full'){if(playing)items.push(['mini',PATHS.pip]);items.push(['vol',PATHS.spk]);items.push(['kb',PATHS.kb]);items.push(['fs',PATHS.expand]);items.push(['close',PATHS.close]);}
 else if(mode==='mini'){if(OV.open)items.push(['vol',PATHS.spk],['size',PATHS.size],['bar',PATHS.note],['full',PATHS.expand],['stopmini',PATHS.close]);
  items.push(['pp',(v&&!v.paused)?PATHS.pause:PATHS.play],['more',PATHS.more]);
  if(v&&v.videoWidth>0&&v.videoHeight>v.videoWidth)items.unshift(['kup',PATHS.up],['kdown',PATHS.down]);}
 while(ov.firstChild)ov.removeChild(ov.firstChild);
 const small=window.innerHeight<300&&OV.vol&&items.some(i=>i[0]==='vol');
 if(small){ov.appendChild(volRow());ov.appendChild(mkBtn('vol',PATHS.close))}else{for(const it of items)ov.appendChild(mkBtn(it[0],it[1]));
 if(OV.vol&&items.some(i=>i[0]==='vol'))ov.appendChild(volPanel())}
 ov.style.display=items.length?'flex':'none';
}catch(e){}};
setInterval(buildOv,400);
/* splash de carga (v50): mientras Leanback arranca se ve un recuadro de marca (mismo estilo que la tarjeta de Steam) que se funde al aparecer contenido */
try{if(location.pathname.indexOf('/tv')===0&&!window.__ytmSplash){window.__ytmSplash=1;const t0=Date.now();let el=null;
 const SVG='<svg viewBox="0 0 64 64" width="64" height="64" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="ytmsg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs><rect x="4" y="8" width="48" height="36" rx="6" fill="#0b0f14" stroke="url(#ytmsg)" stroke-width="3"/><rect x="21" y="29" width="38" height="25" rx="5" fill="url(#ytmsg)"/><path d="M35 35v13l11-6.5z" fill="#fff"/></svg>';
 const done=()=>{if(!el)return;const e=el;el=null;e.style.opacity='0';setTimeout(()=>{try{e.remove()}catch(x){}},420)};
 const chk=()=>{if(!el)return;if(Date.now()-t0>12000||(document.getElementsByTagName('*').length>300&&document.querySelector('ytlr-tile-renderer,ytlr-shelf-renderer,video'))){setTimeout(done,250);return}setTimeout(chk,200)};
 const put=()=>{const de=document.documentElement;if(!de){requestAnimationFrame(put);return}
  el=document.createElement('div');el.id='ytm-splash';
  el.style.cssText='position:fixed;left:0;top:0;right:0;bottom:0;z-index:2147483645;background:radial-gradient(ellipse at 75% 0%,rgba(34,211,238,.13),transparent 55%),radial-gradient(ellipse at 10% 100%,rgba(139,92,246,.14),transparent 55%),#0b0f14;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:sans-serif;transition:opacity .4s ease;pointer-events:none';
  el.innerHTML='<style>@keyframes ytms{0%{left:-45%}100%{left:100%}}@keyframes ytmb{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}</style><div style="animation:ytmb 2.2s ease-in-out infinite">'+SVG+'</div><div style="margin-top:10px;font:700 22px sans-serif;color:#e8ecf4">Mini<span style="background:linear-gradient(90deg,#22d3ee,#8b5cf6);-webkit-background-clip:text;background-clip:text;color:transparent">Tube</span></div><div style="position:relative;width:180px;height:3px;margin-top:16px;border-radius:2px;background:rgba(255,255,255,.1);overflow:hidden"><div style="position:absolute;top:0;height:100%;width:45%;border-radius:2px;background:linear-gradient(90deg,#22d3ee,#8b5cf6);animation:ytms 1.15s ease-in-out infinite"></div></div>';
  de.appendChild(el);chk()};
 put()}}catch(e){}
}catch(e){}})()