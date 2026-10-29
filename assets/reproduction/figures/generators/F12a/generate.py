#!/usr/bin/env python3
"""Known criterion opposition/composite equality, with exact affine costs.
Only frozen public coordinates and the shared public style are inputs.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle
ROOT=fs.ROOT;HERE=Path(__file__).resolve()
DATA=BASE/'data/f12a-co-primary-targets.json'
DEST=ROOT/'evidence/figures/builds/F12a.json'
STEM='f12a-composite-equality-and-criterion-opposition'


def coordinates():
 d=json.loads(DATA.read_text());theta=d['theta_AB'];a=list(map(F,d['a']));w=list(map(F,d['w']))
 assert theta==[[1,-1],[0,0]] and a==w==[F(1,2),F(1,2)] and d['M']==1
 composite=[sum(x*y for x,y in zip(a,t)) for t in theta]
 assert composite==list(map(F,d['composite_AB']))==[0,0]
 checks=[];lookup={}
 for r in d['costs']:
  if r['action']=='hold':
   intercept=F(0)
   coefficient=F(1) if r['loss']=='weak' else (F(composite[0]!=composite[1]) if r['target']=='composite' else sum(w[k]*(theta[0][k]!=theta[1][k]) for k in range(2)))
  else:
   i,j=(0,1) if r['action']=='A>B' else (1,0)
   bad=(lambda x,y:x<=y) if r['loss']=='weak' else (lambda x,y:x<y)
   intercept=F(bad(composite[i],composite[j])) if r['target']=='composite' else sum(w[k]*bad(theta[i][k],theta[j][k]) for k in range(2))
   coefficient=F(0)
  assert intercept==F(r['intercept']) and coefficient==F(r['tau_coefficient'])
  assert intercept+F(1,4)*coefficient==F(r['at_tau_1_4'])
  label='τ' if coefficient==1 and intercept==0 else str(intercept)
  lookup[(r['loss'],r['target'],r['action'])]=label
  checks.append({'loss':r['loss'],'target':r['target'],'action':r['action'],'intercept':str(intercept),'tau_coefficient':str(coefficient),'at_tau_1_4':str(intercept+F(1,4)*coefficient),'status':'PASS'})
 assert len(checks)==len(lookup)==12
 assert [lookup[('weak',t,'hold')] for t in ['composite','criterion']]==['τ','τ']
 assert [lookup[('neutral',t,'hold')] for t in ['composite','criterion']]==['0','τ']
 return d,lookup,checks


def draw(d,lookup,mobile):
 fig=fs.canvas(4.8 if mobile else 10.4,13.2 if mobile else 7.8,mobile)
 fig.text(.04,.98,'Composite equality,\ncriterion opposition' if mobile else 'Composite equality, criterion opposition',ha='left',va='top',fontsize=16,fontweight='semibold',linespacing=1.2)
 fig.text(.04,.925 if mobile else .915,'Known point mass; no uncertainty.' if mobile else 'Known point-mass targets; no estimation uncertainty.',ha='left',va='top',fontsize=14 if mobile else 12.5)
 plane=fig.add_axes([.18,.605,.73,.265] if mobile else [.095,.32,.31,.43])
 plane.set(xlim=(-.35,1.35),ylim=(-1.35,.35),aspect='equal')
 plane.plot([-.35,1.35],[.35,-1.35],color=fs.PALETTE['gray'],ls=(0,(5,3)),lw=1.5)
 plane.scatter([1],[-1],s=80,marker='o',color=fs.PALETTE['teal'],zorder=4)
 plane.scatter([0],[0],s=75,marker='s',facecolor='white',edgecolor=fs.PALETTE['ink'],lw=1.5,zorder=4)
 plane.annotate('A (1, −1)',(1,-1),xytext=(-70,-25),textcoords='offset points',fontsize=14 if mobile else 12.5)
 plane.annotate('B (0, 0)',(0,0),xytext=(9,10),textcoords='offset points',fontsize=14 if mobile else 12.5)
 plane.text(.52,-.39,'c = 0',fontsize=14 if mobile else 12.5,ha='center',va='center',bbox={'facecolor':'white','edgecolor':'none','pad':1.5})
 plane.set_xticks([0,1],['0','1']);plane.set_yticks([-1,0],['−1','0'])
 plane.tick_params(labelsize=14 if mobile else 11.5)
 plane.set_xlabel('Criterion 1: θ₁',fontsize=14 if mobile else 12.5,labelpad=7)
 plane.set_ylabel('Criterion 2: θ₂',fontsize=14 if mobile else 12.5,labelpad=7)
 plane.set_title('c = (θ₁ + θ₂)/2',fontsize=14 if mobile else 13.5,pad=12)
 fs.clean(plane,grid=None);plane.grid(color=fs.PALETTE['line'],lw=.6,alpha=.6)
 table=fs.diagram_axis(fig,[.035,.185,.93,.36] if mobile else [.48,.28,.485,.54])
 contain=[];cells=[]
 def tx(xx,yy,label,size=14,weight='normal',color=None):
  t=table.text(xx,yy,label,ha='center',va='center',fontsize=size,fontweight=weight,color=color or fs.PALETTE['ink'],zorder=3)
  return t
 for loss,y0,title in [('weak',.55,'Weak-error loss'),('neutral',.03,'Equality-neutral loss')]:
  h=.42
  tx(.5,y0+h*.94,title,15 if mobile else 14,'semibold')
  for xx,name in [(.14,'Report'),(.51,'Composite'),(.83,'Criteria')]:tx(xx,y0+h*.73,name,14 if mobile else 12.5,'semibold')
  for action,yy in zip(['A>B','hold','B>A'],[.51,.31,.11]):
   cy=y0+h*yy;rh=h*.19
   if action=='hold':
    table.add_patch(Rectangle((.015,cy-rh/2),.97,rh,facecolor=fs.PALETTE['light'],edgecolor=fs.PALETTE['teal'],linewidth=1.6,zorder=1))
   tx(.14,cy,'Hold' if action=='hold' else action,14 if mobile else 13,'semibold' if action=='hold' else 'normal')
   for target,xx in [('composite',.51),('criterion',.83)]:
    r=Rectangle((xx-.145,cy-rh/2),.29,rh,facecolor='none',edgecolor=fs.PALETTE['line'],linewidth=.8,zorder=2)
    table.add_patch(r);label=lookup[(loss,target,action)];t=tx(xx,cy,label,15 if mobile else 14,'semibold' if action=='hold' else 'normal')
    cells.append((loss,target,action,label,r,t))
    contain.append((loss+'-'+target+'-'+action,r,t))
 fig.text(.04,.125 if mobile else .18,'a = w = (1/2, 1/2); M = 1; 0 < τ ≤ 1/2.',ha='left',va='center',fontsize=14 if mobile else 12.5)
 fig.text(.04,.085 if mobile else .12,
          'Hold row: weak τ versus τ; neutral 0 versus τ.',ha='left',va='center',fontsize=14 if mobile else 12.5,fontweight='semibold')
 fig.text(.04,.025 if mobile else .035,
          'Zero neutral cost does not establish\nstrict superiority or a preferred target.' if mobile else
          'Zero neutral composite cost does not establish strict superiority or a substantively preferred target.',
          ha='left',va='bottom',fontsize=14 if mobile else 11.5,color=fs.PALETTE['muted'],linespacing=1.25)
 if mobile:
  # Explicit wrapping preserves type size in the narrower content column.
  fig.texts[-2].set_text('Hold row: weak τ versus τ;\nneutral 0 versus τ.')
 fig.canvas.draw();ren=fig.canvas.get_renderer();checks=[]
 for name,r,t in contain:
  rb=r.get_window_extent(ren);bb=t.get_window_extent(ren)
  checks.append({'cell':name,'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)})
 if not all(c['inside'] for c in checks):raise RuntimeError('Cost-cell clipping: '+str(checks))
 alltext=list(plane.texts)+[plane.xaxis.label,plane.yaxis.label,plane.title]+list(plane.get_xticklabels())+list(plane.get_yticklabels())+list(table.texts)+list(fig.texts)
 for i,t in enumerate(alltext):
  bb=t.get_window_extent(ren)
  if not (bb.x0>=1 and bb.x1<=fig.bbox.width-1 and bb.y0>=1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
  for t2 in alltext[i+1:]:
   if bb.overlaps(t2.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+t2.get_text())
 assert plane.get_aspect()==1.0
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,13.2] if mobile else [10.4,7.8],
       'cost_cell_containment':checks,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,
       'equal_coordinate_scale':True,'points':d['theta_AB'],'cost_cells':[{'loss':a,'target':b,'action':c,'label':l} for a,b,c,l,_,_ in cells],
       'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}


def generate(overwrite=False):
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite is for an authorized observed repair.')
 old=json.loads(DEST.read_text()) if DEST.exists() else None
 d,lookup,checks=coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat();hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/F12a/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_exports':0}
 history=(old or {}).get('execution_history',[])+[attempt]
 record={'id':'F12a','step':'4.14','created_at_utc':now,'author':'JoonHo Lee (jlee296@ua.edu)','status':'rendering','execution_history':history,
         'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashfile(p)} for p in [DATA,BASE/'figstyle.py',HERE]],'exact_cost_checks':checks,
         'scope':'Known point mass;12 affine cost cells derived from weak/strict error and weighted distinctness. No numerical uncertainty or target preference.',
         'actual_image_views':(old or {}).get('actual_image_views',[]),'scientific_boundaries':['Same three reports,weights and M=1 across all four target/loss evaluations.','Composite equality and report withholding are different events.','Zero neutral cost does not establish strict superiority or select a normative target.'],
         'limits':['Only public coordinate/style/source inputs are read at runtime.'],'publication_and_licenses':'Deferred','required_repairs_remaining':[]}
 if old:record['previous_output_history']=old.get('previous_output_history',[])+[{'outputs':old.get('outputs',[])}]
 DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
 try:
  outputs=[];geometry=[]
  for mobile in [False,True]:
   files,g=draw(d,lookup,mobile);outputs.extend(files);geometry.append(g);attempt['layout_exports']+=1;attempt['asset_exports']+=3
  assert [x['path'] for x in outputs]==[str(p.relative_to(ROOT)) for p in targets]
  record['outputs']=outputs;record['geometry_checks']=geometry;record['status']='rendered';attempt['status']='succeeded'
 except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
 finally:
  attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
  record['execution']={'python':platform.python_version(),'renderer_invocations_total':len(history),'last_command_invocations':1,'layout_exports_total':sum(x['layout_exports'] for x in history),'asset_writes_total':sum(x['asset_exports'] for x in history),'model_runs':0,'optimizer_runs':0,'simulation_runs':0,'canonical_edits':0,'register_edits':0}
  DEST.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'id':'F12a','outputs':outputs,'geometry':'PASS','renderer_commands_total':len(history)},indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
