#!/usr/bin/env python3
"""Exact stationary two-state variance comparison; no chain is simulated."""
from pathlib import Path
from fractions import Fraction as F
import csv, json, hashlib, datetime, sys, argparse
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
ROOT=fs.ROOT
HERE=Path(__file__).resolve()
DATA=BASE/'data/markov-bound-coordinates.csv'
META=BASE/'data/markov-bound-metadata.json'
STEM='f15b-stationarity-does-not-supply-iid-precision'
RECEIPT=ROOT/'evidence/figures/builds/F15b.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def analytic_coordinates():
 meta=json.loads(META.read_text())
 assert sha(DATA)==meta['coordinate_sha256']
 rows=[r for r in csv.DictReader(DATA.open()) if r['series']=='stationary_markov']
 expected_S=[1,2,5,10,20,50,100,200,500]
 assert [int(r['S']) for r in rows]==expected_S
 assert meta['series']['stationary_markov']['S_grid']==expected_S
 result=[]
 for row in rows:
  n=int(row['S']);rho=F(49,50)
  variance=(n+2*sum((n-h)*rho**h for h in range(1,n)))/(4*n*n)
  expected={'stay_probability':F(99,100),'switch_probability':F(1,100),'lag_correlation':rho,
            'no_switch_probability':F(99,100)**(n-1),'markov_mean_variance':variance,
            'iid_mean_variance':F(1,4*n),'finite_variance_equivalent_count':F(1,4)/variance,
            'asymptotic_equivalent_count':F(n,99),'markov_to_iid_variance_ratio':variance/F(1,4*n)}
  residual={key:float(abs(F(row[key])-value)) for key,value in expected.items()}
  assert all(abs(F(row[key])-value)<=F(1,10**16)*max(F(1),abs(value)) for key,value in expected.items())
  result.append({'S':n,**{k:float(v) for k,v in expected.items()},'status':'PASS_EXACT_COVARIANCE_SUM_VS_ROUNDED_CSV','max_absolute_rounding_difference':max(residual.values())})
 return result


def draw(rows,mobile):
 fig=fs.canvas(4.8 if mobile else 11.2,15.5 if mobile else 8.7,mobile)
 ink,teal,rust,muted=(fs.PALETTE[k] for k in ['ink','teal','rust','muted'])
 ftexts=[];panelpairs=[]
 def ft(x,y,text,size=14,**kw):
  t=fig.text(x,y,text,ha='left',va='top',fontsize=size,linespacing=1.25,**kw);ftexts.append(t);return t
 ft(.04,.982,'Stationarity does not supply\nindependent-draw precision' if mobile else 'Stationarity does not supply independent-draw precision',16,fontweight='semibold')
 ft(.04,.925 if mobile else .90,'Known stationary law.\nAll calculations are analytic.' if mobile else 'Known stationary law; all calculations are analytic. No path was simulated.',14 if mobile else 13)
 ax=fig.add_axes([.19,.61,.76,.245] if mobile else [.09,.31,.51,.49])
 S=[r['S'] for r in rows];v=[r['markov_mean_variance'] for r in rows];iid=[r['iid_mean_variance'] for r in rows]
 ax.loglog(S,v,'o-',color=teal,linewidth=2,markersize=5,zorder=3)
 ax.loglog(S,iid,'s--',color=rust,linewidth=1.7,markersize=4,zorder=3)
 ax.set_xlim(.8,700);ax.set_ylim(.00035,.42)
 ax.xaxis.set_major_locator(FixedLocator([1,10,100,500]));ax.xaxis.set_major_formatter(FixedFormatter(['1','10','100','500']))
 ax.yaxis.set_major_locator(FixedLocator([.001,.01,.1]));ax.yaxis.set_major_formatter(FixedFormatter(['0.001','0.01','0.1']))
 ax.xaxis.set_minor_locator(NullLocator());ax.yaxis.set_minor_locator(NullLocator())
 ax.set_xlabel('Consecutive states, S',fontsize=14 if mobile else 12.5,labelpad=8)
 ax.set_ylabel('Variance of sample proportion',fontsize=14 if mobile else 12.5,labelpad=8)
 fs.clean(ax)
 plotlabels=[]
 plotlabels.append(ax.annotate('Markov',xy=(500,v[-1]),xytext=(210,.22),textcoords='data',ha='left',va='bottom',color=teal,fontsize=14 if mobile else 12.5,fontweight='semibold',arrowprops={'arrowstyle':'-','color':muted,'linewidth':.8}))
 plotlabels.append(ax.annotate('IID reference',xy=(500,iid[-1]),xytext=(12,.00055),textcoords='data',ha='left',va='bottom',color=rust,fontsize=14 if mobile else 12.5,arrowprops={'arrowstyle':'-','color':muted,'linewidth':.8}))
 at100=next(r for r in rows if r['S']==100)
 ax.axvline(100,color=fs.PALETTE['gray'],linewidth=1,linestyle=':',zorder=1)
 ax.scatter([100,100],[at100['markov_mean_variance'],at100['iid_mean_variance']],s=60,facecolors='none',edgecolors=ink,linewidths=1.2,zorder=4)
 plotlabels.append(ax.annotate('S = 100',xy=(100,.30),xytext=(0,0),textcoords='offset points',ha='center',va='center',fontsize=13 if mobile else 11.5))
 if not mobile:ft(.09,.84,'Exact finite-length variance',14,fontweight='semibold')
 def card(rect):
  a=fs.diagram_axis(fig,rect);p=FancyBboxPatch((.008,.008),.984,.984,boxstyle='round,pad=0,rounding_size=0.02',facecolor='white',edgecolor=fs.PALETTE['line'],linewidth=1)
  a.add_patch(p);return a,p
 def tx(a,p,x,y,label,size=14,**kw):
  t=a.text(x,y,label,ha=kw.pop('ha','left'),va='center',fontsize=size,linespacing=1.2,**kw);panelpairs.append((p,t));return t
 matrix,mp=card([.04,.405,.92,.155] if mobile else [.66,.64,.30,.20])
 size=14 if mobile else 12
 tx(matrix,mp,.055,.88,'Known transition law',15 if mobile else 13.5,fontweight='semibold')
 for x,text in [(.16,'From'),(.55,'Next 0'),(.82,'Next 1')]:tx(matrix,mp,x,.69,text,size,ha='center',fontweight='semibold')
 for y,state,p0,p1 in [(.51,'0','0.99','0.01'),(.33,'1','0.01','0.99')]:
  for x,text in [(.16,state),(.55,p0),(.82,p1)]:tx(matrix,mp,x,y,text,size,ha='center')
 tx(matrix,mp,.055,.13,'Initial P(0) = P(1) = 1/2',14 if mobile else 11.5)
 metrics,cp=card([.04,.15,.92,.22] if mobile else [.66,.25,.30,.34])
 tx(metrics,cp,.055,.9,'At S = 100',15 if mobile else 13.5,fontweight='semibold')
 labels=[('Markov variance',f"{at100['markov_mean_variance']:.5f}"),('IID variance',f"{at100['iid_mean_variance']:.5f}"),('Finite equivalent count',f"{at100['finite_variance_equivalent_count']:.3f}"),('Asymptotic expression',f"{at100['asymptotic_equivalent_count']:.3f}"),('No-switch probability',f"{at100['no_switch_probability']:.5f}")]
 for y,(label,value) in zip([.73,.59,.45,.31,.17],labels):
  tx(metrics,cp,.055,y,label,14 if mobile else 11.5)
  tx(metrics,cp,.95,y,value,14 if mobile else 12,ha='right',fontweight='semibold')
 ft(.04,.105 if mobile else .14,
    'Counts compare variance only.\nNeither is estimated ESS or an IID tail bound.\nMarkers: nine integer sample lengths.\nSegments guide the eye; no path simulated.' if mobile else
    'Equivalent counts compare variance only; neither is estimated ESS or an IID tail certificate.\nMarkers are nine integer sample lengths; connecting segments guide the eye. No path was simulated.',
    13.5 if mobile else 12,color=muted)
 fig.canvas.draw();ren=fig.canvas.get_renderer();checks=[]
 for patch,t in panelpairs:
  bb=t.get_window_extent(ren);pb=patch.get_window_extent(ren)
  ok=bb.x0>=pb.x0+1 and bb.x1<=pb.x1-1 and bb.y0>=pb.y0+1 and bb.y1<=pb.y1-1
  checks.append({'text':t.get_text(),'inside_panel':bool(ok)})
 alltexts=ftexts+[t for _,t in panelpairs]+plotlabels+[ax.xaxis.label,ax.yaxis.label]+ax.get_xticklabels()+ax.get_yticklabels()
 canvas=[]
 for t in alltexts:
  bb=t.get_window_extent(ren);inside=bb.x0>=1 and bb.x1<=fig.bbox.width-1 and bb.y0>=1 and bb.y1<=fig.bbox.height-1
  canvas.append({'text':t.get_text(),'inside':bool(inside)})
 overlaps=[]
 for i,t in enumerate(alltexts):
  for u in alltexts[i+1:]:
   if t.get_window_extent(ren).overlaps(u.get_window_extent(ren)):overlaps.append([t.get_text(),u.get_text()])
 if not all(c['inside_panel'] for c in checks):raise RuntimeError('Panel text outside: '+str([c for c in checks if not c['inside_panel']]))
 if not all(c['inside'] for c in canvas):raise RuntimeError('Canvas text outside: '+str([c for c in canvas if not c['inside']]))
 if overlaps:raise RuntimeError('Text overlap: '+str(overlaps))
 files=fs.export(fig,STEM,mobile)
 return files,{'mobile':mobile,'panel_containment_checks':checks,'canvas_containment_checks':canvas,'all_pass':True,'pairwise_text_nonoverlap':True,'plotted_integer_sample_lengths':S,'minimum_mobile_font_pt':13.5 if mobile else None}


def main(overwrite=False):
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (RECEIPT.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; overwrite only for an observed authorized repair.')
 old=json.loads(RECEIPT.read_text()) if RECEIPT.exists() else {}
 rows=analytic_coordinates();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 attempt={'started_at_utc':started,'command':'python -B assets/reproduction/figures/generators/F15b/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_exports':0,'layout_exports':0}
 history=old.get('execution_history',[])+[attempt]
 record={'id':'F15b','step':'5.9','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':started,'status':'RENDERING','scope':'Nine exact known-law covariance sums and derived metrics checked against accepted rounded coordinates; no chain, model or optimizer run.','coordinate_selector':'series=stationary_markov only','inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in [DATA,META,BASE/'figstyle.py',HERE]],'analytic_coordinate_checks':rows,'execution_history':history,'actual_image_views':old.get('actual_image_views',[]),'repairs':old.get('repairs',[]),'previous_output_history':old.get('previous_output_history',[]),'notes':['Initial state stationary; no initialization error in this construction.','Finite equivalent count is (1/4)/Var(meanX); asymptotic expression is S/99. Neither is estimated ESS or an IID tail replacement.','No-switch probability is a named event, not the full tail failure distribution.','Only nine integer S markers are analytic sample lengths; connecting segments are visual guides.'],'publication_and_licenses':'Deferred'}
 RECEIPT.parent.mkdir(parents=True,exist_ok=True)
 try:
  files=[];geometry=[]
  for mobile in [False,True]:
   out,geo=draw(rows,mobile);files+=out;geometry.append(geo);attempt['asset_exports']+=3;attempt['layout_exports']+=1
  record['outputs']=files;record['geometry_checks']=geometry;record['status']='exported';attempt['status']='succeeded'
 except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='RENDER_FAILED';raise
 finally:
  attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
  record['execution']={'production_command_attempts_total':len(history),'completed_renderer_commands':sum(a['status']=='succeeded' for a in history),'failed_renderer_commands':sum(a['status']=='failed' for a in history),'asset_writes_total':sum(a['asset_exports'] for a in history),'layout_exports_total':sum(a['layout_exports'] for a in history),'analytic_coordinate_check_invocations_total':len(history),'chain_simulations':0,'model_runs':0,'optimizer_runs':0,'public_coordinate_writes':0,'canonical_or_registry_edits':0}
  RECEIPT.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'id':'F15b','outputs':record.get('outputs',[]),'attempts':len(history)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
