(()=>{const o=[];const tryit=(n,f)=>{try{const r=f();o.push(n+':'+(r===undefined?'ok':String(r)))}catch(e){o.push(n+': error '+String(e).slice(0,70))}};
const b=window.__bv;tryit('m_refKeyboard.ShowVirtualKeyboard',()=>{if(!b||!b.m_refKeyboard||typeof b.m_refKeyboard.ShowVirtualKeyboard!=='function')return 'no existe';b.m_refKeyboard.ShowVirtualKeyboard()});
if(window.__kbmode==='B'){o.length=0}
tryit('MainWindowInstance.m_VirtualKeyboardManager',()=>{const m=window.SteamUIStore&&SteamUIStore.m_WindowStore&&SteamUIStore.m_WindowStore.MainWindowInstance&&SteamUIStore.m_WindowStore.MainWindowInstance.m_VirtualKeyboardManager;if(!m||typeof m.SetVirtualKeyboardVisible!=='function')return 'no existe';m.SetVirtualKeyboardVisible()});
return o.join(' | ')})()