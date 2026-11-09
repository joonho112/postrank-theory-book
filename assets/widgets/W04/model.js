/* Stored exact results from the accepted crossed-law pilot; no optimizer runs. */
(function(root){'use strict';
 const choices={
  common:{name:'Common grades',grades:[[1,1],[1,1]],risk:'1/3',joint:'0',issued:0,familySize:3,optima:['W/W'],conclusion:'Both comparisons are withheld. The report asserts no direction in either domain.'},
  profile:{name:'Domain profiles',grades:[[1,2],[2,1]],risk:'1/5',joint:'1/5',issued:2,familySize:9,optima:['AB/BA'],conclusion:'Alder is placed higher in Domain 1; Birch is placed higher in Domain 2. The two errors occur together in the state of probability 1/5.'}
 };
 function getChoice(key){
  if(!Object.prototype.hasOwnProperty.call(choices,key))throw new RangeError('Unknown report form');
  const x=choices[key];return {...x,grades:x.grades.map(r=>r.slice()),optima:x.optima.slice()};
 }
 const api={getChoice};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.W04Model=api;
})(typeof window==='undefined'?globalThis:window);
