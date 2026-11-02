(()=>{const o={};try{const v=document.querySelector('video');o.path=location.pathname;o.query=Array.from(new URLSearchParams(location.search).keys());
o.video=v?{w:v.videoWidth,h:v.videoHeight,portrait:v.videoHeight>v.videoWidth,paused:v.paused,t:Math.round(v.currentTime*10)/10,d:isFinite(v.duration)?Math.round(v.duration):0}:null;
const p=document.getElementById('movie_player')||document.querySelector('.html5-video-player');
if(p){try{o.estado=p.getPlayerState&&p.getPlayerState()}catch(e){}try{const d=p.getVideoData&&p.getVideoData();o.datos=d?{id:d.video_id,titulo:String(d.title||'').slice(0,60)}:null}catch(e){}try{o.calidad=p.getPlaybackQuality&&p.getPlaybackQuality()}catch(e){}}
const tags=new Set();document.querySelectorAll('*').forEach(e=>{const n=e.tagName.toLowerCase();if(/short|reel/.test(n)||/short|reel/i.test(String(e.className||'').slice(0,80)))tags.add(n+(e.className?'.'+String(e.className).split(' ')[0]:''))});
o.shorts=Array.from(tags).slice(0,25);
const ch=[];let e=document.activeElement;for(let i=0;e&&i<8;i++,e=e.parentElement){const n=e.tagName.toLowerCase();if(n.startsWith('ytlr-'))ch.push(n)}o.foco=ch;
o.vp=[innerWidth,innerHeight];o.titulo=document.title.slice(0,50)}catch(x){o.err=String(x)}return JSON.stringify(o)})()
