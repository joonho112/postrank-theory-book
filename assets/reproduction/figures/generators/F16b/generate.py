#!/usr/bin/env python3
"""Exact three-case denominator example; distinct aggregation estimands.
All scientific inputs are public coordinates. The silent case retains NA.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
ROOT=fs.ROOT;HERE=Path(__file__).resolve();DATA=BASE/'data/f16b-disclosed-error-ratios.json'
DEST=ROOT/'evidence/figures/builds/F16b.json';STEM='f16b-ratios-average-different-things'


def coordinates():
 d=json.loads(DATA.read_text());assert d['n']==3 and d['M']==3 and d['K']==1 and F(d['criterion_weight'])==1
 checks=[]
 for row in d['cases']:
  theta,g=row['theta'],row['g'];directions=[(i,j) for i in range(3) for j in range(3) if g[i]<g[j]]
  n=len(directions);a=sum(theta[i]<=theta[j] for i,j in directions)
  assert (a,n)==(row['A'],row['N']) and F(row['probability'])==F(1,3)
  assert row['disclosed_error_fraction']==(str(F(a,n)) if n else None)
  assert F(row['disclosure_fraction'])==F(n,3)
  checks.append({'case':row['Y'],'A':a,'N':n,'fraction':row['disclosed_error_fraction'],'status':'PASS'})
 assert [(r['A'],r['N']) for r in d['cases']]==[(2,2),(0,3),(0,0)]
 ea=sum(F(r['probability'])*r['A'] for r in d['cases']);en=sum(F(r['probability'])*r['N'] for r in d['cases'])
 positive=sum(F(r['probability']) for r in d['cases'] if r['N'])
 nonsilent=sum(F(r['probability'])*F(r['A'],r['N']) for r in d['cases'] if r['N'])/positive
 imputed=sum(F(r['probability'])*(F(r['A'],r['N']) if r['N'] else 0) for r in d['cases'])
 agg=d['aggregation'];assert ea/en==F(agg['pooled']['value'])==F(2,5)
 assert nonsilent==F(agg['nonsilent_mean']['value'])==F(1,2)
 assert imputed==F(agg['zero_imputed_mean']['value'])==F(1,3)==positive*nonsilent
 assert positive==F(2,3)==F(agg['positive_disclosure_probability']) and en/3==F(agg['mean_disclosure_fraction'])==F(5,9)
 rateweights=[F(r['probability'])*r['N']/en for r in d['cases']]
 assert rateweights==list(map(F,agg['pooled']['nonsilent_outcome_rate_weights']))==[F(2,5),F(3,5),0]
 return d,{'cases':checks,'expected_A':str(ea),'expected_N':str(en),'pooled':str(ea/en),'nonsilent_mean':str(nonsilent),'zero_imputed_mean':str(imputed),'rate_weights':list(map(str,rateweights)),'positive_frequency':str(positive),'mean_N_over_M':str(en/3),'silent_original_fraction':d['cases'][2]['disclosed_error_fraction']}


def draw(d,mobile):
 fig=fs.canvas(4.8 if mobile else 10.8,18.6 if mobile else 10.4,mobile)
 fig.text(.04,.985,'Ratios average\ndifferent things' if mobile else 'Ratios average different things',ha='left',va='top',fontsize=16,fontweight='semibold',linespacing=1.2)
 fig.text(.04,.925,'Three equally probable dataset cases.\nOne criterion; three units; M = 3.' if mobile else 'Three equally probable dataset cases; one criterion, three units, M = 3.',ha='left',va='top',fontsize=14 if mobile else 12.5,linespacing=1.25)
 ax=fs.diagram_axis(fig,[.03,.11,.94,.80]);containers={};texts=[]
 def panel(key,rect,emphasis=False):
  patch=FancyBboxPatch(rect[:2],rect[2],rect[3],boxstyle='round,pad=0.003,rounding_size=0.008',facecolor='white',edgecolor=fs.PALETTE['teal'] if emphasis else fs.PALETTE['line'],linewidth=1.1,zorder=1)
  ax.add_patch(patch);containers[key]=patch;return rect
 def tx(key,role,rect,xx,yy,label,size,weight='normal',color=None,align='center'):
  x,y,w,h=rect;t=ax.text(x+w*xx,y+h*yy,label,ha=align,va='center',fontsize=size,fontweight=weight,color=color or fs.PALETTE['ink'],zorder=3,linespacing=1.2);texts.append((key,role,t));return t
 for i,row in enumerate(d['cases']):
  rect=(.015,[.84,.685,.53][i],.97,.135) if mobile else (.01+i*.335,.735,.31,.24)
  key='case'+str(row['Y']);panel(key,rect)
  tx(key,'case probability',rect,.5,.86,'Case '+str(row['Y'])+':  P = 1/3',15 if mobile else 14,'semibold')
  tx(key,'coherent report',rect,.5,.68,'g = ('+', '.join(map(str,row['g']))+')',14 if mobile else 13)
  tx(key,'counts',rect,.5,.49,'(A, N) = ('+str(row['A'])+', '+str(row['N'])+')',15,'semibold')
  rate='A/N: NA\nNo disclosure' if row['N']==0 else 'A/N = '+row['disclosed_error_fraction']
  tx(key,'individual fraction',rect,.5,.30,rate,15 if row['N']==0 else 16,'semibold',fs.PALETTE['muted'] if row['N']==0 else fs.PALETTE['ink'])
  tx(key,'disclosure',rect,.5,.12,'N/M = '+row['disclosure_fraction'],14 if mobile else 12.5)
 if not mobile:ax.text(.5,.697,'Three summaries of the same stipulated law',ha='center',va='center',fontsize=13.5,fontweight='semibold')
 rows=[('pooled','Pool counts',r'$(2+0+0)/(2+3+0)=2/5$','Rate weights: (2/5, 3/5, 0).','Silent case contributes zero counts.'),
       ('nonsilent','Average nonsilent rates',r'$(1+0)/2=1/2$','Conditional weights: (1/2, 1/2).','Exclude silence; keep its rate NA.'),
       ('imputed','Impute zero, then average',r'$(1+0+0)/3=1/3$','Case weights: (1/3, 1/3, 1/3).','Extra convention: NA → 0.')]
 for i,(key,title,formula,weights,note) in enumerate(rows):
  rect=(.015,[.35,.18,.01][i],.97,.15) if mobile else (.015,[.47,.25,.03][i],.97,.19)
  panel(key,rect)
  if mobile:
   tx(key,'operation',rect,.5,.84,title,15,'semibold')
   tx(key,'formula',rect,.5,.61,formula,16)
   tx(key,'weights',rect,.5,.37,weights,14)
   tx(key,'meaning',rect,.5,.14,note,14,'semibold' if key=='imputed' else 'normal')
  else:
   tx(key,'operation',rect,.03,.72,title,14,'semibold',align='left')
   tx(key,'formula',rect,.73,.72,formula,16)
   tx(key,'weights',rect,.03,.28,weights,12.5,align='left')
   tx(key,'meaning',rect,.73,.28,note,12.5,'semibold' if key=='imputed' else 'normal')
 fig.text(.04,.025,'P(N > 0) = 2/3; mean N/M = 5/9.\nA/N is undefined when N = 0.\nDifferent estimands and weights.' if mobile else
          'Positive-disclosure frequency: 2/3; mean disclosure N/M: 5/9. The silent fraction stays undefined.\nThese are different estimands and weighting conventions, not competing estimates of one quantity.',ha='left',va='bottom',fontsize=14 if mobile else 11.5,color=fs.PALETTE['muted'],linespacing=1.25)
 fig.canvas.draw();ren=fig.canvas.get_renderer();checks=[]
 for key,role,t in texts:
  bb=t.get_window_extent(ren);rb=containers[key].get_window_extent(ren);checks.append({'container':key,'role':role,'font_pt':t.get_fontsize(),'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)})
 if not all(c['inside'] for c in checks):raise RuntimeError('Card clipping: '+str([c for c in checks if not c['inside']]))
 alltext=list(ax.texts)+list(fig.texts)
 for i,t in enumerate(alltext):
  bb=t.get_window_extent(ren)
  if not(bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
  for u in alltext[i+1:]:
   if bb.overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,18.6] if mobile else [10.8,10.4],'card_text_containment':checks,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,'original_silent_card':'A/N: NA; no disclosure','imputation_is_separately_labelled':True,'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}


def generate(overwrite=False):
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite is for an authorized observed repair.')
 old=json.loads(DEST.read_text()) if DEST.exists() else None;d,checks=coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/F16b/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_exports':0};history=(old or {}).get('execution_history',[])+[attempt]
 record={'id':'F16b','step':'6.9','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':history,'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in [DATA,BASE/'figstyle.py',HERE]],'exact_checks':checks,'actual_image_views':(old or {}).get('actual_image_views',[]),'scope':'Exact population-case aggregation check and deterministic figure rendering; no model,simulation,optimizer or empirical sampling.','scientific_boundaries':['A is weak-error count in a one-criterion stipulated joint evaluation law.','Silent A/N remains NA; zero imputation is an explicit separate convention.','Pooled and conditional means are different estimands and weights.','No finite-ratio unbiasedness or independent-pair sampling claim.'],'limits':['Independent semantic/color/PDF/final chapter context acceptance remain separate.','Only public data/style/source are scientific runtime inputs.'],'publication_and_licenses':'Deferred','required_repairs_remaining':[]}
 if old:record['previous_output_history']=old.get('previous_output_history',[])+[{'outputs':old.get('outputs',[])}]
 DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
 try:
  outputs=[];geometry=[]
  for mobile in [False,True]:
   files,g=draw(d,mobile);outputs.extend(files);geometry.append(g);attempt['layout_exports']+=1;attempt['asset_exports']+=3
  assert [o['path'] for o in outputs]==[str(p.relative_to(ROOT)) for p in targets]
  record['outputs']=outputs;record['geometry_checks']=geometry;record['status']='rendered';attempt['status']='succeeded'
 except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
 finally:
  attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record['execution']={'python':platform.python_version(),'renderer_invocations_total':len(history),'last_command_invocations':1,'layout_exports_total':sum(x['layout_exports'] for x in history),'asset_writes_total':sum(x['asset_exports'] for x in history),'model_runs':0,'simulation_runs':0,'optimizer_runs':0,'canonical_edits':0,'register_edits':0};DEST.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'id':'F16b','outputs':outputs,'geometry':'PASS','renderer_commands_total':len(history)},indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
