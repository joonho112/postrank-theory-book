(function(){'use strict';
 const write=(id,value)=>{document.getElementById(id).textContent=String(value);};
 PostrankWidget.init({defaults:{report:'full',threshold:'1/5'},render(values){
  const x=W10Model.evaluate(values.report,values.threshold);
  write('report-name',x.name);write('issued',x.N);write('false-count',x.F);write('fraction',x.fraction===null?'NA — no issued comparisons':x.fraction);write('probability',x.probability);
  write('threshold-shown',x.threshold);write('exceeded',x.exceeded?'Yes':'No');
  write('cutoff',x.N===0?'Inactive: no issued comparisons':x.firstExceedanceCount+' errors'+(x.firstExceedanceCount>x.N?' (more than can be issued)':''));
  write('explanation',x.N===0?'Both counts are zero. The fraction is undefined, and the strict event is false. Withholding does not assert equal targets.':x.exceeded?'The false-direction fraction is strictly greater than the threshold in the only state. Its exact probability is 1.':'The false-direction fraction is at or below the threshold in the only state. Equality does not trigger strict exceedance.');
  x.grades.forEach((g,i)=>write('grade-'+i,g));x.pairs.forEach((p,i)=>{write('direction-'+i,p.direction);write('error-'+i,p.falseIssued===null?'Not issued':p.falseIssued?'False':'Correct');});
  return x.name+': '+x.F+' false directions among '+x.N+' issued comparisons; fraction '+(x.fraction===null?'undefined':x.fraction)+', threshold '+x.threshold+', exceedance probability '+x.probability+'.';
 }});
})();
