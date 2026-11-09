(function(){'use strict';
 const write=(id,value)=>{document.getElementById(id).textContent=String(value);};
 PostrankWidget.init({defaults:{representation:'common'},render(values){
  const s=W04Model.getChoice(values.representation);
  write('card-title',s.name);
  for(let i=0;i<2;i++)for(let d=0;d<2;d++)write('g'+i+d,s.grades[i][d]);
  write('risk',s.risk);write('joint',s.joint);write('issued',s.issued);write('family-size',s.familySize);write('meaning',s.conclusion);
  return s.name+': loss '+s.risk+', joint error probability '+s.joint+', '+s.issued+' issued comparisons. Best feasible card among '+s.familySize+' candidates.';
 }});
})();
