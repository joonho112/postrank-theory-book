/* Native controls and explicit reset; this helper does not compute scientific results. */
(function(root){'use strict';
 function init(config){
  const doc=root.document;if(!doc)return null;
  const controls={};for(const id of Object.keys(config.defaults)){const el=doc.getElementById(id);if(!el)throw new Error('Missing control: '+id);controls[id]=el;el.value=String(config.defaults[id]);}
  const values=()=>Object.fromEntries(Object.entries(controls).map(([key,el])=>[key,el.value]));
  function update(){const message=config.render(values());const status=doc.getElementById('widget-status');if(status&&message)status.textContent=String(message);resize();}
  for(const el of Object.values(controls)){el.addEventListener('change',update);if(el.type==='range')el.addEventListener('input',update);el.disabled=false;}
  const reset=doc.getElementById('widget-reset');if(!reset)throw new Error('Missing reset');reset.addEventListener('click',()=>{for(const [id,value] of Object.entries(config.defaults))controls[id].value=String(value);update();});reset.disabled=false;update();return {update,values};
 }
 function resize(){if(!root.document||root.parent===root)return;const content=root.document.querySelector('.postrank-widget');if(!content)return;const height=Math.ceil(content.getBoundingClientRect().height);root.parent.postMessage({type:'postrank-widget-height',height},'*');}
 const api={init,resize};if(typeof module!=='undefined'&&module.exports)module.exports=api;else{root.PostrankWidget=api;if(root.ResizeObserver){const content=root.document.querySelector('.postrank-widget');if(content)new root.ResizeObserver(resize).observe(content);}root.addEventListener('load',resize);}
})(typeof window==='undefined'?globalThis:window);
