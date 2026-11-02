(async()=>{const o={md:typeof navigator.mediaDevices,sr:typeof window.SpeechRecognition+'/'+typeof window.webkitSpeechRecognition,secure:window.isSecureContext};
try{const d=await navigator.mediaDevices.enumerateDevices();o.entradas=d.filter(x=>x.kind==='audioinput').length}catch(e){o.enum=String(e)}
try{const st=await navigator.permissions.query({name:'microphone'});o.permiso=st.state}catch(e){o.permiso='?'+e}
try{const g=await navigator.mediaDevices.getUserMedia({audio:true});o.getUserMedia='ok';g.getTracks().forEach(t=>t.stop())}catch(e){o.getUserMedia=e.name+': '+e.message}
window.__ytmmic=JSON.stringify(o);return 0})()