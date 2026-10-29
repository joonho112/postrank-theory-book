#!/usr/bin/env python3
"""Small exact coordinates for two Chapter9 examples; no figure production."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
import csv,json,hashlib,datetime,platform
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'assets/reproduction/figures/data';REVIEW=ROOT/'evidence/figures/fixtures/f09-coordinate-review.json'
PATHS=[OUT/'f09-grade-pairs.json',OUT/'f09-couplings.csv',OUT/'f09-couplings-metadata.json',REVIEW]
for p in PATHS:
 if p.exists():raise SystemExit('Refuse overwrite existing coordinate artifact: '+str(p.relative_to(ROOT)))
checks=[]
def check(name,ok,detail):
 if not ok:raise AssertionError(name)
 checks.append({'name':name,'status':'PASS','detail':detail})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();UNITS=['A','B','C','D'];PAIRS=list(combinations(range(4),2));reports=[]
expected={'1222':{'N':3,'pairs':['AB','AC','AD']},'1122':{'N':4,'pairs':['AC','AD','BC','BD']}}
for g in [[1,2,2,2],[1,1,2,2]]:
 key=''.join(map(str,g));blocks=[[u for u,z in zip(UNITS,g) if z==grade] for grade in sorted(set(g))];pair_rows=[]
 for i,j in PAIRS:
  issued=g[i]!=g[j];forward=int(g[i]<g[j]);reverse=int(g[j]<g[i]);check('unordered_once_'+key+'_'+UNITS[i]+UNITS[j],forward+reverse==int(issued),'Exactly one ordered direction for a disclosed unordered pair; neither for a hold.')
  pair_rows.append({'pair':UNITS[i]+UNITS[j],'unit_i':UNITS[i],'unit_j':UNITS[j],'g_i':g[i],'g_j':g[j],'x_i_above_j':forward,'x_j_above_i':reverse,'disclosed':issued,'direction':(UNITS[i]+'>'+UNITS[j] if forward else UNITS[j]+'>'+UNITS[i] if reverse else 'hold')})
 N=sum(x['disclosed'] for x in pair_rows);block_product=sum(len(a)*len(b) for a,b in combinations(blocks,2));within=sum(len(b)*(len(b)-1)//2 for b in blocks)
 check('direct_vs_block_counts_'+key,N==block_product==6-within==expected[key]['N'],'Direct six-pair mask, cross-block products and complement of within-block pairs agree.')
 check('explicit_pair_labels_'+key,[x['pair'] for x in pair_rows if x['disclosed']]==expected[key]['pairs'],'Compared with independently declared small report mask.')
 reports.append({'id':'g'+key,'units':UNITS,'grades':g,'blocks_high_priority_first':blocks,'G':len(blocks),'M':6,'N':N,'withheld_pairs':6-N,'disclosure_fraction':str(F(N,6)),'pairs':pair_rows})
grade={'fixture':'f09a-grade-pairs-v1','source':'chapters/09-targets-actions-laws.qmd#sec-grade-actions','units':UNITS,'pair_order':[''.join(UNITS[i]+UNITS[j]) for i,j in PAIRS],'orientation':'Smaller nonempty canonical grade label means higher reported priority.','reports':reports,'scope':'Deterministic reporting examples; no latent target values,probability law,risk or optimality is instantiated. Grade ties withhold directions,not assert equality.'};PATHS[0].write_text(json.dumps(grade,indent=2)+'\n')
laws={'Q1':[(0,1),(1,2),(2,0)],'Q2':[(0,2),(1,0),(2,1)]};rows=[];summaries=[]
for name,states in laws.items():
 mass={s:F(1,3) for s in states};total=sum(mass.values());ma={a:sum(p for (x,y),p in mass.items() if x==a) for a in range(3)};mb={b:sum(p for (x,y),p in mass.items() if y==b) for b in range(3)}
 check('total_probability_'+name,total==1,'Three distinct support states of mass1/3.')
 check('uniform_marginals_'+name,all(p==F(1,3) for p in list(ma.values())+list(mb.values())),'Each support value0,1,2 occurs once in each coordinate.')
 greater=sum(p for (a,b),p in mass.items() if a>b);equal=sum(p for (a,b),p in mass.items() if a==b);less=sum(p for (a,b),p in mass.items() if a<b)
 check('event_partition_'+name,greater+equal+less==1 and equal==0,'Strict comparison events partition each stipulated tie-free joint law.')
 check('above_region_'+name,greater==F(sum(a>b for a,b in states),3)==(F(1,3) if name=='Q1' else F(2,3)),'State-mass sum versus number of equally weighted support states in A>B region.')
 for a,b in product(range(3),repeat=2):rows.append({'law':name,'A':a,'B':b,'probability':str(mass.get((a,b),F(0))),'event_A_gt_B':int(a>b),'event_A_eq_B':int(a==b),'event_A_lt_B':int(a<b),'marginal_A_at_value':str(ma[a]),'marginal_B_at_value':str(mb[b])})
 summaries.append({'law':name,'support':[{'A':a,'B':b,'probability':'1/3'} for a,b in states],'marginal_A':{str(k):str(v) for k,v in ma.items()},'marginal_B':{str(k):str(v) for k,v in mb.items()},'P_A_gt_B':str(greater),'P_A_eq_B':str(equal),'P_A_lt_B':str(less)})
check('same_marginals_across_laws',summaries[0]['marginal_A']==summaries[1]['marginal_A'] and summaries[0]['marginal_B']==summaries[1]['marginal_B'],'Marginal equality does not force event probability equality.')
with PATHS[1].open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
meta={'fixture':'f09b-couplings-v1','source':'chapters/09-targets-actions-laws.qmd#sec-posterior-risk-laws','coordinate_file':'f09-couplings.csv','coordinate_sha256':sha(PATHS[1]),'laws':summaries,'cell_semantics':'All18law/cell combinations are explicit probabilities; absent support cells have stipulated probability0,not missing observations.','recommended_axes':{'x':'A,values0/1/2','y':'B,values0/1/2','A_gt_B_region':'Below the diagonal y=x when A is horizontal and B vertical.'},'scope':'Two stipulated exact finite laws,not estimated posteriors or observed samples. Independence would supply a third joint law and is not assumed here.'};PATHS[2].write_text(json.dumps(meta,indent=2)+'\n')
r={'step':'4.1','status':'PASS_SMALL_EXACT_COORDINATES','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'JoonHo Lee (jlee296@ua.edu)','scope':'One bounded exact coordinate derivation from the two canonical Chapter9 examples; not a new simulation campaign,figure production or general-proof audit.','source':{'path':'chapters/09-targets-actions-laws.qmd','sha256':sha(ROOT/'chapters/09-targets-actions-laws.qmd')},'checks':checks,'check_count':len(checks),'all_passed':True,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in PATHS[:3]],'derivation_source':{'path':'assets/reproduction/figures/data/derive_f09_coordinates.py','sha256':sha(Path(__file__))},'execution':{'python':platform.python_version(),'derivation_runs':1,'exact_arithmetic':'fractions.Fraction and integer pair counts','random_draws':0,'plots_generated':0,'package_or_optimizer_runs':0,'canonical_or_register_edits':0}};REVIEW.parent.mkdir(exist_ok=True,parents=True);REVIEW.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'checks':len(checks),'grade_reports':len(reports),'coupling_rows':len(rows),'outputs':r['outputs']},indent=2))
