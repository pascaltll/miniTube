(()=>{const D=window.DFL,R=window.SP_REACT,h=R.createElement,BC=window.__bvc,b=window.__bv,L=window.DeckyPluginLoader;
if(!BC||!b)return 'faltan piezas';const rh=L&&L.routerHook;
if(!rh||typeof rh.addGlobalComponent!=='function')return 'sin DeckyPluginLoader.routerHook.addGlobalComponent';
try{window.__bvm&&window.__bvm.Close()}catch(e){}window.__bvm=null;
try{rh.removeGlobalComponent('ytmini-mini')}catch(e){}
let CLS='';try{const cm=D.findClassModule(m=>!!m['ExternalBrowserContainer']||!!m['MainBrowserContainer']);CLS=(cm&&cm.ExternalBrowserContainer)||'';}catch(e){}
window.__bvui=Object.assign({},__UI__);const M=__MARG__;const STEAMBTN=__STEAMBTN__;const SIZES=[320,420,560];
const P={play:'M8 5v14l11-7z',pause:'M6 5h4v14H6zM14 5h4v14h-4z',
 close:'M19 6.4 17.6 5 12 10.6 6.4 5 5 6.4 10.6 12 5 17.6 6.4 19 12 13.4 17.6 19 19 17.6 13.4 12z',
 expand:'M4 4h6v2H6v4H4zm10 0h6v6h-2V6h-4zM4 14h2v4h4v2H4zm14 0h2v6h-6v-2h4z',
 note:'M9 3v11.2A3.5 3.5 0 1 0 11 17.5V7h5V3z',
 video:'M4 6h11a1 1 0 0 1 1 1v3.5l4-3v9l-4-3V17a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1z',
 size:'M3 15h2v4h4v2H3zM15 3h6v6h-2V5h-4z',
 more:'M6 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm6 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm6 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4z'};
const Ic=(d,s)=>h('svg',{width:s||20,height:s||20,viewBox:'0 0 24 24',style:{display:'block',fill:'#fff'}},h('path',{d}));
const fmt=s=>{s=Math.max(0,Math.floor(s||0));return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')};
let CH=null;try{CH=D.findModuleChild(m=>{if(typeof m!=='object'||!m)return undefined;for(const k in m){const f=m[k];if(typeof f!=='function')continue;let sc='';try{sc=f.toString()}catch(e){continue}
 if(sc.includes('AddMinimumCompositionStateRequest')&&sc.includes('ChangeMinimumCompositionStateRequest')&&sc.includes('RemoveMinimumCompositionStateRequest')&&!sc.includes('m_mapCompositionStateRequests'))return f}return undefined})}catch(e){window.__bvcherr=String(e)}
window.__bvch=!!CH;
const qamDoc=()=>{try{const now=Date.now();if(window.__bvqd&&window.__bvqd.defaultView)return window.__bvqd;if(now-(window.__bvqdt||0)<250)return null;window.__bvqdt=now;let trees=null;if(typeof D.getGamepadNavigationTrees==='function')trees=D.getGamepadNavigationTrees();
 if(!trees){const c=(window.GamepadNavTree&&window.GamepadNavTree.m_context&&window.GamepadNavTree.m_context.m_controller)||window.FocusNavController;trees=c&&(c.m_rgGamepadNavigationTrees||(c.GetNavigationTrees&&c.GetNavigationTrees()))}
 try{window.__bvtrees=(trees||[]).map(x=>String(x.id||x.m_ID)).slice(0,10)}catch(e){}
 const t=(trees||[]).find(x=>{const id=x.id||x.m_ID;return typeof id==='string'&&id.startsWith('QuickAccess')});const el=t&&((t.m_Root&&t.m_Root.m_element)||(t.Root&&t.Root.Element));
 window.__bvqd=(el&&el.ownerDocument)||null;return window.__bvqd}catch(e){window.__bvqerr=String(e);return null}};
const qamW=()=>{try{const d=qamDoc();if(!d)return 0;const v=d.defaultView;if(!v||d.visibilityState!=='visible')return 0;
 const ok=(el)=>{if(!el||!el.isConnected||el.ownerDocument!==d)return 0;const r=el.getBoundingClientRect();return(r.width>150&&r.left<80)?Math.round(r.right):0};
 let w=ok(window.__bvqel);if(w)return w;
 let el=null,best=0,n=0;for(const e of Array.from(d.querySelectorAll('div'))){const r=e.getBoundingClientRect();if(r.height>=v.innerHeight*0.8&&r.width>150&&r.width<v.innerWidth*0.7&&r.left<80&&r.right>best){best=r.right;el=e}n++}
 window.__bvqel=el;window.__bvqinfo={vw:v.innerWidth,vh:v.innerHeight,n:n,best:Math.round(best)};return ok(el)}catch(e){return 0}};
const inGame=()=>{try{const u=window.SteamUIStore;let g=null;if(u&&typeof u.MainRunningAppID==='number')g=u.MainRunningAppID>0;else if(u&&u.RunningApps&&typeof u.RunningApps.length==='number')g=u.RunningApps.length>0;window.__bvgame=g;return g===true}catch(e){return false}};
const qamMain=()=>{try{const d=qamDoc(),el=window.__bvqel;if(!d||!el)return false;const f=d.querySelector('.gpfocus')||d.activeElement;if(!f||f===d.body)return false;const r=f.getBoundingClientRect(),L=el.getBoundingClientRect().left;return r.width<150&&r.right<=L+110}catch(e){return false}};
const Req=({lv})=>{if(CH)CH(lv||1);return null};
const Mini=()=>{
 const [,tick]=R.useState(0);const [drag,setDrag]=R.useState(null);const ref=R.useRef(null);const [open,setOpen]=R.useState(false);const tm=R.useRef(null);window.__bvqcur=window.__bvqcur||0;
 R.useEffect(()=>{let aid=null;
  const step=()=>{const el=ref.current;if(!el)return;if(window.__bvdrag){clearInterval(aid);aid=null;return}const u=window.__bvui||{};const tgt=(u.corner||'').endsWith('derecha')?(window.__bvqw||0):0;let c=window.__bvqcur;
   if(Math.abs(tgt-c)<0.5){if(c!==tgt){c=tgt;window.__bvqcur=c;el.style.transform=c?'translateX('+(-c)+'px)':'';window.__bvsync&&window.__bvsync()}clearInterval(aid);aid=null;return}
   c+=(tgt-c)*0.3;window.__bvqcur=c;el.style.transform='translateX('+(-c)+'px)';window.__bvsync&&window.__bvsync()};
  const kick=()=>{if(!aid)aid=setInterval(step,16)};
  const poll=setInterval(()=>{const w=qamW();const prev=window.__bvqw||0;if(w!==prev){window.__bvqw=w;kick();window.__bvpf=0;window.__bvctl=0;tick(x=>x+1);if(w===0)setTimeout(window.__bvfocus,150)}},120);
  return()=>{clearInterval(poll);if(aid)clearInterval(aid)}},[]);
 R.useEffect(()=>{const id=setInterval(()=>tick(x=>x+1),1000);return()=>{clearInterval(id);if(tm.current)clearTimeout(tm.current)}},[]);
 const moff=()=>{try{const w=window.__bvmwrap,c=w&&w.firstElementChild;if(!c||drag)return window.__bvmoff||40;const o=Math.round(c.getBoundingClientRect().top-w.getBoundingClientRect().top);if(o>=0&&o<=80){window.__bvmoff=o;return o}}catch(x){}return window.__bvmoff||40};
 const arm=()=>{setOpen(true);if(tm.current)clearTimeout(tm.current);tm.current=setTimeout(()=>setOpen(false),4000)};
 const ui=window.__bvui,meta=window.__bvmeta||{};
 const parts=ui.corner.split('-'),vert=parts[0],horiz=parts[1];
 const pill=ui.mode==='pill';const bar=ui.mode==='bar'||pill;const por=!!M.sh&&!bar&&!!meta.portrait;const PAD=6,TOP=22;const AH=(()=>{try{const w=ref.current&&ref.current.ownerDocument.defaultView;return w?w.innerHeight:429}catch(e){return 429}})();const VH=por?Math.max(120,Math.min(Math.round(ui.w*0.9),AH-TOP-PAD-M.m-M.mb)):Math.round(ui.w*9/16),VW=por?Math.round(VH*9/16):ui.w;const W=pill?60:bar?380:VW+2*PAD,H=pill?34:bar?56:VH+TOP+PAD;
 R.useEffect(()=>{if(bar)return;const v=b.m_browserView;let stop=false,last='',chk=0;const sync=()=>{if(stop)return;const w=window.__bvmwrap;if(!w)return;if(!(Date.now()-(w.__nbT||0)<250)){w.__nbT=Date.now();try{const V=w.ownerDocument.defaultView;w.querySelectorAll('*').forEach(e=>{if(e.getAttribute('data-ytm-ph')==='1')return;const bi=V.getComputedStyle(e).backgroundImage;if(bi&&bi!=='none')e.style.setProperty('background-image','none','important')})}catch(x){}}const r=w.getBoundingClientRect();const t=[r.x,r.y,r.width,r.height];const k=t.map(Math.round).join(',');
  try{if(k!==last){last=k;v.SetBounds(t[0],t[1],t[2],t[3]);chk=Date.now();const T=(window.__bvtr=window.__bvtr||[]);T.push([Math.round(performance.now()),'SetBounds',k]);if(T.length>60)T.shift();return}
   if(Date.now()-chk>1000){chk=Date.now();Promise.resolve(v.GetBounds()).then(c=>{if(stop||!c)return;if(Math.abs(c.x-t[0])>1||Math.abs(c.y-t[1])>1||Math.abs(c.width-t[2])>1||Math.abs(c.height-t[3])>1){v.SetBounds(t[0],t[1],t[2],t[3])}})}}catch(e){}};
  window.__bvsync=sync;window.__bvsync2=()=>{last='';sync()};const id=setInterval(sync,100);sync();const ft=setTimeout(()=>{try{v.SetFocus(true)}catch(e){}},700);return()=>{stop=true;window.__bvsync=null;window.__bvsync2=null;clearInterval(id);clearTimeout(ft)}},[bar]);
 R.useLayoutEffect(()=>{if(window.__bvmwrap)window.__bvmwrap.__nbT=0;window.__bvsync&&window.__bvsync()},[drag]);
 const [fresh,setFresh]=R.useState(false);
 R.useLayoutEffect(()=>{const T=(window.__bvtr=window.__bvtr||[]);const t0=performance.now();T.push([Math.round(t0),'cambio',ui.mode+' w'+ui.w]);let n=0;const rf=()=>{const el=ref.current;if(el){const r=el.getBoundingClientRect();T.push([Math.round(performance.now()),'tarjeta',[r.x,r.y,r.width,r.height].map(Math.round).join(',')])}if(++n<14)requestAnimationFrame(rf);while(T.length>60)T.shift()};requestAnimationFrame(rf);
  if(bar)return;setFresh(true);const ts=[40,110,200,330,500,800].map(ms=>setTimeout(()=>{window.__bvsync2&&window.__bvsync2()},ms));const t=setTimeout(()=>{window.__bvsync2&&window.__bvsync2();setFresh(false)},280);return()=>{clearTimeout(t);ts.forEach(clearTimeout)}},[ui.mode,ui.w,por]);
 const place=drag?{left:drag.x+'px',top:drag.y+'px'}:Object.assign({},vert==='abajo'?{bottom:M.mb+'px'}:{top:M.m+'px'},horiz==='derecha'?{right:M.m+'px'}:{left:M.m+'px'});
 const qam=(window.__bvqw||0)>0,game=inGame();const ctlOn=!!window.__bvpf||Date.now()<(window.__bvctl||0);const locked=game&&!qam&&!ctlOn&&(M.nivel||1)<2;
 window.__bvfocus=()=>{try{b.m_browserView.SetFocus(true)}catch(e){}};
 window.__bvctlbtn=(btn)=>{if(!window.__bvpf)window.__bvctl=Date.now()+7000;
  if(btn===2){window.__bvctl=0;window.__bvpf=0;tick(x=>x+1);setTimeout(window.__bvfocus,150);return}
  if(btn===1){window.__bvreq='pp';return}
  if(btn>=9&&btn<=12){const pr=ui.corner.split('-');let v=pr[0],hh=pr[1];if(btn===9)v='arriba';else if(btn===10)v='abajo';else if(btn===11)hh='izquierda';else hh='derecha';ui.corner=v+'-'+hh;window.__bvqcur=0;if(ref.current)ref.current.style.transform='';window.__bvreq='set:mini_esquina='+ui.corner;tick(x=>x+1);return}
  if(btn===7||btn===8){const i=SIZES.indexOf(ui.w);ui.w=SIZES[(i+(btn===8?1:SIZES.length-1))%SIZES.length];window.__bvreq='set:mini_ancho='+ui.w;tick(x=>x+1)}};
 R.useEffect(()=>{if(!ctlOn&&!qam)return;let reg=null;try{const c=(window.GamepadNavTree&&window.GamepadNavTree.m_context&&window.GamepadNavTree.m_context.m_controller)||window.FocusNavController;
  if(c&&typeof c.SetCatchAllGamepadInput==='function'){reg=c.SetCatchAllGamepadInput((btn,down,rep)=>{if(btn===27||btn===28)return false;window.__bvlastbtn=btn;if(window.__bvpf||(!(window.__bvqw>0)&&Date.now()<(window.__bvctl||0))){if(down&&!rep&&window.__bvctlbtn)window.__bvctlbtn(btn);return true}if(window.__bvqw>0&&btn===11&&qamMain()){if(down&&!rep){window.__bvpf=1;window.__bvctl=0;tick(x=>x+1)}return true}return false});window.__bvca=1}else window.__bvca=0}catch(e){window.__bvcaerr=String(e)}
  return()=>{try{reg&&reg.Unregister&&reg.Unregister()}catch(e){}}},[ctlOn,qam]);
 R.useEffect(()=>{if(!ctlOn||window.__bvpf)return;const id=setInterval(()=>{if(Date.now()>=(window.__bvctl||0)){clearInterval(id);tick(x=>x+1);setTimeout(window.__bvfocus,150)}},300);return()=>clearInterval(id)},[ctlOn]);
 const down=(e)=>{const el=ref.current;if(!el)return;const r=el.getBoundingClientRect();window.__bvqcur=0;el.style.transform='';el.style.left=r.x+'px';el.style.top=r.y+'px';el.style.right='auto';el.style.bottom='auto';window.__bvdrag={px:e.clientX,py:e.clientY,x:r.x,y:r.y};try{e.currentTarget.setPointerCapture(e.pointerId)}catch(x){}};
 const move=(e)=>{const st=window.__bvdrag;if(!st)return;setDrag({x:st.x+e.clientX-st.px,y:st.y+e.clientY-st.py});};
 const up=(e)=>{const st=window.__bvdrag;window.__bvdrag=null;if(!st)return;const el=ref.current,w=el&&el.ownerDocument.defaultView;
  const vw=w?w.innerWidth:900,vh=w?w.innerHeight:500,cx=st.x+e.clientX-st.px+W/2,cy=st.y+e.clientY-st.py+H/2;const fw=vw-(window.__bvqw||0);
  ui.corner=(cy<vh/2?'arriba':'abajo')+'-'+(cx<fw/2?'izquierda':'derecha');{const tg=ui.corner.endsWith('derecha')?(window.__bvqw||0):0;window.__bvqcur=tg;if(el)el.style.transform=tg?'translateX('+(-tg)+'px)':''}setDrag(null);window.__bvreq='set:mini_esquina='+ui.corner;tick(x=>x+1);};
 const Btn=(d,fn)=>h('div',{onClick:(e)=>{e.stopPropagation();fn()},style:{width:'36px',height:'36px',borderRadius:'18px',background:'rgba(255,255,255,.14)',display:'flex',alignItems:'center',justifyContent:'center',flex:'none'}},Ic(d,20));
 const buttons=[
  Btn(meta.paused?P.play:P.pause,()=>{window.__bvreq='pp'}),
  bar?null:Btn(P.size,()=>{const i=SIZES.indexOf(ui.w);ui.w=SIZES[(i+1)%SIZES.length];tick(x=>x+1);window.__bvreq='set:mini_ancho='+ui.w}),
  Btn(bar?P.video:P.note,()=>{ui.mode=bar?'video':'bar';tick(x=>x+1);window.__bvreq='set:mini_modo='+ui.mode}),
  Btn(P.expand,()=>{window.__bvreq='full'}),
  Btn(P.close,()=>{window.__bvreq='stopmini'})];
 const glass={background:'rgba(14,20,27,.4)',backdropFilter:'blur(10px)',WebkitBackdropFilter:'blur(10px)',border:'1px solid rgba(255,255,255,.2)'};
 const G=(d,fn)=>h('div',{onClick:(e)=>{e.stopPropagation();fn()},style:Object.assign({width:'34px',height:'34px',borderRadius:'17px',opacity:.88,display:'flex',alignItems:'center',justifyContent:'center',flex:'none'},glass)},Ic(d,18));
 const vgrip=h('div',{onPointerDown:down,onPointerMove:move,onPointerUp:up,onPointerCancel:up,style:Object.assign({position:'absolute',top:'6px',left:'6px',width:'64px',height:'30px',borderRadius:'15px',
   display:'flex',alignItems:'center',justifyContent:'center',touchAction:'none',opacity:.72},glass)},h('div',{style:{width:'26px',height:'4px',borderRadius:'2px',background:'rgba(255,255,255,.85)'}}));
 const vtitle=h('div',{style:{position:'absolute',top:'8px',left:'78px',right:STEAMBTN?'190px':'10px',height:'26px',color:'#dcdedf',fontSize:'13px',lineHeight:'26px',whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis',pointerEvents:'none'}},meta.title||'');
 const vctl=h('div',{style:{position:'absolute',top:'6px',right:'6px',display:'flex',gap:'6px',alignItems:'center'}},
  ...(!STEAMBTN?[]:open?[G(P.size,()=>{const i=SIZES.indexOf(ui.w);ui.w=SIZES[(i+1)%SIZES.length];tick(x=>x+1);window.__bvreq='set:mini_ancho='+ui.w;arm()}),
   G(P.note,()=>{ui.mode='bar';tick(x=>x+1);window.__bvreq='set:mini_modo=bar'}),
   G(P.expand,()=>{window.__bvreq='full'}),
   G(P.close,()=>{window.__bvreq='stopmini'})]:[]),
  ...(!STEAMBTN?[]:[G(meta.paused?P.play:P.pause,()=>{window.__bvreq='pp';if(open)arm()}),
  G(P.more,()=>{if(open){if(tm.current)clearTimeout(tm.current);setOpen(false)}else arm()})]));
 const title=meta.title||'YouTube';
 const grip=h('div',{onPointerDown:down,onPointerMove:move,onPointerUp:up,onPointerCancel:up,style:{flex:1,height:'100%',display:'flex',alignItems:'center',gap:'10px',padding:'0 10px 0 14px',touchAction:'none',minWidth:0}},
  bar?Ic(P.note,22):h('div',{style:{width:'18px',height:'4px',borderRadius:'2px',background:'rgba(255,255,255,.55)',flex:'none'}}),
  h('div',{style:{minWidth:0,color:'#dcdedf',fontSize:'14px',lineHeight:'18px',whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}},
   title,bar&&meta.d?h('div',{style:{fontSize:'11px',color:'#8b929a'}},fmt(meta.t)+' / '+fmt(meta.d)):null));
 const strip=h('div',{style:{display:'flex',alignItems:'center',gap:'6px',paddingRight:'8px',height:bar?'56px':'48px',
   position:bar?'static':'absolute',top:0,left:0,right:0,zIndex:5,background:bar?'transparent':'linear-gradient(rgba(0,0,0,.72),rgba(0,0,0,0))'}},grip,...buttons);
 const prog=bar&&meta.d?h('div',{style:{position:'absolute',left:0,bottom:0,height:'3px',width:Math.min(100,100*meta.t/meta.d)+'%',background:'#1a9fff'}}):null;
 if(pill){const pd=(e)=>{window.__bvtap={x:e.clientX,y:e.clientY,t:Date.now()};down(e)};
  const pu=(e)=>{const t=window.__bvtap;window.__bvtap=null;if(t&&Math.hypot(e.clientX-t.x,e.clientY-t.y)<10&&Date.now()-t.t<700){window.__bvdrag=null;setDrag(null);window.__bvreq='full';return}up(e)};
  return h('div',{ref:(el)=>{ref.current=el;window.__bvmel=el},onPointerDown:pd,onPointerMove:move,onPointerUp:pu,onPointerCancel:pu,style:Object.assign({position:'fixed',width:'60px',height:'34px',zIndex:7000,borderRadius:'17px',background:'rgba(14,20,27,.82)',border:'1px solid rgba(255,255,255,.22)',display:'flex',alignItems:'center',justifyContent:'center',touchAction:'none',boxShadow:ctlOn?'0 0 0 2px rgba(26,159,255,.9),0 0 18px rgba(26,159,255,.35)':'0 4px 14px rgba(0,0,0,.5)'},place)},
   Ic(P.expand,18),h(Req,{key:'req',lv:locked?1:2}))}
 return h('div',{ref:(el)=>{ref.current=el;window.__bvmel=el},onPointerDownCapture:()=>{if(!window.__bvpf&&Date.now()<(window.__bvctl||0))window.__bvctl=Date.now()+7000},style:Object.assign({position:'fixed',width:W+'px',height:H+'px',zIndex:7000,borderRadius:'14px',overflow:'hidden',
   background:bar?'rgba(14,20,27,.95)':'#0b0f14',opacity:(fresh&&!bar)?0.001:1,transition:'opacity .16s ease-out',border:'1px solid rgba(255,255,255,.16)',boxShadow:ctlOn?'0 0 0 2px rgba(26,159,255,.9),0 0 22px rgba(26,159,255,.35),0 8px 26px rgba(0,0,0,.6)':'0 8px 26px rgba(0,0,0,.6)'},place)},
  bar?null:h('div',{onPointerDown:down,onPointerMove:move,onPointerUp:up,onPointerCancel:up,style:{position:'absolute',left:0,top:0,right:0,bottom:0,touchAction:'none'}},
   h('div',{style:{position:'absolute',top:'9px',left:'50%',marginLeft:'-22px',width:'44px',height:'4px',borderRadius:'2px',background:'rgba(255,255,255,.55)',pointerEvents:'none'}})),
  bar?null:h('div',{ref:(el)=>{window.__bvmwrap=el},style:{position:'absolute',left:PAD+'px',top:TOP+'px',width:VW+'px',height:VH+'px',background:'#000',borderRadius:'8px',overflow:'hidden',pointerEvents:(ctlOn&&M.mt)?'none':'auto'}},h(BC,{browser:b,className:CLS,visible:!drag&&!fresh&&!(ctlOn&&M.mt),hideForModals:true,external:true,displayURLBar:false,autoFocus:false}),((drag||fresh||(ctlOn&&M.mt))?h('div',{'data-ytm-ph':'1',style:{position:'absolute',inset:0,zIndex:3,background:meta.vid?'#000 url(https://i.ytimg.com/vi/'+meta.vid+'/mqdefault.jpg) center/cover':'#000',borderRadius:'8px',filter:'brightness(.55)'}},(ctlOn&&M.mt&&!drag)?h('div',{style:{position:'absolute',left:0,right:0,bottom:'8px',textAlign:'center',font:'600 11px sans-serif',color:'#fff',textShadow:'0 1px 3px #000',pointerEvents:'none'}},'D-pad: move · A pause · L1/R1 size · B back to QAM'):null):null)),
  bar?strip:null,bar?prog:null,(game&&(locked||qam||ctlOn))?h('div',{key:'lk',style:Object.assign({position:'absolute',display:'flex',alignItems:'center',justifyContent:'center',pointerEvents:'none',zIndex:5,transition:'opacity .2s'},bar?{left:'5px',bottom:'4px',width:'12px',height:'12px',opacity:locked?.45:.9}:{top:'6px',right:'6px',width:'18px',height:'18px',borderRadius:'9px',background:ctlOn?'rgba(26,159,255,.95)':(locked?'rgba(0,0,0,.35)':'rgba(26,159,255,.6)'),opacity:locked?.6:1})},Ic(ctlOn?'M12 2l4 4h-3v4h-2V6H8l4-4zm0 20l-4-4h3v-4h2v4h3l-4 4zM2 12l4-4v3h4v2H6v3l-4-4zm20 0l-4 4v-3h-4v-2h4V8l4 4z':(locked?'M18 8h-1V6a5 5 0 0 0-10 0v2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2zM9 6a3 3 0 0 1 6 0v2H9z':'M12 1a5 5 0 0 0-5 5v2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2H9V6a3 3 0 0 1 5.8-1.1l1.9-.7A5 5 0 0 0 12 1z'),bar?10:11)):null,h(Req,{key:'req',lv:locked?1:2}));};
rh.addGlobalComponent('ytmini-mini',Mini);window.__bvmini=true;return 'ok';})()