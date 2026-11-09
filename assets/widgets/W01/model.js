(function(root,factory){if(typeof module!=='undefined'&&module.exports)module.exports=factory(require('./data.js'));else root.W01Model=factory(root.W01Data);})(typeof window==='undefined'?globalThis:window,function(data){'use strict';
 function evaluate(settings){const gap=Number(settings.gap_index),sd=Number(settings.sd_choice);if(!Number.isInteger(gap)||gap< -8||gap>8||![1,2,3].includes(sd))throw new RangeError('Unknown normal-law setting');const row=data.rows.find(x=>x.gap_index===gap&&x.sd_choice===sd);if(!row)throw new Error('Missing declared law');return {...row};}
 return {evaluate,defaults:data.defaults,allSettings:()=>data.rows.map(r=>({gap_index:r.gap_index,sd_choice:r.sd_choice}))};
});
