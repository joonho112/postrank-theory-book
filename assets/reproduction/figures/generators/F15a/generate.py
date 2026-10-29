#!/usr/bin/env python3
"""Two exact coefficient/protection cases, shown as membership matrices.

No area encodes a set size or probability. All scientific coordinates come
from the public coefficient_protection subobject; no simulation is run.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle,FancyBboxPatch
ROOT=fs.ROOT;HERE=Path(__file__).resolve();DATA=BASE/'data/transformations-protections.json'
DEST=ROOT/'evidence/figures/builds/F15a.json';STEM='f15a-approximate-and-intended-protection-feasibility'


def coordinates():
 cases=json.loads(DATA.read_text())['coefficient_protection'];checks=[]
 assert [F(c['t']) for c in cases]==[0,F(1,5)]
 for c in cases:
  t,q,eps=map(F,[c['t'],c['q'],c['epsilon']]);assert q==t+F(1,20) and eps==F(1,10)
  assert F(c['inner_threshold'])==q-eps and F(c['outer_threshold'])==q+eps
  sets={k:[] for k in ['inner','exact','nominal','outer']}
  for row in c['actions']:
   n=row['N'];e,eh=map(F,[row['exact_error'],row['estimated_error']])
   if row['action']=='withhold':assert n==0 and e==eh==0 and row['rate'] is None
   else:
    assert n==1 and (e,eh)==((t+eps,t) if row['action']=='A>B' else (1-t-eps,1-t))
    assert F(row['rate'])==e/n
   tests={'inner':eh<=(q-eps)*n,'exact':e<=q*n,'nominal':eh<=q*n,'outer':eh<=(q+eps)*n}
   assert all(row[k]==v for k,v in tests.items()) and abs(e-eh)<=eps*n
   for k,v in tests.items():
    if v:sets[k].append(row['action'])
   checks.append({'t':str(t),'action':row['action'],'N':n,'exact_count':str(e),'estimated_count':str(eh),'membership':tests,'rate':row['rate'],'status':'PASS'})
  assert sets=={'inner':['withhold'],'exact':['withhold'],'nominal':['withhold','A>B'],'outer':['withhold','A>B']}
 assert F(cases[0]['inner_threshold'])==F(-1,20)
 forward=cases[0]['actions'][1]
 assert forward['action']=='A>B' and F(forward['estimated_error'])==0
 assert F(forward['estimated_error'])<=0 and F(forward['exact_error'])>F(cases[0]['q'])
 return cases,checks


def draw(cases,mobile):
 fig=fs.canvas(4.8 if mobile else 10.8,19 if mobile else 11.2,mobile)
 fig.text(.04,.982,'Approximate feasibility can miss\nthe intended constraint' if mobile else
          'Approximate feasibility can miss the intended constraint',ha='left',va='top',fontsize=16,fontweight='semibold',linespacing=1.2)
 fig.text(.04,.925,
          'One pair, one criterion; M = 1.\nExact forward error = t + 1/10;\napproximate forward error = t.' if mobile else
          'One pair, one criterion; M = 1. Exact forward error = t + 1/10; approximate forward error = t.',
          ha='left',va='top',fontsize=14 if mobile else 12.5,linespacing=1.25)
 ax=fs.diagram_axis(fig,[.025,.285,.95,.55] if mobile else [.025,.33,.95,.54])
 containers={};texts=[];matrixcells=[];membershipheaders=[];size=14 if mobile else 12.5
 def panel(key,rect):
  patch=FancyBboxPatch(rect[:2],rect[2],rect[3],boxstyle='round,pad=0.003,rounding_size=0.008',facecolor='white',edgecolor=fs.PALETTE['line'],linewidth=1,zorder=1)
  ax.add_patch(patch);containers[key]=patch;return rect
 def tx(owner,role,x,y,label,font=None,weight='normal',color=None):
  t=ax.text(x,y,label,ha='center',va='center',fontsize=font or size,fontweight=weight,color=color or fs.PALETTE['ink'],zorder=4,linespacing=1.2);texts.append((owner,role,t));return t
 def cell(owner,role,x,y,w,h,label,passed):
  patch=Rectangle((x-w/2,y-h/2),w,h,facecolor=fs.PALETTE['light'] if passed else 'white',edgecolor=fs.PALETTE['teal'] if passed else fs.PALETTE['line'],linewidth=1.25 if passed else .8,zorder=2)
  ax.add_patch(patch);cid=owner+'-'+role;containers[cid]=patch
  tx(cid,role,x,y,label,weight='semibold' if passed else 'normal',color=fs.PALETTE['teal'] if passed else fs.PALETTE['muted'])
 for ci,(case,bottom) in enumerate(zip(cases,[.515,.015])):
  key='case'+str(ci);x,y,w,h=panel(key,(.005,bottom,.99,.47))
  tx(key,'parameter setting',.5,y+h*(.94 if mobile else .91),
     't = '+case['t']+';  q = '+case['q']+';  ε = '+case['epsilon'],15 if mobile else 14,'semibold')
  tx(key,'signed cutoffs',.5,y+h*(.84 if mobile else .75),
     'q − ε = '+case['inner_threshold']+';  q + ε = '+case['outer_threshold'],14 if mobile else 12.5,
     color=fs.PALETTE['rust'] if ci==0 else None)
  if mobile:
   countxs=[.17,.40,.61,.82];header_y=.72;countys=[.63,.54,.45]
   for xx,label in zip(countxs,['Report','N',r'$\widehat E$',r'$E$']):tx(key,'count header '+label,xx,y+h*header_y,label,weight='semibold')
   for row,yy in zip(case['actions'],countys):
    values=['Hold' if row['action']=='withhold' else row['action'],str(row['N']),row['estimated_error'],row['exact_error']]
    for xx,label in zip(countxs,values):tx(key,'count '+row['action'],xx,y+h*yy,label)
   setxs=[.09,.32,.51,.71,.91];group=[]
   for xx,label in zip(setxs,['Report','Inner','Exact','Nominal','Outer']):group.append(tx(key,'membership header '+label,xx,y+h*.33,label,weight='semibold'))
   membershipheaders.append(group)
   for row,yy in zip(case['actions'],[.24,.15,.06]):
    tx(key,'report '+row['action'],setxs[0],y+h*yy,'Hold' if row['action']=='withhold' else row['action'])
    for xx,kind in zip(setxs[1:],['inner','exact','nominal','outer']):
     cell(key,row['action']+'-'+kind,xx,y+h*yy,.145,h*.075,'Yes' if row[kind] else 'No',row[kind]);matrixcells.append({'t':case['t'],'action':row['action'],'set':kind,'member':row[kind]})
  else:
   xs=[.09,.23,.35,.46,.59,.71,.83,.95]
   for xx,label in zip(xs,['Report','N',r'$\widehat E$',r'$E$','Inner','Exact','Nominal','Outer']):tx(key,'header '+label,xx,y+h*.57,label,weight='semibold')
   for row,yy in zip(case['actions'],[.40,.24,.08]):
    for xx,label in zip(xs[:4],['Hold' if row['action']=='withhold' else row['action'],str(row['N']),row['estimated_error'],row['exact_error']]):tx(key,'count '+row['action'],xx,y+h*yy,label)
    for xx,kind in zip(xs[4:],['inner','exact','nominal','outer']):
     cell(key,row['action']+'-'+kind,xx,y+h*yy,.09,h*.13,'Yes' if row[kind] else 'No',row[kind]);matrixcells.append({'t':case['t'],'action':row['action'],'set':kind,'member':row[kind]})
 definitions=(r'Inner: $\widehat E\leq(q-\varepsilon)N$'+'\n'+r'Exact: $E\leq qN$'+'\n'+r'Nominal: $\widehat E\leq qN$'+'\n'+r'Outer: $\widehat E\leq(q+\varepsilon)N$') if mobile else (
              r'Inner: $\widehat E\leq(q-\varepsilon)N$'+r'     Exact: $E\leq qN$'+'\n'+r'Nominal: $\widehat E\leq qN$'+r'     Outer: $\widehat E\leq(q+\varepsilon)N$')
 fig.text(.04,.26 if mobile else .29,definitions,ha='left',va='top',fontsize=size,linespacing=1.3)
 call=fs.diagram_axis(fig,[.04,.105,.92,.10] if mobile else [.04,.10,.92,.145])
 note=('At t = 0, A>B has N = 1.\nInner 0 ≤ −1/20 fails.\nClipping to 0 wrongly passes;\nexact 1/10 > q = 1/20 still fails.') if mobile else (
       'At t = 0, A>B fails the inner test 0 ≤ −1/20. Clipping the threshold to 0 wrongly admits it.\n'
       'Its exact error 1/10 > q = 1/20 still violates the intended protection.')
 callpatch=fs.box(call,.015,.035,.97,.93,note,size=size,ec=fs.PALETTE['rust'],fc='white');calltext=call.texts[-1]
 fig.text(.04,.025,
          'Hold: N = 0; all count rows read 0 ≤ 0.\nIts error fraction is undefined.\nExact refers to the intended supplied law.' if mobile else
          'Hold (N = 0): all count rows read 0 ≤ 0; the displayed error fraction is undefined.\nExact refers to the intended supplied law; membership columns are separate tests.',
          ha='left',va='bottom',fontsize=14 if mobile else 11.5,color=fs.PALETTE['muted'],linespacing=1.25)
 fig.canvas.draw();ren=fig.canvas.get_renderer();geometry=[]
 headergaps=[]
 for group in membershipheaders:
  for left,right in zip(group,group[1:]):
   gap=right.get_window_extent(ren).x0-left.get_window_extent(ren).x1
   headergaps.append({'left':left.get_text(),'right':right.get_text(),'gap_pixels_at_renderer_dpi':float(gap),'minimum8pixels':bool(gap>=8)})
 if not all(x['minimum8pixels'] for x in headergaps):raise RuntimeError('Mobile header crowding: '+str(headergaps))
 for owner,role,t in texts:
  bb=t.get_window_extent(ren);rb=containers[owner].get_window_extent(ren);geometry.append({'owner':owner,'role':role,'font_pt':t.get_fontsize(),'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)})
 rb=callpatch.get_window_extent(ren);bb=calltext.get_window_extent(ren);geometry.append({'owner':'clipping callout','role':'signed threshold','font_pt':size,'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)})
 if not all(g['inside'] for g in geometry):raise RuntimeError('Container clipping: '+str([g for g in geometry if not g['inside']]))
 alltext=list(ax.texts)+list(call.texts)+list(fig.texts)
 for i,t in enumerate(alltext):
  bb=t.get_window_extent(ren)
  if not(bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
  for u in alltext[i+1:]:
   if bb.overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
 assert len(matrixcells)==24
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,19] if mobile else [10.8,11.2],
          'text_containment':geometry,'membership_header_gaps':headergaps,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,
          'membership_cells':matrixcells,'no_area_or_probability_geometry':True,
          'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}


def generate(overwrite=False):
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite is for an authorized observed repair.')
 old=json.loads(DEST.read_text()) if DEST.exists() else None;cases,checks=coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/F15a/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_exports':0}
 history=(old or {}).get('execution_history',[])+[attempt]
 record={'id':'F15a','step':'5.8','created_at_utc':now,'author':'JoonHo Lee (jlee296@ua.edu)','status':'rendering','execution_history':history,
         'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in [DATA,BASE/'figstyle.py',HERE]],'coordinate_selector':'coefficient_protection only','exact_count_and_membership_checks':checks,
         'scope':'Exact two-case membership readback and rendering; no Monte Carlo,model,optimizer or original example program execution.','actual_image_views':(old or {}).get('actual_image_views',[]),
         'scientific_boundaries':['Signed inner thresholds are not clipped.','The four columns are separate count tests; no general exact/nominal nesting is implied.','N0 gives0<=0 without defining an error fraction,provided withholding belongs to the base family.','Exact denotes the intended supplied law,not a verified data-generating posterior.','No area,set size or numerical confidence is encoded.'],
         'limits':['Only public coordinate/style/source inputs are scientific runtime dependencies.'],'publication_and_licenses':'Deferred','required_repairs_remaining':[]}
 if old:record['previous_output_history']=old.get('previous_output_history',[])+[{'outputs':old.get('outputs',[])}]
 DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
 try:
  outputs=[];geometry=[]
  for mobile in [False,True]:
   files,g=draw(cases,mobile);outputs.extend(files);geometry.append(g);attempt['layout_exports']+=1;attempt['asset_exports']+=3
  assert [o['path'] for o in outputs]==[str(p.relative_to(ROOT)) for p in targets]
  assert geometry[0]['membership_cells']==geometry[1]['membership_cells']
  record['outputs']=outputs;record['geometry_checks']=geometry;record['status']='rendered';attempt['status']='succeeded'
 except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
 finally:
  attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record['execution']={'python':platform.python_version(),'renderer_invocations_total':len(history),'last_command_invocations':1,'layout_exports_total':sum(x['layout_exports'] for x in history),'asset_writes_total':sum(x['asset_exports'] for x in history),'model_runs':0,'optimizer_runs':0,'simulation_runs':0,'canonical_edits':0,'register_edits':0};DEST.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'id':'F15a','outputs':outputs,'geometry':'PASS','render_commands_total':len(history)},indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
