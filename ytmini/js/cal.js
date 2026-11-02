(()=>{const q='__Q__',r={};const p=document.getElementById('movie_player')||document.querySelector('.html5-video-player');r.player=!!p;
try{if(p&&q){if(q==='fit'&&p.setPlaybackQualityRange){const H={highres:4320,hd2880:2880,hd2160:2160,hd1440:1440,hd1080:1080,hd720:720,large:480,medium:360,small:240,tiny:144};
 const A=((p.getAvailableQualityLevels&&p.getAvailableQualityLevels())||[]).filter(x=>H[x]).sort((a,b)=>H[a]-H[b]);const px=innerHeight*devicePixelRatio;r.px=Math.round(px);
 let t=A.find(x=>H[x]>=px*0.9);if(!t)t=A[A.length-1];if(t){p.setPlaybackQualityRange(t,t);r.fit=t;r.set='fit'}else{p.setPlaybackQualityRange('tiny','highres');r.set='range'}}
 else if(p.setPlaybackQualityRange){if(q==='auto')p.setPlaybackQualityRange('tiny','highres');else p.setPlaybackQualityRange(q,q);r.set='range'}else if(p.setPlaybackQuality){p.setPlaybackQuality(q);r.set='q'}}
if(p&&p.getAvailableQualityLevels)r.disp=p.getAvailableQualityLevels();if(p&&p.getPlaybackQuality)r.actual=p.getPlaybackQuality()}catch(e){r.err=String(e)}
const v=document.querySelector('video');r.video=v?[v.videoWidth,v.videoHeight]:null;return JSON.stringify(r)})()