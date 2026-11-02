(()=>{const D=window.DFL,R=window.SP_REACT;if(!D||!R)return JSON.stringify({error:'sin DFL/SP_REACT'});
const w=D.Router&&D.Router.WindowStore&&D.Router.WindowStore.GamepadUIMainWindowInstance;let bc=null;
try{bc=D.findModuleChild(m=>{if(typeof m!=='object')return;for(const p in m){if(typeof m[p]==='function'){const s=m[p].toString();
if(s.includes('displayURLBar')&&s.includes('BExternalTriggeredLoad()'))return m[p];}}});}catch(e){}
window.__bvc=bc;
return JSON.stringify({ventana_principal:!!w,CreateBrowserView:!!(w&&typeof w.CreateBrowserView==='function'),BrowserContainer:typeof bc,
 showModal:typeof D.showModal,ModalRoot:typeof D.ModalRoot,
 teclado_HID:!!(window.SteamClient&&SteamClient.Input&&typeof SteamClient.Input.ControllerKeyboardSetKeyState==='function')});})()