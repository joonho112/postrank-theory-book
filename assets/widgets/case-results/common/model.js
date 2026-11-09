(function(root,factory){'use strict';const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.PostrankSavedResults=api;})(typeof globalThis==='undefined'?this:globalThis,function(){'use strict';
 function copy(value){return JSON.parse(JSON.stringify(value));}
 function counts(rows){const out={sites:rows.length,M:rows.length*(rows.length-1)/2,S:0,C:0,any:0,none:0,concordant:0,crossing:0,S_only:0,C_only:0};for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){const s=Math.sign(rows[j].S_grade-rows[i].S_grade),c=Math.sign(rows[j].C_grade-rows[i].C_grade);if(s)out.S++;if(c)out.C++;if(s||c)out.any++;else out.none++;if(s&&c)out[s===c?'concordant':'crossing']++;else if(s)out.S_only++;else if(c)out.C_only++;}return out;}
 function commonCounts(rows){const groups={};for(const row of rows)groups[row.grade]=(groups[row.grade]||0)+1;const n=rows.length,M=n*(n-1)/2;return {units:n,M,N:M-Object.values(groups).reduce((sum,k)=>sum+k*(k-1)/2,0),grades:Object.keys(groups).length};}
 function create(data){
  if(!data||!Array.isArray(data.scenarios)||!data.scenarios.length)throw new Error('Saved scenarios required');
  const ids=data.scenarios.map(x=>x.id);if(new Set(ids).size!==ids.length)throw new Error('Duplicate scenario');
  for(const s of data.scenarios){const rows=s.rows||[];if(new Set(rows.map(x=>x.id)).size!==rows.length)throw new Error('Duplicate unit ID');if(s.kind==='profile')for(const r of rows)if(!Number.isInteger(r.S_grade)||!Number.isInteger(r.C_grade)||r.S_grade<1||r.C_grade<1)throw new Error('Invalid stored grade');}
  const defaults=Object.freeze({scenario:data.defaultScenario,unit:data.unitControl==='lookup'?'':'none'});if(!ids.includes(defaults.scenario))throw new Error('Unknown default scenario');
  function readout(scenario,unit){const s=data.scenarios.find(x=>x.id===scenario);if(!s)throw new RangeError('Unknown stored scenario');const rows=s.rows||[];const chosen=unit&&unit!=='none'?rows.find(x=>x.id===unit):null;return {id:s.id,label:s.label,metrics:copy(s.metrics),notes:copy(s.notes||[]),columns:copy(s.columns||[]),rows:copy(rows),rowCaption:s.rowCaption||'Stored unit values',unit:chosen?copy(chosen):null,unitStatus:chosen?'Selected '+chosen.label+'.':unit&&unit!=='none'?'That unit is not in this reporting frame.':'No unit highlighted.',counts:s.kind==='profile'?counts(rows):s.kind==='common'?commonCounts(rows):null};}
  return Object.freeze({defaults,readout,scenarios:()=>data.scenarios.map(s=>({id:s.id,label:s.label})),reset:()=>readout(defaults.scenario,defaults.unit)});
 }
 return Object.freeze({create,profilePairCounts:counts,commonPairCounts:commonCounts});
});
