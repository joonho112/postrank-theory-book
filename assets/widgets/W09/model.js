(function(root,factory){if(typeof module!=='undefined'&&module.exports)module.exports=factory(require('./data.js'));else root.W09Model=factory(root.W09Data);})(typeof window==='undefined'?globalThis:window,function(data){'use strict';
 function evaluate(settings){const draws=Number(settings.draws);const row=data.rows.find(x=>x.draws===draws);if(!row)throw new RangeError('Unknown prespecified draw count');return {...row,variance:4/(25*draws),scope:'Theoretical iid frequency variability; unchanged pair-error probability, no simulated estimate or guarantee.'};}
 return {evaluate,defaults:data.defaults,allSettings:()=>data.rows.map(r=>({draws:r.draws}))};
});
