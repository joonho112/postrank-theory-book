#!/usr/bin/env python3
"""Exact weight sensitivity and fixed-included-criterion minimax comparison."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle
ROOT=fs.ROOT;HERE=Path(__file__).resolve();DATA=BASE/'data/transformations-protections.json'
DEST=ROOT/'evidence/figures/builds/F13b.json';STEM='f13b-weights-change-an-optimal-reporting-action'
# Exact structured reading of the law stated in the selected public JSON and
# Chapter13's 'One exact comparison as weights change'. These are fixed states,
# not simulated observations or additional fitted numerical inputs.
STATES=[([1,1],[0,0],F(1,2)),([1,-1],[0,0],F(1,2))]


def coordinates():
 d=json.loads(DATA.read_text())['weight_sensitivity'];tau=F(d['tau'])
 assert tau==F(1,4) and d['included_minimax_criteria']==[1,2] and d['omega_domain']==['0','1']
 assert sum(s[2] for s in STATES)==1
 vectors={}
 for action in ['A>B','B>A','withhold']:
  if action=='withhold':v=[tau,tau]
  else:
   v=[sum(p*((a[k]<=b[k]) if action=='A>B' else (b[k]<=a[k])) for a,b,p in STATES) for k in range(2)]
  line=d['lines'][action]
  assert F(line['intercept'])==v[1] and F(line['slope'])==v[0]-v[1]
  assert F(line['minimax'])==max(v)
  vectors[action]=v
 assert vectors=={'A>B':[0,F(1,2)],'B>A':[1,F(1,2)],'withhold':[tau,tau]}
 rows=[]
 for omega in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
  values={a:omega*v[0]+(1-omega)*v[1] for a,v in vectors.items()}
  minimum=min(values.values());opt=[a for a,v in values.items() if v==minimum]
  expected=['withhold'] if omega<F(1,2) else ['A>B'] if omega>F(1,2) else ['A>B','withhold']
  assert opt==expected and 'B>A' not in opt
  rows.append({'omega':str(omega),'weighted_risks':{a:str(v) for a,v in values.items()},'full_minimizing_set':opt})
 # Affine differences establish the intervals, rather than only sampled points.
 assert F(1,2)-tau==F(1,4)
 assert min(F(d['lines']['B>A']['intercept']),F(d['lines']['B>A']['intercept'])+F(d['lines']['B>A']['slope']))>tau
 maxima={a:max(v) for a,v in vectors.items()}
 assert [a for a,v in maxima.items() if v==min(maxima.values())]==['withhold']
 return d,vectors,{'states':[{'A':a,'B':b,'probability':str(p)} for a,b,p in STATES],
        'criterion_risks':{a:list(map(str,v)) for a,v in vectors.items()},'checked_weight_coordinates':rows,
        'continuous_switch_proof':'R_forward-R_hold=1/4-omega/2; changes sign only atomega1/2. R_reverse>=1/2>1/4 throughout[0,1].',
        'fixed_minimax_criteria':[1,2],'criterion_maxima':{a:str(v) for a,v in maxima.items()},'unique_minimax_action':'withhold'}


def plot(ax,d,mobile):
 x=[0,.25,.5,.75,1];styles={'A>B':(fs.PALETTE['teal'],'-'),'B>A':(fs.PALETTE['rust'],(0,(5,3))),'withhold':(fs.PALETTE['ochre'],(0,(1,2)))}
 for name,(color,ls) in styles.items():
  line=d['lines'][name];ax.plot(x,[float(F(line['intercept'])+F(str(z))*F(line['slope'])) for z in x],color=color,ls=ls,lw=1.8,zorder=2)
 ax.plot([0,.5],[.25,.25],color=styles['withhold'][0],ls=styles['withhold'][1],lw=4,zorder=3)
 ax.plot([.5,1],[.25,0],color=styles['A>B'][0],ls='-',lw=4,zorder=3)
 ax.vlines(.5,0,.25,color=fs.PALETTE['gray'],ls=(0,(2,3)),lw=1,zorder=1)
 ax.scatter([.5],[.25],s=80,facecolor='white',edgecolor=fs.PALETTE['ink'],lw=1.5,zorder=5)
 for xx,yy,name in [(.62,.88,'B>A'),(.74,.17,'A>B'),(.05,.30,'Hold')]:
  key='withhold' if name=='Hold' else name
  ax.text(xx,yy,name,fontsize=14 if mobile else 12.5,color=styles[key][0],ha='left',va='bottom',bbox={'facecolor':'white','edgecolor':'none','pad':1})
 ax.set(xlim=(0,1),ylim=(0,1));ax.set_xticks([0,.5,1],['0','1/2','1']);ax.set_yticks([0,.25,.5,1],['0','1/4','1/2','1'])
 ax.tick_params(labelsize=14 if mobile else 11.5)
 ax.set_xlabel('Weight ω on criterion 1',fontsize=14 if mobile else 12.5,labelpad=8)
 ax.set_ylabel('Weighted risk (M = 1)',fontsize=14 if mobile else 12.5,labelpad=9)
 fs.clean(ax)


def draw(d,vectors,mobile):
 fig=fs.canvas(4.8 if mobile else 10.8,15.2 if mobile else 8.5,mobile)
 fig.text(.04,.985,'Weights change the\nselected report' if mobile else 'Weights change the selected report',ha='left',va='top',fontsize=16,fontweight='semibold',linespacing=1.2)
 fig.text(.04,.925 if mobile else .91,
          'Each state has probability 1/2:\n(A, B) = ((1, 1), (0, 0))\nor ((1, −1), (0, 0)).' if mobile else
          'Fixed law: each of ((1, 1), (0, 0)) and ((1, −1), (0, 0)) has probability 1/2.',
          ha='left',va='top',fontsize=14 if mobile else 12.5,linespacing=1.25)
 p=fig.add_axes([.20,.565,.72,.245] if mobile else [.095,.40,.43,.40]);plot(p,d,mobile)
 if mobile:
  fig.text(.08,.505,'Thick segments: minimum weighted risk',ha='left',va='top',fontsize=14,color=fs.PALETTE['muted'])
  strip=fs.diagram_axis(fig,[.08,.425,.84,.055])
  fig.text(.08,.400,'At ω = 1/2: both Hold and A>B minimize.',ha='left',va='top',fontsize=14)
  table=fs.diagram_axis(fig,[.035,.155,.93,.215])
 else:
  fig.text(.095,.325,'Thick segments: minimum weighted risk',ha='left',va='top',fontsize=11.5,color=fs.PALETTE['muted'])
  strip=fs.diagram_axis(fig,[.095,.22,.43,.07])
  fig.text(.095,.18,'At ω = 1/2: both Hold and A>B minimize.',ha='left',va='top',fontsize=12.5)
  table=fs.diagram_axis(fig,[.60,.29,.365,.50])
 for x,w,label,color in [(0,.5,'Hold\nω < 1/2',fs.PALETTE['ochre']),(.5,.5,'A>B\nω > 1/2',fs.PALETTE['teal'])]:
  strip.add_patch(Rectangle((x,.05),w,.9,facecolor=fs.PALETTE['light'],edgecolor=color,lw=1.2))
  strip.text(x+w/2,.5,label,ha='center',va='center',fontsize=14 if mobile else 12.5,linespacing=1.2)
 size=14 if mobile else 12.5
 table.text(.02,.97,'Expected-criterion minimax',ha='left',va='top',fontsize=15 if mobile else 14,fontweight='semibold')
 table.text(.02,.82,'Included criteria fixed at {1, 2}',ha='left',va='center',fontsize=size)
 for xx,label in [(.14,'Report'),(.46,'R₁'),(.66,'R₂'),(.86,'Max')]:table.text(xx,.66,label,ha='center',va='center',fontsize=size,fontweight='semibold')
 cellchecks=[]
 for name,yy in [('A>B',.49),('B>A',.33),('withhold',.17)]:
  if name=='withhold':table.add_patch(Rectangle((.015,yy-.065),.97,.13,facecolor=fs.PALETTE['light'],edgecolor=fs.PALETTE['teal'],lw=1.5))
  table.text(.14,yy,'Hold' if name=='withhold' else name,ha='center',va='center',fontsize=size,fontweight='semibold' if name=='withhold' else 'normal')
  for xx,value in zip([.46,.66,.86],vectors[name]+[max(vectors[name])]):
   rect=Rectangle((xx-.085,yy-.06),.17,.12,facecolor='none',edgecolor=fs.PALETTE['line'],lw=.7);table.add_patch(rect)
   t=table.text(xx,yy,str(value),ha='center',va='center',fontsize=15 if mobile else 13.5,fontweight='semibold' if name=='withhold' else 'normal');cellchecks.append((name,rect,t))
 table.text(.02,.035,'Unique minimax action: Hold',ha='left',va='center',fontsize=size,fontweight='semibold',color=fs.PALETTE['teal'])
 fig.text(.04,.10 if mobile else .105,'w = (ω, 1−ω); τ = 1/4; M = 1.\nAll three reports remain available.' if mobile else
          'w = (ω, 1−ω); τ = 1/4; M = 1. All three reports remain available.',ha='left',va='top',fontsize=14 if mobile else 12.5,linespacing=1.25)
 fig.text(.04,.025,
          'Both criteria remain in minimax at ω = 1.\nThe weight switch changes preferences,\nwhile the target law stays fixed.' if mobile else
          'Both criteria remain in minimax at ω = 1. The weight switch changes declared preferences while the target law stays fixed.',
          ha='left',va='bottom',fontsize=14 if mobile else 11.5,linespacing=1.25,color=fs.PALETTE['muted'])
 fig.canvas.draw();ren=fig.canvas.get_renderer();checks=[]
 for name,rect,t in cellchecks:
  bb=t.get_window_extent(ren);rb=rect.get_window_extent(ren);checks.append({'action':name,'cell':t.get_text(),'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)})
 if not all(c['inside'] for c in checks):raise RuntimeError('Table cell clipping: '+str(checks))
 alltext=list(p.texts)+[p.xaxis.label,p.yaxis.label]+list(p.get_xticklabels())+list(p.get_yticklabels())+list(strip.texts)+list(table.texts)+list(fig.texts)
 for i,t in enumerate(alltext):
  bb=t.get_window_extent(ren)
  if not(bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
  for u in alltext[i+1:]:
   if bb.overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,15.2] if mobile else [10.8,8.5],
         'minimax_cell_containment':checks,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,
         'axes_limits':{'omega':[0,1],'risk':[0,1]},'cooptimal_boundary':'omega1/2: A>B and withhold',
         'included_minimax_criteria':[1,2],'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}


def generate(overwrite=False):
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite requires an authorized recorded repair.')
 old=json.loads(DEST.read_text()) if DEST.exists() else None;d,vectors,checks=coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/F13b/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_exports':0}
 history=(old or {}).get('execution_history',[])+[attempt]
 record={'id':'F13b','step':'4.17','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':history,
         'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in [DATA,BASE/'figstyle.py',HERE]],'coordinate_selector':'weight_sensitivity only, with the public generator explicitly transcribing its two-state law into structured exact states.','exact_checks':checks,
         'actual_image_views':(old or {}).get('actual_image_views',[]),'scope':'Exact two-state risk derivation and five affine-coordinate checks,continuous sign argument and figure rendering; no model,simulation,optimizer or package run.',
         'scientific_boundaries':['Weights are preference settings,not target-law probabilities.','Both boundary minimizers are retained; reverse never minimizes in the unchanged three-action family.','Minimax takes the maximum of two criterion expectations with included set fixed at{1,2},including omega1.','The lower envelope compares discrete reports; no continuous report action or sampling guarantee is asserted.'],
         'limits':['Only public coordinate/style/source are required as scientific runtime inputs.'],'publication_and_licenses':'Deferred','required_repairs_remaining':[]}
 if old:record['previous_output_history']=old.get('previous_output_history',[])+[{'outputs':old.get('outputs',[])}]
 DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
 try:
  outputs=[];geometry=[]
  for mobile in [False,True]:
   out,g=draw(d,vectors,mobile);outputs.extend(out);geometry.append(g);attempt['layout_exports']+=1;attempt['asset_exports']+=3
  assert [o['path'] for o in outputs]==[str(p.relative_to(ROOT)) for p in targets]
  record['outputs']=outputs;record['geometry_checks']=geometry;record['status']='rendered';attempt['status']='succeeded'
 except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
 finally:
  attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record['execution']={'python':platform.python_version(),'renderer_invocations_total':len(history),'last_command_invocations':1,'layout_exports_total':sum(a['layout_exports'] for a in history),'asset_writes_total':sum(a['asset_exports'] for a in history),'model_runs':0,'simulation_runs':0,'optimizer_runs':0,'canonical_edits':0,'register_edits':0};DEST.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'id':'F13b','outputs':outputs,'geometry':'PASS','render_commands_total':len(history)},indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
