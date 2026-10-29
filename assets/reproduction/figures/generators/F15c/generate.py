#!/usr/bin/env python3
"""Equality-neutral risk-error envelope and separate common-family regret proof.
Stipulated public algebraic bounds, not attained reports or confidence bands.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,csv,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
ROOT=fs.ROOT;HERE=Path(__file__).resolve();DATA=BASE/'data/markov-bound-coordinates.csv';META=BASE/'data/markov-bound-metadata.json'
DEST=ROOT/'evidence/figures/builds/F15c.json';STEM='f15c-two-coefficient-uncertainties-contribute-to-risk'


def coordinates():
 meta=json.loads(META.read_text());assert hashlib.sha256(DATA.read_bytes()).hexdigest()==meta['coordinate_sha256']
 rows=[r for r in csv.DictReader(DATA.open()) if r['series']=='neutral_coefficient_envelope'];assert len(rows)==11
 assert [F(r['disclosure_fraction']) for r in rows]==[F(i,10) for i in range(11)]
 checks=[]
 for r in rows:
  rho,tau,db,dd,eta=map(F,[r[k] for k in ['disclosure_fraction','tau','delta_b','delta_d','optimization_gap_eta']])
  assert (tau,db,dd,eta)==(F(1,4),F(1,10),F(1,5),0)
  strict=rho*db;held=(1-rho)*tau*dd;total=strict+held;zeta=max(db,tau*dd)
  assert strict==F(r['strict_disclosed_component']) and held==F(r['distinct_withheld_component'])
  assert total==F(r['risk_error_envelope'])==F(1,20)+rho/F(20)
  assert total<=zeta==F(r['uniform_radius_zeta'])==F(1,10)
  assert 2*zeta+eta==F(r['uniform_regret_ceiling'])==F(1,5)
  checks.append({'rho':str(rho),'disclosed_component':str(strict),'withheld_component':str(held),'sum':str(total),'zeta':str(zeta),'regret_ceiling':str(2*zeta+eta),'status':'PASS'})
 p=meta['series']['neutral_coefficient_envelope']['parameters'];assert {k:F(v) for k,v in p.items()}=={'tau':F(1,4),'Delta_b':F(1,10),'Delta_d':F(1,5),'eta':0,'zeta':F(1,10),'uniform_regret_ceiling':F(1,5)}
 return rows,checks


def envelope(ax,rows,mobile):
 x=[float(F(r['disclosure_fraction'])) for r in rows];a=[float(F(r['strict_disclosed_component'])) for r in rows];b=[float(F(r['risk_error_envelope'])) for r in rows]
 ax.fill_between(x,0,a,facecolor=fs.PALETTE['teal'],alpha=.20,edgecolor=fs.PALETTE['teal'],lw=.7,zorder=1)
 ax.fill_between(x,a,b,facecolor=fs.PALETTE['ochre'],alpha=.18,hatch='///',edgecolor=fs.PALETTE['ochre'],lw=.7,zorder=1)
 ax.plot(x,b,color=fs.PALETTE['ink'],lw=1.8,zorder=3)
 ax.axhline(.1,color=fs.PALETTE['muted'],ls=(0,(5,3)),lw=1.4,zorder=2)
 size=14 if mobile else 12.5
 ax.text(.025,.107,'Uniform ζ = 0.10',ha='left',va='bottom',fontsize=size,color=fs.PALETTE['muted'])
 ax.text(.06,.043,'Withheld',ha='left',va='center',fontsize=size,color=fs.PALETTE['ink'],bbox={'facecolor':'white','edgecolor':'none','pad':.5})
 ax.text(.60,.024,'Disclosed',ha='left',va='center',fontsize=size,color=fs.PALETTE['ink'])
 ax.set(xlim=(0,1),ylim=(0,.125));ax.set_xticks([0,.5,1],['0','1/2','1']);ax.set_yticks([0,.05,.1],['0','0.05','0.10'])
 ax.tick_params(labelsize=14 if mobile else 11.5)
 ax.set_xlabel('Algebraic disclosure fraction\nρ = N/M',fontsize=size,labelpad=8)
 ax.set_ylabel('Fixed-action absolute\nrisk-error bound',fontsize=size,labelpad=9)
 ax.set_title('A. Fixed-action envelope',fontsize=15 if mobile else 14.5,loc='left',pad=12)
 fs.clean(ax)


def bridge(ax,mobile):
 size=14 if mobile else 12.5
 ax.text(.015,.96,'B. A separate regret argument',ha='left',va='top',fontsize=15 if mobile else 14.5,fontweight='semibold')
 ax.text(.015,.84,'Same nonempty finite family F.\ng*: exact minimizer.\nĝ: estimated optimizer (η = 0).' if mobile else
         'Same nonempty finite family F under exact and estimated objectives.\ng*: exact minimizer; ĝ: estimated optimizer (η = 0).',ha='left',va='center',fontsize=size,linespacing=1.25)
 titles=['Exact → estimated at ĝ','Estimated optimization','Estimated → exact at g*']
 formulas=[r'$R(\widehat g)-\widehat R(\widehat g)\leq\zeta=0.10$',r'$\widehat R(\widehat g)-\widehat R(g^*)\leq\eta=0$',r'$\widehat R(g^*)-R(g^*)\leq\zeta=0.10$']
 rectangles=[(.015,y,.97,.165) for y in [.58,.365,.15]] if mobile else [(x,.34,.30,.32) for x in [.015,.35,.685]]
 objects=[]
 for i,(rect,title,formula) in enumerate(zip(rectangles,titles,formulas)):
  x,y,w,h=rect;patch=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.003,rounding_size=0.008',facecolor='white',edgecolor=fs.PALETTE['line'],linewidth=1.1,zorder=1);ax.add_patch(patch)
  t1=ax.text(x+w/2,y+h*.72,title,ha='center',va='center',fontsize=size,fontweight='semibold',zorder=3)
  t2=ax.text(x+w/2,y+h*.30,formula,ha='center',va='center',fontsize=14 if mobile else 12.2,zorder=3)
  objects.append((i,patch,[t1,t2]))
 for x,y in [(.5,.555),(.5,.34)] if mobile else [(.3325,.50),(.6675,.50)]:ax.text(x,y,'+',ha='center',va='center',fontsize=16,color=fs.PALETTE['muted'])
 ax.text(.5,.045 if mobile else .16,r'Exact-risk regret $\leq\zeta+\eta+\zeta=0.20$',ha='center',va='center',fontsize=14 if mobile else 14,fontweight='semibold')
 return objects


def draw(rows,mobile):
 fig=fs.canvas(4.8 if mobile else 10.8,18.6 if mobile else 10.8,mobile)
 fig.text(.04,.985,'Two coefficient uncertainties\ncontribute to risk' if mobile else 'Two coefficient uncertainties contribute to risk',ha='left',va='top',fontsize=16,fontweight='semibold',linespacing=1.2)
 fig.text(.04,.925 if mobile else .92,'τ = 0.25; Δb = 0.10; Δd = 0.20.\nIllustrative simultaneous radii.' if mobile else
          'Illustrative simultaneous radii: τ = 0.25; Δb = 0.10; Δd = 0.20; η = 0.',ha='left',va='top',fontsize=14 if mobile else 12.5,linespacing=1.25)
 p=fig.add_axes([.26,.67,.66,.18] if mobile else [.10,.60,.52,.27]);envelope(p,rows,mobile)
 if mobile:
  fig.text(.04,.61,r'Disclosed: $\rho\Delta_b$'+'\n'+r'Withheld: $(1-\rho)\tau\Delta_d$'+'\n'+r'Total $B(\rho)=0.05+0.05\rho$',ha='left',va='top',fontsize=14,linespacing=1.3)
  fig.text(.04,.555,'B(0) = 0.05: withheld distinctness.\nB(1) = 0.10: disclosed direction.',ha='left',va='top',fontsize=14,linespacing=1.25)
 else:
  note=fs.diagram_axis(fig,[.68,.60,.285,.27])
  lines=[('Component upper bounds',.94,13.5,'semibold'),(r'Disclosed: $\rho\Delta_b$',.75,12.5,'normal'),(r'Withheld: $(1-\rho)\tau\Delta_d$',.60,12.5,'normal'),(r'Total: $0.05+0.05\rho$',.45,12.5,'semibold'),('B(0) = 0.05\nWithheld distinctness',.26,12.5,'normal'),('B(1) = 0.10\nDisclosed direction',.06,12.5,'normal')]
  for text,y,size,weight in lines:note.text(.02,y,text,ha='left',va='center',fontsize=size,fontweight=weight,linespacing=1.2)
 b=fs.diagram_axis(fig,[.04,.14,.92,.36] if mobile else [.04,.13,.92,.35]);objects=bridge(b,mobile)
 fig.text(.04,.025,'Algebraic bound; no attained action path.\nFeasible ρ depends on n and the family.\nRisk and regret use the same M and loss.' if mobile else
          'Algebraic envelope; no attained report path. Feasible N/M depends on n and the family.\nBoth stages use normalized risk units; regret requires the same targets, law, weights and nonempty finite family.\nThese are conditional bounds, not observed error or sampling confidence.',
          ha='left',va='bottom',fontsize=14 if mobile else 11.5,color=fs.PALETTE['muted'],linespacing=1.25)
 fig.canvas.draw();ren=fig.canvas.get_renderer();contain=[]
 for i,patch,txt in objects:
  rb=patch.get_window_extent(ren)
  for t in txt:
   bb=t.get_window_extent(ren);contain.append({'term':i,'text':t.get_text(),'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)})
 if not all(c['inside'] for c in contain):raise RuntimeError('Proof-card clipping: '+str([c for c in contain if not c['inside']]))
 alltext=list(p.texts)+[p.xaxis.label,p.yaxis.label,p.title]+list(p.get_xticklabels())+list(p.get_yticklabels())+list(b.texts)+list(fig.texts)
 if not mobile:alltext+=list(note.texts)
 for i,t in enumerate(alltext):
  bb=t.get_window_extent(ren)
  if not(bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
  for u in alltext[i+1:]:
   if bb.overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,18.6] if mobile else [10.8,10.8],
         'proof_card_containment':contain,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,
         'plot_axes_limits':{'algebraic_rho':[0,1],'absolute_risk_error_bound':[0,.125]},
         'proof_terms':['R(ghat)-Rhat(ghat)<=zeta','Rhat(ghat)-Rhat(gstar)<=eta','Rhat(gstar)-R(gstar)<=zeta'],
         'proof_has_no_shared_vertical_axis':True,'optional_endpoint_law_inset':False,
         'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}


def generate(overwrite=False):
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite is for an authorized observed repair.')
 old=json.loads(DEST.read_text()) if DEST.exists() else None;rows,checks=coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/F15c/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_exports':0}
 history=(old or {}).get('execution_history',[])+[attempt]
 record={'id':'F15c','step':'5.10','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':history,
         'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in [DATA,META,BASE/'figstyle.py',HERE]],'coordinate_selector':'Exactly11rows with series=neutral_coefficient_envelope; other-series blanks are not zeros.','exact_checks':checks,'actual_image_views':(old or {}).get('actual_image_views',[]),
         'scope':'Stipulated algebraic coefficient-error envelope and separate common-family optimization inequality; no simulation,model,optimization or original example execution.',
         
         'scientific_boundaries':['Filled areas are stacked component upper bounds,not probabilities or attained errors.','Algebraic rho grid does not assert feasibility of every intermediate N/M.','Same targets,law,weights,normalization and common nonempty finite family underlie the regret bound.','Regret0.20 is a conditional upper bound,not an attained value or confidence level.','No endpoint-law inset or package guarantee is shown.'],
         'limits':['Independent meaning/color/PDF/final chapter-context checks remain separate.','Only public coordinates,metadata,style and ownsource supply scientific plotted inputs.'],'publication_and_licenses':'Deferred','required_repairs_remaining':[]}
 if old:record['previous_output_history']=old.get('previous_output_history',[])+[{'outputs':old.get('outputs',[])}]
 DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
 try:
  outputs=[];geometry=[]
  for mobile in [False,True]:
   files,g=draw(rows,mobile);outputs.extend(files);geometry.append(g);attempt['layout_exports']+=1;attempt['asset_exports']+=3
  assert [o['path'] for o in outputs]==[str(p.relative_to(ROOT)) for p in targets]
  record['outputs']=outputs;record['geometry_checks']=geometry;record['status']='rendered';attempt['status']='succeeded'
 except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
 finally:
  attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record['execution']={'python':platform.python_version(),'renderer_invocations_total':len(history),'last_command_invocations':1,'layout_exports_total':sum(x['layout_exports'] for x in history),'asset_writes_total':sum(x['asset_exports'] for x in history),'model_runs':0,'simulation_runs':0,'optimizer_runs':0,'canonical_edits':0,'register_edits':0};DEST.write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'id':'F15c','outputs':outputs,'geometry':'PASS','render_commands_total':len(history)},indent=2))


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
