/* Exact evaluation of three fixed reports under one complete, one-state law. */
(function(root){'use strict';
 const targets=[4,2,3,1];
 const reports={full:{name:'All six comparisons',grades:[1,2,3,4]},coarsened:{name:'Two unresolved bands',grades:[1,1,2,2]},withheld:{name:'All comparisons withheld',grades:[1,1,1,1]}};
 const thresholds={'0':[0n,1n],'1/6':[1n,6n],'1/5':[1n,5n],'1/4':[1n,4n],'1':[1n,1n]};
 function ratio(a,b){let x=a,y=b;while(y){const z=x%y;x=y;y=z;}return b/x===1?String(a/x):(a/x)+'/'+(b/x);}
 function evaluate(reportKey,threshold){
  if(!Object.prototype.hasOwnProperty.call(reports,reportKey))throw new RangeError('Unknown report');
  if(!Object.prototype.hasOwnProperty.call(thresholds,threshold))throw new RangeError('Unknown exact threshold');
  const report=reports[reportKey],pairs=[];let N=0,F=0;
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
   if(report.grades[i]===report.grades[j]){pairs.push({pair:(i+1)+'–'+(j+1),direction:'Withheld',falseIssued:null});continue;}
   const high=report.grades[i]<report.grades[j]?i:j,low=high===i?j:i;
   const error=targets[high]<=targets[low];N++;if(error)F++;
   pairs.push({pair:(i+1)+'–'+(j+1),direction:(high+1)+' > '+(low+1),falseIssued:error});
  }
  const [p,q]=thresholds[threshold];
  const exceeded=N>0&&BigInt(F)*q>p*BigInt(N);
  return {reportKey,name:report.name,grades:report.grades.slice(),targets:targets.slice(),originalPairs:6,N,F,fraction:N===0?null:ratio(F,N),threshold,firstExceedanceCount:Number(p*BigInt(N)/q+1n),exceeded,probability:exceeded?'1':'0',pairs};
 }
 const api={evaluate};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.W10Model=api;
})(typeof window==='undefined'?globalThis:window);
