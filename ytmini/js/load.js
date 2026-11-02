(()=>{try{const D=window.DFL,R=window.SP_REACT,h=R&&R.createElement,L=window.DeckyPluginLoader;
if(!D||!R||!L||!L.routerHook)return 'sin Decky';
const St=window.__bvload=window.__bvload||{};St.msg=__MSG__;St.err=__ERR__;St.on=true;
if(St.mounted){if(St.kick)St.kick();return 'ok'}
const SVG='<svg viewBox="0 0 64 64" width="58" height="58" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="ytmg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs><rect x="4" y="8" width="48" height="36" rx="6" fill="#0b0f14" stroke="url(#ytmg)" stroke-width="3"/><rect x="21" y="29" width="38" height="25" rx="5" fill="url(#ytmg)"/><path d="M35 35v13l11-6.5z" fill="#fff"/></svg>';
const CSS='@keyframes ytmfade{from{opacity:0}to{opacity:1}}@keyframes ytmrise{from{opacity:0;transform:translateY(10px) scale(.97)}to{opacity:1;transform:none}}@keyframes ytmbar{0%{left:-45%}100%{left:100%}}@keyframes ytmbreath{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}';
const Card=()=>{const [,t]=R.useState(0);
 R.useEffect(()=>{St.kick=()=>t(x=>x+1);St.mounted=true;return()=>{St.mounted=false;St.kick=null}},[]);
 if(!St.on)return null;const err=!!St.err;
 return h('div',{style:{position:'fixed',top:0,left:0,right:0,bottom:0,zIndex:9000,display:'flex',alignItems:'center',justifyContent:'center',pointerEvents:'none',background:'rgba(4,6,10,.5)',animation:'ytmfade .22s ease-out'}},
  h('style',null,CSS),
  h('div',{style:{width:'300px',boxSizing:'border-box',padding:'22px 22px 20px',borderRadius:'14px',background:'#0b0f14',border:'1px solid rgba(255,255,255,.16)',boxShadow:'0 8px 26px rgba(0,0,0,.6)',textAlign:'center',font:'14px/1.4 sans-serif',color:'#e8ecf4',animation:'ytmrise .28s ease-out'}},
   h('div',{style:{display:'inline-block',animation:err?'none':'ytmbreath 2.2s ease-in-out infinite'},dangerouslySetInnerHTML:{__html:SVG}}),
   h('div',{style:{marginTop:'8px',font:'700 20px sans-serif',letterSpacing:'.2px'}},'Mini',h('span',{style:{background:'linear-gradient(90deg,#22d3ee,#8b5cf6)',WebkitBackgroundClip:'text',backgroundClip:'text',color:'transparent'}},'Tube')),
   err?h('div',{style:{marginTop:'12px',color:'#fbbf24',fontSize:'13px'}},St.msg||'No se pudo abrir')
      :h('div',{style:{marginTop:'12px',color:'#aab3c5',fontSize:'13px'}},St.msg||'Opening…'),
   err?null:h('div',{style:{position:'relative',height:'3px',marginTop:'14px',borderRadius:'2px',background:'rgba(255,255,255,.1)',overflow:'hidden'}},
     h('div',{style:{position:'absolute',top:0,height:'100%',width:'45%',borderRadius:'2px',background:'linear-gradient(90deg,#22d3ee,#8b5cf6)',animation:'ytmbar 1.15s ease-in-out infinite'}}))));};
L.routerHook.addGlobalComponent('ytmini-load',Card);return 'ok'}catch(e){return 'error: '+String(e)}})()
