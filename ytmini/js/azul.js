(()=>{const m=window.__bvmel;if(!m)return 'sin tarjeta mini';const d=m.ownerDocument,V=d.defaultView,r=m.getBoundingClientRect(),out=[];
for(const p of [[.5,.5],[.08,.5],[.92,.5],[.5,.2],[.5,.92]]){const x=r.x+r.width*p[0],y=r.y+r.height*p[1];
 out.push([p.join(','),d.elementsFromPoint(x,y).slice(0,9).map(e=>{const cs=V.getComputedStyle(e);return e.tagName.toLowerCase()+'.'+String(e.className).slice(0,28)+' bg='+cs.backgroundColor+(cs.backgroundImage!=='none'?'+img':'')})])}
return JSON.stringify(out)})()