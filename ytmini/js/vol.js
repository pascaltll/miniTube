(async()=>{window.__bvvol='';try{const A=SteamClient.System.Audio;const nom=__NOM__,mode=__MODE__,val=__VAL__;
const nm=x=>String(x.sName||x.name||'');const f=(i)=>(i.vecDevices||[]).find(x=>nom==='*def'?(x.bIsDefaultOutputDevice&&x.bHasOutput):nm(x)===nom);
const i=await A.GetDevices();const d=f(i);if(!d){window.__bvvol='dispositivo no encontrado: '+nom;return}
const cur=d.flOutputVolume;if(mode==='lista'){window.__bvvol=JSON.stringify({canal:nom,vol:Math.round(cur*100)});return}
let t=mode==='rel'?cur+val/100:val/100;t=Math.max(0,Math.min(1,t));A.SetDeviceVolume(d.id,1,t);
await new Promise(r=>setTimeout(r,350));const j=await A.GetDevices();const e=(j.vecDevices||[]).find(x=>x.id===d.id);
window.__bvvol=JSON.stringify({canal:nom,antes:Math.round(cur*100),pedido:Math.round(t*100),despues:e?Math.round(e.flOutputVolume*100):null})}catch(e){window.__bvvol='error '+e}})()