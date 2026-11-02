(()=>{const D=window.DFL;const w=D.Router.WindowStore.GamepadUIMainWindowInstance;
if(window.__bv){try{window.__bv.Destroy()}catch(e){}}
const b=w.CreateBrowserView('YTMiniView');window.__bv=b;b.LoadURL('data:text/plain,'+%s);return 'ok';})()