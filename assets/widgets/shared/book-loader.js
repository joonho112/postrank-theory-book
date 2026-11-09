/* Load a local exhibit only after the reader asks; frame messages are source-bound. */
(function(){'use strict';if(window.PostrankBookLoader)return;window.PostrankBookLoader=true;
 function start(){
  document.querySelectorAll('[data-postrank-widget]').forEach(host=>{
   const button=host.querySelector('[data-widget-load]'),slot=host.querySelector('[data-widget-frame]');if(!button||!slot)return;
   button.disabled=false;button.addEventListener('click',()=>{
    if(slot.querySelector('iframe'))return;
    const url=new URL(host.dataset.widgetSrc,document.baseURI);
    if(url.protocol!==location.protocol||url.host!==location.host||!url.pathname.includes('/assets/widgets/'))throw new Error('Only local book widgets may load');
    const frame=document.createElement('iframe');frame.title=host.dataset.widgetTitle;frame.loading='lazy';frame.setAttribute('sandbox','allow-scripts');frame.setAttribute('referrerpolicy','no-referrer');frame.style.width='100%';frame.style.height=(host.dataset.widgetHeight||'900')+'px';frame.style.border='1px solid #cad5d7';frame.src=url.href;
    window.addEventListener('message',event=>{if(event.source!==frame.contentWindow||!event.data||event.data.type!=='postrank-widget-height')return;const h=Number(event.data.height);if(Number.isFinite(h)&&h>=200&&h<=6000)frame.style.height=h+'px';});
    slot.appendChild(frame);button.disabled=true;button.textContent='Interactive example opened';
   });
  });
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
