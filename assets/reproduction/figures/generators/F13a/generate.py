#!/usr/bin/env python3
"""Exact count-form protection example; zero weight does not remove a guard."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
ROOT=fs.ROOT;HERE=Path(__file__).resolve()
DATA=BASE/'data/transformations-protections.json';DEST=ROOT/'evidence/figures/builds/F13a.json'
STEM='f13a-protection-can-leave-withholding-or-an-empty-family'


def coordinates():
 d=json.loads(DATA.read_text())['pointmass_protection'];theta=d['targets'];w=list(map(F,d['weights']));q=list(map(F,d['q']))
 assert theta=={'A':[1,0],'B':[0,1]} and w==[1,0] and q==[F(1,2),F(1,2)]
 checks=[]
 for r in d['rows']:
  n=0 if r['action']=='withhold' else 1
  if n:
   a,b=r['action'].split('>');e=[F(theta[a][k]<=theta[b][k]) for k in range(2)]
  else:e=[F(0),F(0)]
  assert n==r['N'] and e==list(map(F,r['criterion_errors']))
  intercept=sum(x*y for x,y in zip(w,e));coefficient=F(1-n)
  assert ('tau' if coefficient else str(intercept))==r['weighted_risk']
  passed=[e[k]<=q[k]*n for k in range(2)]
  assert all(passed)==r['feasible_at_most2']
  assert (all(passed) and n==1)==r['feasible_exact2']
  checks.append({'action':r['action'],'N':n,'errors':list(map(str,e)),
                 'budget_rhs':[str(x*n) for x in q],'protection_pass':passed,
                 'risk_intercept':str(intercept),'risk_tau_coefficient':str(coefficient),
                 'displayed_error_fractions':[str(x/n) for x in e] if n else None,
                 'feasible_at_most2':all(passed),'feasible_exact2':all(passed) and n==1,'status':'PASS'})
 assert [c['action'] for c in checks if c['feasible_at_most2']]==['withhold']
 assert not any(c['feasible_exact2'] for c in checks)
 assert checks[0]['risk_intercept']=='0' and checks[0]['protection_pass']==[True,False]
 return d,checks


def draw(d,checks,mobile):
 fig=fs.canvas(4.8 if mobile else 10.4,19.2 if mobile else 8.5,mobile)
 fig.text(.04,.985,'Protection can leave only silence\nor no admissible report' if mobile else
          'Protection can leave withholding or an empty family',ha='left',va='top',fontsize=16,fontweight='semibold',linespacing=1.2)
 ax=fs.diagram_axis(fig,(.025,.13,.95,.80) if mobile else (.025,.10,.95,.80))
 rectangles={};text=[];rects={}
 def panel(key,rect,color=None):
  rects[key]=rect;p=FancyBboxPatch(rect[:2],rect[2],rect[3],boxstyle='round,pad=0.003,rounding_size=0.008',
     facecolor='white',edgecolor=color or fs.PALETTE['line'],linewidth=1.2,zorder=1);ax.add_patch(p);rectangles[key]=p
 def tx(key,role,yy,label,size=None,weight='normal',color=None):
  x,y,w,h=rects[key];t=ax.text(x+w*.5,y+h*yy,label,ha='center',va='center',fontsize=size or (14 if mobile else 12.5),
     fontweight=weight,color=color or fs.PALETTE['ink'],linespacing=1.22,zorder=3);text.append((key,role,t));return t
 panel('source',(.015,.84,.97,.125))
 if mobile:
  tx('source','state',.84,'Known A = (1, 0), B = (0, 1)',weight='semibold')
  tx('source','orientation',.66,'Larger is higher on both criteria.')
  tx('source','weights and budgets',.40,'Objective w = (1, 0)\nBudgets q₁ = q₂ = 1/2')
  tx('source','zero weight boundary',.12,'Criterion 2 remains protected.',weight='semibold')
 else:
  tx('source','state and orientation',.84,'Known A = (1, 0), B = (0, 1); larger is higher on both criteria.',weight='semibold')
  tx('source','weights and budgets',.50,'Objective weights w = (1, 0); both protection budgets q₁ = q₂ = 1/2.')
  tx('source','zero weight boundary',.16,'Criterion 2 remains protected although its objective weight is zero.',weight='semibold')
 for i,c in enumerate(checks):
  key='action'+str(i);r=(.015,[.62,.405,.19][i],.97,.195) if mobile else (.015+i*.33,.28,.31,.50)
  panel(key,r,fs.PALETTE['teal'] if c['feasible_at_most2'] else fs.PALETTE['line'])
  tx(key,'action',.91,'Hold the pair' if c['action']=='withhold' else 'Report '+c['action'],15 if mobile else 14,'semibold')
  tx(key,'counts',.75,'N = '+str(c['N'])+';  (E₁, E₂) = ('+', '.join(c['errors'])+')')
  for k,yy in [(0,.59),(1,.43)]:
   passed=c['protection_pass'][k];symbol='≤' if passed else '>'
   label='Criterion '+str(k+1)+': '+c['errors'][k]+' '+symbol+' '+c['budget_rhs'][k]+'  '+('PASS' if passed else 'FAIL')
   tx(key,'protection '+str(k+1),yy,label,weight='semibold',color=fs.PALETTE['teal'] if passed else fs.PALETTE['rust'])
  tx(key,'weighted risk',.27,'Weighted risk = '+('τ' if c['risk_tau_coefficient']=='1' else c['risk_intercept']),weight='semibold')
  tx(key,'displayed fractions',.11,'Error fractions: undefined\nbecause N = 0' if c['displayed_error_fractions'] is None else
     'Error fractions: ('+', '.join(c['displayed_error_fractions'])+')')
 if mobile:
  panel('atmost',(.015,.095,.97,.075),fs.PALETTE['teal']);panel('exact',(.015,.008,.97,.075),fs.PALETTE['rust'])
 else:
  panel('atmost',(.015,.05,.465,.17),fs.PALETTE['teal']);panel('exact',(.52,.05,.465,.17),fs.PALETTE['rust'])
 tx('atmost','family',.72,'At most 2 grades',15 if mobile else 14,'semibold')
 tx('atmost','protected result',.30,'Protected family: {hold}',weight='semibold',color=fs.PALETTE['teal'])
 tx('exact','family',.72,'Exactly 2 grades',15 if mobile else 14,'semibold')
 tx('exact','protected result',.30,'Empty: no admissible report',weight='semibold',color=fs.PALETTE['rust'])
 fig.text(.04,.025,
          ('Count rows are Eₖ ≤ qₖN, with M = 1.\nAt N = 0, the error fractions are undefined.\nFeasibility does not establish fairness\nor repeated-sampling error control.') if mobile else
          ('Count rows are Eₖ ≤ qₖN, with M = 1. At N = 0, error fractions are undefined.\n'
           'Feasibility under the supplied point mass does not establish fairness or repeated-sampling error control.'),
          ha='left',va='bottom',fontsize=14 if mobile else 11.5,color=fs.PALETTE['muted'],linespacing=1.25)
 fig.canvas.draw();ren=fig.canvas.get_renderer();geometry=[]
 patchchecks=[]
 for key,patch in rectangles.items():
  bb=patch.get_window_extent(ren);rb=ax.get_window_extent(ren)
  inside=bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)
  patchchecks.append({'container':key,'entire_patch_inside_axes':inside})
 if not all(c['entire_patch_inside_axes'] for c in patchchecks):raise RuntimeError('Patch clipping: '+str(patchchecks))
 for key,role,t in text:
  bb=t.get_window_extent(ren);rb=rectangles[key].get_window_extent(ren)
  geometry.append({'container':key,'role':role,'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1),'font_pt':t.get_fontsize()})
 alltext=list(ax.texts)+list(fig.texts)
 for i,t in enumerate(alltext):
  bb=t.get_window_extent(ren)
  if not(bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
  for u in alltext[i+1:]:
   if bb.overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
 if not all(c['inside'] for c in geometry):raise RuntimeError('Container clipping: '+str([c for c in geometry if not c['inside']]))
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,19.2] if mobile else [10.4,8.5],
          'text_containment':geometry,'patch_containment':patchchecks,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,
          'action_order':[c['action'] for c in checks],'family_results':{'at_most2':['withhold'],'exactly2':[]},
          'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}


def generate(overwrite=False):
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite is for an authorized observed repair.')
 old=json.loads(DEST.read_text()) if DEST.exists() else None;d,checks=coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/F13a/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_exports':0}
 history=(old or {}).get('execution_history',[])+[attempt]
 record={'id':'F13a','step':'4.16','created_at_utc':now,'author':'JoonHo Lee (jlee296@ua.edu)','status':'rendering','execution_history':history,
         'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in [DATA,BASE/'figstyle.py',HERE]],'coordinate_selector':'pointmass_protection only','exact_checks':checks,'actual_image_views':(old or {}).get('actual_image_views',[]),
         'scope':'Exact point-mass cost/protection check for the three saved two-unit actions; no simulation,optimizer or model run.',
         'scientific_boundaries':['Zero objective weight does not remove a separately declared protection.','At N=0, homogeneous count rows hold while displayed fractions remain undefined.','The protected exact-two-grade family is empty,not a report with a higher attained risk.','Feasibility is conditional on the supplied law and does not establish fairness or repeated-sampling control.'],
         'limits':['Independent semantic,color/PDF and final chapter context checks remain separate.','Only public coordinate/style/source are scientific runtime inputs.'],'publication_and_licenses':'Deferred','required_repairs_remaining':[]}
 if old:record['previous_output_history']=old.get('previous_output_history',[])+[{'outputs':old.get('outputs',[])}]
 DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
 try:
  outputs=[];geometry=[]
  for mobile in [False,True]:
   files,g=draw(d,checks,mobile);outputs.extend(files);geometry.append(g);attempt['layout_exports']+=1;attempt['asset_exports']+=3
  assert [o['path'] for o in outputs]==[str(p.relative_to(ROOT)) for p in targets]
  record['outputs']=outputs;record['geometry_checks']=geometry;record['status']='rendered';attempt['status']='succeeded'
 except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
 finally:
  attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record['execution']={'python':platform.python_version(),'renderer_invocations_total':len(history),'last_command_invocations':1,'layout_exports_total':sum(a['layout_exports'] for a in history),'asset_writes_total':sum(a['asset_exports'] for a in history),'model_runs':0,'optimizer_runs':0,'simulation_runs':0,'canonical_edits':0,'register_edits':0}
  DEST.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'id':'F13a','outputs':outputs,'geometry':'PASS','renderer_commands_total':len(history)},indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
