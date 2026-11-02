(()=>{const o={},b=window.__bv,BC=window.__bvc;const names=x=>{try{const r=new Set();let p=x;for(let i=0;i<3&&p&&p!==Object.prototype;i++){Object.getOwnPropertyNames(p).forEach(k=>r.add(k));p=Object.getPrototypeOf(p)}return [...r].filter(k=>!/^(constructor|__)/.test(k)).slice(0,90)}catch(e){return String(e)}};
o.browser=names(b);o.view=names(b&&b.m_browserView);
const snip=(src,re)=>{const out=[];let m;const g=new RegExp(re,'g');while((m=g.exec(src))&&out.length<8)out.push(src.slice(Math.max(0,m.index-90),m.index+160));return out};
try{const src=String(BC);o.bcLen=src.length;o.bcBounds=snip(src,'Bounds|SetSize|offsetTop|\\b40\\b');}catch(e){o.bcErr=String(e)}
try{const pr=BC&&BC.prototype;o.bcProto=pr?Object.getOwnPropertyNames(pr).slice(0,40):null;if(pr){const all=Object.getOwnPropertyNames(pr).map(k=>{try{return String(pr[k])}catch(e){return ''}}).join('\n');o.protoBounds=snip(all,'Bounds|SetSize|\\b40\\b')}}catch(e){}
return JSON.stringify(o)})()