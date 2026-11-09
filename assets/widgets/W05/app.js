(function(){'use strict';
 const model=window.PostrankW05,doc=document;
 function table(id,headers,rows){const body=doc.getElementById(id);body.replaceChildren();for(const row of rows){const tr=doc.createElement('tr');row.forEach((value,i)=>{const cell=doc.createElement(i===0?'th':'td');if(i===0)cell.scope='row';cell.textContent=String(value);tr.appendChild(cell);});body.appendChild(tr);}}
 function render(values){const r=model.evaluate(values),w=model.fixture.id;
  doc.getElementById('selection').textContent='All minimum-risk cards: '+r.optima.join(', ')+'. Minimum risk: '+r.minimum+'.';
  doc.getElementById('setting-summary').textContent='Weights ('+r.weights.join(', ')+'); cost '+r.tau+'; '+(r.alpha===null?'joint protection disabled.':'strict exceedance threshold 0 in each domain; inclusive joint cap '+r.alpha+'.');
  table('candidate-rows',[],r.rows.map(x=>[x.id,x.risk,x.criterion_risks.join(', '),x.J===null?'Disabled':x.J,x.feasible?'Yes':'No',x.optimal?'Optimal':'—']));
  table('law-rows',[],model.fixture.laws[r.law].map(s=>['('+s.targets[0].join(', ')+')',s.mass]));
  let explanation;
  if(w==='W03'){explanation='Criterion-specific minima in the same column family: ('+r.criterion_minima.join(', ')+'). Costs below are unweighted risk increments, including at a zero objective weight.';table('detail-rows',[],r.rows.filter(x=>x.optimal).map(x=>[x.id,...x.criterion_costs]));}
  else if(w==='W05'){explanation='Actual projections: {'+r.factors[0].join(', ')+'} × {'+r.factors[1].join(', ')+'}. Product family: '+(r.product_family?'yes':'no')+'. Weighted sum of projected minima: '+r.weighted_lower_bound+'. Bound attained: '+(r.lower_bound_attained?'yes':'no')+'. The comparison uses all feasible cards.';table('detail-rows',[],r.rows.filter(x=>x.optimal).map(x=>[x.id,x.N.join(', '),x.K.join(', ')]));}
  else if(w==='W06'){const fixed=r.rows.find(x=>x.id==='AB/AB');explanation='For the fixed AB/AB card: marginal error probabilities (1/10, 1/10), additive risk '+fixed.risk+', union probability '+fixed.J+'. The sum 1/5 is not substituted for the union.';table('detail-rows',[],r.rows.filter(x=>x.optimal).map(x=>[x.id,x.N.join(', '),x.K.join(', ')]));}
  else{explanation='Auxiliary maximum total disclosure: '+r.max_disclosure+' (cards: '+r.max_disclosure_cards.join(', ')+'). This separate maximum is not a monotonicity claim about each risk-optimal domain grade count.';table('detail-rows',[],r.rows.filter(x=>x.optimal).map(x=>[x.id,x.N.join(', '),x.K.join(', ')]));}
  doc.getElementById('explanation').textContent=explanation;
  return r.rows.filter(x=>x.feasible).length+' feasible cards; '+r.optima.length+' minimum-risk card'+(r.optima.length===1?'':'s')+'. All ties shown.';
 }
 window.PostrankWidget.init({defaults:model.fixture.defaults,render});
})();
