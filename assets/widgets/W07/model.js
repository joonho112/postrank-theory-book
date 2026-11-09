/* Exact complete-law teaching model; no DOM, sampling, optimizer or network. */
(function(root){'use strict';
 const fixture={"id":"W07","units":["Alder","Birch"],"domains":["1","2"],"columns":{"W":[1,1],"AB":[1,2],"BA":[2,1]},"family":"product","tau":"1/4","laws":{"resolution":[{"mass":"17/20","targets":[[1,1],[0,0]]},{"mass":"1/10","targets":[[1,-1],[0,0]]},{"mass":"1/20","targets":[[-1,1],[0,0]]},{"mass":"0","targets":[[-1,-1],[0,0]]}]},"defaults":{"alpha":"3/40"},"control_values":{"alpha":["0","1/20","3/40","1/10","1/8","3/20"]},"assumptions":{"target_orientation":"Higher targets are better; grade 1 is highest.","loss":"weak error: a reported i>j fails when theta_i <= theta_j","normalization":"M=choose(2,2)=1 in each domain; withholding cost paid once per domain pair","thresholds":["0","0"],"joint_event":"union of F_d > t_d*N_d, strictly; inclusive J <= alpha","guards":"Identity-only guards; no declared equality between the two units; no mean caps.","zero_disclosure":"N=0 makes the exceedance event false; the error fraction is undefined, shown as NA.","zero_weight":"A zero objective weight never disables a guard or protected domain.","law_status":"Complete stipulated finite probability law, not fitted data or Monte Carlo samples."}};
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r;}return a;};
 function q(x){if(Array.isArray(x))return x;const p=String(x).split('/');return norm(BigInt(p[0]),p.length===2?BigInt(p[1]):1n);}
 function norm(a,b){if(b===0n)throw Error('Zero denominator');if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
 const add=(a,b)=>{a=q(a);b=q(b);return norm(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);};
 const sub=(a,b)=>{b=q(b);return add(a,[-b[0],b[1]]);};
 const mul=(a,b)=>{a=q(a);b=q(b);return norm(a[0]*b[0],a[1]*b[1]);};
 const cmp=(a,b)=>{a=q(a);b=q(b);const v=a[0]*b[1]-b[0]*a[1];return v<0n?-1:v>0n?1:0;};
 const out=a=>{a=q(a);return a[1]===1n?String(a[0]):a[0]+'/'+a[1];};
 const min=xs=>xs.reduce((a,b)=>cmp(a,b)<0?a:b);
 const columns=['W','AB','BA'];
 function evaluateLaw(config){
  const {states,weights,alpha,tau,family}=config, thresholds=config.thresholds||['0','0'];
  if(cmp(states.reduce((s,x)=>add(s,x.mass),'0'),'1')!==0||states.some(x=>cmp(x.mass,'0')<0))throw Error('Incomplete probability law');
  if(cmp(add(weights[0],weights[1]),'1')!==0||weights.some(x=>cmp(x,'0')<0))throw Error('Invalid weights');
  const cards=family==='common'?columns.map(c=>[c,c]):columns.flatMap(a=>columns.map(b=>[a,b]));
  const rows=cards.map(card=>{
   const N=card.map(c=>c==='W'?0:1), risks=['0','0'];let J='0';
   for(const state of states){
    const errors=card.map((c,d)=>c==='W'?0:c==='AB'?Number(state.targets[0][d]<=state.targets[1][d]):Number(state.targets[1][d]<=state.targets[0][d]));
    for(let d=0;d<2;d++)risks[d]=out(add(risks[d],mul(state.mass,add(errors[d],mul(tau,1-N[d])))));
    if(errors.some((e,d)=>cmp(e,mul(thresholds[d],N[d]))>0))J=out(add(J,state.mass));
   }
   return {id:card.join('/'),columns:card,risk:out(add(mul(weights[0],risks[0]),mul(weights[1],risks[1]))),criterion_risks:risks,J:alpha===null?null:J,feasible:alpha===null||cmp(J,alpha)<=0,N,K:N.map(n=>n+1),error_fraction:N.map((n,d)=>n?risks[d]:'NA')};
  });
  const feasible=rows.filter(r=>r.feasible),minimum=min(feasible.map(r=>r.risk));
  const optima=feasible.filter(r=>cmp(r.risk,minimum)===0).map(r=>r.id);
  const factors=[0,1].map(d=>columns.filter(c=>feasible.some(r=>r.columns[d]===c)));
  const minima=[0,1].map(d=>min(feasible.map(r=>r.criterion_risks[d])));
  const lower=out(add(mul(weights[0],minima[0]),mul(weights[1],minima[1]))),maxN=Math.max(...feasible.map(r=>r.N[0]+r.N[1]));
  for(const row of rows){row.optimal=optima.includes(row.id);row.criterion_costs=row.criterion_risks.map((r,d)=>out(sub(r,minima[d])));}
  return {rows,minimum,optima,factors,product_family:feasible.length===factors[0].length*factors[1].length,criterion_minima:minima,weighted_lower_bound:lower,lower_bound_attained:cmp(minimum,lower)===0,max_disclosure:maxN,max_disclosure_cards:feasible.filter(r=>r.N[0]+r.N[1]===maxN).map(r=>r.id)};
 }
 function evaluate(values){
  const v=Object.assign({},fixture.defaults,values||{});
  for(const [k,opts] of Object.entries(fixture.control_values))if(!opts.includes(v[k]))throw Error('Unsupported control value: '+k);
  let law,weights,alpha;
  if(fixture.id==='W03'){law='crossed';weights=[v.weight,out(sub('1',v.weight))];alpha=null;}
  else if(fixture.id==='W05'){law=v.setting.startsWith('independent')?'independent':'coincident';weights=[v.weight,out(sub('1',v.weight))];alpha=v.setting.endsWith('unprotected')?null:'3/20';}
  else if(fixture.id==='W06'){law=v.coupling;weights=['1/2','1/2'];alpha=v.alpha;}
  else{law='resolution';weights=['1/4','3/4'];alpha=v.alpha;}
  return Object.assign({values:v,law,weights,alpha,tau:fixture.tau},evaluateLaw({states:fixture.laws[law],weights,alpha,tau:fixture.tau,family:fixture.family}));
 }
 const api={fixture,evaluate,evaluateLaw};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PostrankW07=api;
})(typeof window==='undefined'?globalThis:window);
