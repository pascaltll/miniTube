(()=>{const D=window.DFL,R=window.SP_REACT,h=R.createElement,BC=window.__bvc,b=window.__bv;
if(!BC||!b)return 'faltan piezas';let CLS='';try{const cm=D.findClassModule(m=>!!m['ExternalBrowserContainer']||!!m['MainBrowserContainer']);CLS=(cm&&cm.ExternalBrowserContainer)||'';}catch(e){}window.__bvcls=CLS;
try{D.Navigation.CloseSideMenus()}catch(e){}
window.__bvpress=0;window.__bverr='';window.__bvfs=false;window.__bvgame=-1;const tok={e:false};window.__bvtok=tok;
const press=(hid)=>{try{const I=SteamClient.Input;I.ControllerKeyboardSetKeyState(hid,true);I.ControllerKeyboardSetKeyState(hid,false);window.__bvpress++;}catch(e){window.__bverr=String(e)}};
const GB=D.GamepadButton||{};
const onDir=(ev)=>{const bt=ev&&ev.detail&&ev.detail.button;
 if(bt===GB.DIR_UP)press(82);else if(bt===GB.DIR_DOWN)press(81);else if(bt===GB.DIR_LEFT)press(80);else if(bt===GB.DIR_RIGHT)press(79);};
const STEAMBTN=__STEAMBTN__;
const Gb=(d,fn,off,g)=>h('div',{onClick:fn,style:{position:'absolute',top:g.t+'px',right:(g.r+off)+'px',width:'40px',height:'40px',borderRadius:'20px',zIndex:10,
    background:'rgba(14,20,27,.36)',backdropFilter:'blur(10px)',WebkitBackdropFilter:'blur(10px)',border:'1px solid rgba(255,255,255,.2)',opacity:.78,
    display:'flex',alignItems:'center',justifyContent:'center'}},
  h('svg',{width:20,height:20,viewBox:'0 0 24 24',style:{display:'block',fill:'#fff'}},h('path',{d})));
const meas=()=>{try{const w=window.__bvwrap,e=window.__bvel,c=w&&w.firstElementChild;if(!c||!e)return {off:40,t:8,r:8};const wr=w.getBoundingClientRect(),cr=c.getBoundingClientRect(),er=e.getBoundingClientRect();
 return {off:Math.max(0,Math.min(80,Math.round(cr.top-wr.top))),t:Math.max(0,Math.round(cr.top-er.top))+8,r:Math.max(0,Math.round(er.right-cr.right))+8}}catch(x){return {off:40,t:8,r:8}}};
const Slider=(q)=>{const ref=R.useRef(null),dr=R.useRef(false);
 const set=(e)=>{try{const r=ref.current.getBoundingClientRect();q.onChange(Math.round(Math.max(0,Math.min(1,1-(e.clientY-r.top)/r.height))*100))}catch(x){}};
 return h('div',{style:{display:'flex',flexDirection:'column',alignItems:'center',gap:'6px',width:'54px',height:'100%'}},
  h('div',{style:{fontSize:'10px',color:'#8b929a',textTransform:'uppercase',letterSpacing:'.5px'}},q.label),
  h('div',{ref,onPointerDown:(e)=>{try{e.currentTarget.setPointerCapture(e.pointerId)}catch(x){}dr.current=true;set(e)},onPointerMove:(e)=>{if(dr.current)set(e)},
   onPointerUp:(e)=>{if(dr.current){dr.current=false;set(e);q.onCommit&&q.onCommit()}},onPointerCancel:()=>{dr.current=false},
   style:{position:'relative',width:'30px',flex:1,minHeight:'110px',borderRadius:'15px',background:'rgba(255,255,255,.12)',touchAction:'none',overflow:'hidden'}},
   h('div',{style:{position:'absolute',left:0,right:0,bottom:0,height:q.value+'%',background:'#1a9fff',borderRadius:'15px'}})),
  h('div',{style:{fontSize:'12px',color:'#dcdedf'}},q.value+'%'))};
const VolBar=()=>{const [loc,setLoc]=R.useState({});const last=R.useRef({});const meta=window.__bvmeta||{};
 const yt=loc.yt!=null?loc.yt:(meta.vol!=null?Math.round(meta.vol*100):100);const gm=window.__bvgame;const gv=loc.game!=null?loc.game:(gm>=0?gm:null);
 const send=(k,v)=>{window.__bvreq='vol:'+k+'='+v};
 const mk=(k,label,val)=>h(Slider,{label,value:val,onChange:(v)=>{setLoc(o=>Object.assign({},o,{[k]:v}));const n=Date.now();if(n-(last.current[k]||0)>180){last.current[k]=n;send(k,v)}},
  onCommit:()=>{setTimeout(()=>{const v=(window.__bvloc||{})[k];if(v!=null)send(k,v)},30);setTimeout(()=>setLoc(o=>{const c=Object.assign({},o);delete c[k];return c}),2500)}});
 window.__bvloc=loc;
 return h('div',{style:{display:'flex',flexDirection:'row',gap:'6px',padding:'10px 8px',alignItems:'stretch',justifyContent:'center',width:(gv!=null?118:66)+'px',flex:'none'}},mk('yt','YouTube',yt),gv!=null?mk('game','Game',gv):null)};
const Body=(p)=>{
 const [,tick]=R.useState(0);
 R.useEffect(()=>{const id=setInterval(()=>tick(x=>x+1),700);return()=>clearInterval(id)},[]);
 R.useEffect(()=>{const v=b.m_browserView;let stop=false,last='',chk=0,bl=null;const sync=()=>{if(stop)return;const w=window.__bvwrap;if(!w)return;let t;
   if(window.__bvfs){const W=w.ownerDocument.defaultView;t=[0,0,W.innerWidth,W.innerHeight];window.__bvfst=t}else{let r=null;try{const wr=w.getBoundingClientRect();if(!bl||!w.contains(bl)){bl=null;let best=1e12;for(const e of w.querySelectorAll('*')){const q=e.getBoundingClientRect();if(q.width<wr.width*0.5||q.height<wr.height*0.4)continue;const cs=getComputedStyle(e);
      const colored=(cs.backgroundImage&&cs.backgroundImage!=='none')||(cs.backgroundColor&&!/rgba\(0, 0, 0, 0\)|transparent/.test(cs.backgroundColor));if(!colored)continue;const a=q.width*q.height;if(a<best){best=a;bl=e}}}
     if(bl)r=bl.getBoundingClientRect()}catch(x){}
    if(!r||r.width<50)r=w.getBoundingClientRect();window.__bvblue=!!bl;t=[r.x,r.y,r.width,r.height]}
   const k=t.map(Math.round).join(',');
   try{if(k!==last){last=k;v.SetBounds(t[0],t[1],t[2],t[3]);chk=Date.now();return}
    if(Date.now()-chk>1000){chk=Date.now();Promise.resolve(v.GetBounds()).then(c=>{if(stop||!c)return;if(Math.abs(c.x-t[0])>1||Math.abs(c.y-t[1])>1||Math.abs(c.width-t[2])>1||Math.abs(c.height-t[3])>1)v.SetBounds(t[0],t[1],t[2],t[3])})}}catch(e){}};
  const id=setInterval(sync,40);sync();return()=>{stop=true;clearInterval(id)}},[]);
 const [sw,setSw]=R.useState(0);const sref=R.useRef(null);
 R.useEffect(()=>{const doc=(window.__bvwrap&&window.__bvwrap.ownerDocument)||document;
  const inRoot=t=>{try{return !!(t&&t.closest&&t.closest('[data-ytm-root]'))}catch(e){return false}};
  let wd=null,cur=0;
  const S_=(v)=>{cur=v;setSw(v)};
  const arm=()=>{if(wd)clearTimeout(wd);wd=setTimeout(()=>{wd=null;sref.current=null;S_(0)},700)};
  const down=(x,y)=>{if(cur>0)S_(0);sref.current={x:x,y:y,v:0,t:Date.now(),act:false}};
  const move=(x,y)=>{const st=sref.current;if(!st)return false;const dy=y-st.y,dx=Math.abs(x-st.x);if(!st.act){if(dy>36&&dx<dy*0.7)st.act=true;else return false}st.v=Math.max(0,dy)/Math.max(1,Date.now()-st.t);S_(Math.max(0,dy-30));arm();return true};
  const fin=(y)=>{const st=sref.current;sref.current=null;if(wd){clearTimeout(wd);wd=null}if(!st)return;if(!st.act){if(cur>0)S_(0);return}const dy=Math.max(0,y-st.y);
   if(dy>90||(dy>40&&st.v>0.5)){S_(420);setTimeout(()=>{tok.e=true;window.__bvreq='autobar';p.closeModal();setTimeout(()=>{tok.e=false;S_(0)},900)},170)}else S_(0)};
  const on=(e)=>{try{const ty=e.type;
   if(ty.indexOf('touch')===0){const t=(e.touches&&e.touches[0])||(e.changedTouches&&e.changedTouches[0]);if(!t)return;
    if(ty==='touchstart'){if(e.touches.length===1)down(t.clientX,t.clientY)}
    else if(ty==='touchmove'){if(move(t.clientX,t.clientY)&&e.cancelable)e.preventDefault()}
    else fin(t.clientY);
    return}
   if(!inRoot(e.target)&&(ty==='pointerdown'||ty==='pointerup'||ty==='click'))window.__bvlastOut=Date.now();
   if(e.pointerType!=='touch'){
    if(ty==='pointerdown'){if(e.isPrimary!==false)down(e.clientX,e.clientY)}
    else if(ty==='pointermove')move(e.clientX,e.clientY);
    else if(ty==='pointerup'||ty==='pointercancel')fin(e.clientY)}
   if(!inRoot(e.target)&&ty!=='pointermove'){e.stopPropagation();if(ty!=='pointerdown'&&ty!=='pointerup'&&e.cancelable)e.preventDefault()}
  }catch(x){}};
  const T=['pointerdown','pointermove','pointerup','pointercancel','mousedown','mouseup','click','touchstart','touchmove','touchend','touchcancel'];
  const O={capture:true,passive:false};
  T.forEach(n=>doc.addEventListener(n,on,O));
  let pb=null,ph=null;try{pb=doc.body.style.touchAction;ph=doc.documentElement.style.touchAction;doc.body.style.touchAction='none';doc.documentElement.style.touchAction='none'}catch(e){}
  return()=>{if(wd)clearTimeout(wd);T.forEach(n=>doc.removeEventListener(n,on,O));try{doc.body.style.touchAction=pb||'';doc.documentElement.style.touchAction=ph||''}catch(e){}}},[]);
 const meta=window.__bvmeta||{},can=!!(meta.has&&meta.t>0.5),g=meas();
 return h(D.ModalRoot,{closeModal:()=>{if(tok.e||Date.now()-(window.__bvlastOut||0)>700)p.closeModal()},onCancel:()=>press(41),onOK:()=>{},bAllowFullSize:true},
 h('div',{'data-ytm-root':'1',style:__OUTER__},
  h(D.Focusable,{style:{position:'absolute',inset:0,display:'flex',flexDirection:'column'},noFocusRing:true,className:'ytmini-foc',
    onGamepadFocus:async(ev)=>{try{await new Promise(r=>setTimeout(r,1));window.__bvfoc=(window.__bvfoc||0)+1;if(ev.target&&ev.target.classList&&ev.target.classList.contains('ytmini-foc')){ev.detail&&ev.detail.focusedNode&&ev.detail.focusedNode.BChildTakeFocus&&ev.detail.focusedNode.BChildTakeFocus();window.__bvchild=(window.__bvchild||0)+1;}}catch(e){window.__bverr=String(e)}},
    onGamepadDirection:onDir,onOKButton:()=>press(88),onCancelButton:()=>press(41),onOptionsButton:()=>{tok.e=true;p.closeModal()},
    onOKActionDescription:'Select',onCancelActionDescription:'Back',onOptionsActionDescription:'Close'},
   h('div',{style:{flex:1,display:'flex',flexDirection:'row',minHeight:'70vh',transform:'translateY('+sw+'px)',opacity:Math.max(0,1-sw/300),transition:sref.current?'none':'transform .17s ease-out, opacity .17s'}},
   h('div',{ref:(el)=>{window.__bvel=el},style:{flex:1,position:'relative',minHeight:'70vh'}},
    h('div',{ref:(el)=>{window.__bvwrap=el},style:{position:'absolute',left:0,right:0,top:0,bottom:0}},h(BC,{browser:b,className:CLS,visible:!(sw>6),hideForModals:false,external:true,displayURLBar:false,autoFocus:true}),(sw>6?h('div',{style:{position:'absolute',inset:0,zIndex:3,background:'#0b0f14',display:'flex',alignItems:'center',justifyContent:'center'}},h('svg',{width:44,height:44,viewBox:'0 0 24 24',style:{fill:'rgba(255,255,255,.7)'}},h('path',{d:'M4 6h11a1 1 0 0 1 1 1v3.5l4-3v9l-4-3V17a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1z'}))):null)),
    (STEAMBTN&&can)?Gb('M10 4v6H4V8h4V4zm4 0h2v4h4v2h-6zM4 14h6v6H8v-4H4zm10 0h6v2h-4v4h-2z',()=>{window.__bvreq='mini';p.closeModal()},48,{t:4,r:8}):null,
    STEAMBTN?Gb('M19 6.4 17.6 5 12 10.6 6.4 5 5 6.4 10.6 12 5 17.6 6.4 19 12 13.4 17.6 19 19 17.6 13.4 12z',p.closeModal,0,{t:4,r:8}):null),
   null)),
  null));};
window.__bvm=D.showModal(h(Body,null),window,{strTitle:'ytmini-bv',bHideMainWindowForPopouts:false,fnOnClose:()=>{window.__bvm=null;if(!tok.e)window.__bvreq='autobar'}});setTimeout(()=>{try{b.m_browserView.SetFocus(true);window.__bvsf=1}catch(e){window.__bverr=String(e)}},1000);return 'ok';})()