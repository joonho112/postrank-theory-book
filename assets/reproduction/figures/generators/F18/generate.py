#!/usr/bin/env python3
"""Original calculation-flow map: two conditional risk laws, one frozen decision.
No empirical estimates, scientific coordinates, simulation or optimization.
"""
from pathlib import Path
import sys,json,hashlib,datetime,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;HERE=Path(__file__).resolve();STEM='f18-select-under-one-law-and-evaluate-under-another';DEST=ROOT/'evidence/figures/builds/F18.json'

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 12,19.8 if mobile else 10.8,mobile)
 ax=fs.diagram_axis(fig,[.035,.02,.93,.93]);ax.set_xlim(-.025,1.025);checks=[];texts=[]
 title='Select under one law;\nevaluate under another' if mobile else 'Select under one law; evaluate under another'
 fig.text(.04,.985,title,va='top',fontsize=16 if mobile else 19,weight='semibold')
 def card(x,y,w,h,heading,body,fc='light',size=None):
  p=fs.box(ax,x,y,w,h,'',fc=fs.PALETTE[fc]);size=size or (14 if mobile else 12.5)
  t=ax.text(x+.025,y+h*.84,heading,va='center',fontsize=14 if mobile else 13.5,weight='semibold',linespacing=1.2)
  b=ax.text(x+.025,y+h*.40,body,va='center',fontsize=size,linespacing=1.25)
  texts.extend([t,b]);checks.extend([(p,t),(p,b)]);return p
 if mobile:
  card(0,.895,1,.063,'Hold the problem fixed','y, targets, loss, preferences;\nM; nonempty finite family F(y).',size=14)
  s=card(0,.742,1,.115,'1. Choose under supplied beliefs',r'$\widehat g\in\mathcal{F}(y)$'+'\n'+r'$R^s(\widehat g)\leq\min_{g\in\mathcal{F}}R^s(g)+\eta$'+'\nActual selection-risk gap η ≥ 0.','light')
  g=card(0,.644,1,.060,'2. Freeze the selected report','Same complete report ĝ in both risks.','white')
  e=card(0,.457,1,.150,'3. Assess the same report twice',r'Supplied law $\Pi_s(\cdot\mid y)$: $R^s(\widehat g)$'+'\n\n'+r'Evaluation law $P(\cdot\mid y)$: $R^P(\widehat g)$'+'\n\nP is a declared evaluation model;\nits correctness is not established here.','white')
  fs.arrow(ax,(.5,.742),(.5,.704),patchA=s,patchB=g);fs.arrow(ax,(.5,.644),(.5,.607),patchA=g,patchB=e)
  card(0,.300,1,.115,'A conditional common-family bound',r'$d=\max_{g\in\mathcal{F}}|R^s(g)-R^P(g)|$'+'\n'+r'$R^P(\widehat g)-\min_{g\in\mathcal{F}}R^P(g)\leq2d+\eta$'+'\nThe diagram supplies no value for d.','light')
  card(0,.162,1,.100,'Numerical approximation','Approximate the same supplied law.\nMore draws can improve integration;\nthey do not establish agreement with P.','white')
  card(0,.025,1,.100,'Discrepancy between laws','Requires evidence about the model.\nDifferent laws can share action risks.\nRisk control does not transfer\ncriterion protections across laws.','white')
  fig.text(.04,.007,'Neutral loss also retains distinctness\nand withholding; guard families must match.',va='bottom',fontsize=14,color=fs.PALETTE['muted'],linespacing=1.2)
 else:
  card(0,.87,1,.095,'Hold the decision problem fixed','Observed y, targets, loss, preferences, M and the same nonempty finite family F(y).',size=12.5)
  s=card(0,.54,.31,.25,'1. Choose under\nsupplied beliefs',r'$\widehat g\in\mathcal{F}(y)$'+'\n'+r'$R^s(\widehat g)\leq\min_{g\in\mathcal{F}}R^s(g)+\eta$'+'\nActual selection-risk gap η ≥ 0.')
  g=card(.37,.59,.23,.15,'2. Freeze the report','Same complete\nreport ĝ.','white')
  e=card(.67,.50,.33,.33,'3. Assess the same report',r'$\Pi_s(\cdot\mid y):\quad R^s(\widehat g)$'+'\n\n'+r'$P(\cdot\mid y):\quad R^P(\widehat g)$'+'\n\nP is a declared evaluation model;\nits correctness needs evidence.','white')
  fs.arrow(ax,(.31,.665),(.37,.665),patchA=s,patchB=g);fs.arrow(ax,(.60,.665),(.67,.665),patchA=g,patchB=e)
  card(0,.335,1,.115,'Conditional comparison on that same family',r'$d=\max_{g\in\mathcal{F}}|R^s(g)-R^P(g)|,\qquad R^P(\widehat g)-\min_{g\in\mathcal{F}}R^P(g)\leq2d+\eta$'+'\nNo value for d is supplied by the diagram; g minimizers stay within F(y).')
  card(0,.095,.47,.175,'Numerical approximation within one law','Approximate the same supplied law.\nMore draws can improve integration; they do not\nestablish agreement with the evaluation law.','white')
  card(.53,.095,.47,.175,'Discrepancy between laws','Requires evidence about the evaluation model.\nDifferent laws can share relevant action risks.\nObjective control does not transfer protection safety.','white')
  fig.text(.04,.025,'Equality-neutral loss also retains distinctness-dependent withholding. Law-specific guards must not silently change the common family.\nArrows depict calculation flow; no empirical calibration, causal effect or universally positive regret is asserted.',va='bottom',fontsize=11.5,color=fs.PALETTE['muted'],linespacing=1.25)
 fig.canvas.draw();ren=fig.canvas.get_renderer()
 for p,t in checks:
  bb=p.get_window_extent(ren);tb=t.get_window_extent(ren)
  assert tb.x0>=bb.x0+1 and tb.x1<=bb.x1-1 and tb.y0>=bb.y0+1 and tb.y1<=bb.y1-1,('card clipping',t.get_text())
 alltexts=texts+list(fig.texts)
 for i,t in enumerate(alltexts):
  bb=t.get_window_extent(ren);assert bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height,('canvas',t.get_text())
  for u in alltexts[i+1:]:assert not bb.overlaps(u.get_window_extent(ren)),('overlap',t.get_text(),u.get_text())
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'card_text_containment':len(checks),'all_canvas_and_text_nonoverlap':True}

def main(overwrite):
 old=json.loads(DEST.read_text()) if DEST.exists() else {};assert overwrite or not old,'Use --overwrite only for recorded repair/reproduction.'
 history=old.get('execution_history',[]);a={'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'python -B assets/reproduction/figures/generators/F18/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_writes':0,'layout_exports':0};history.append(a)
 d={'id':'F18','author':'JoonHo Lee (jlee296@ua.edu)','scope':'Original conceptual source-based diagram; no scientific coordinates or empirical/model/solver runs.','inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,BASE/'figstyle.py']],'execution_history':history,'outputs':[],'geometry_checks':[],'actual_image_views':old.get('actual_image_views',[])}
 DEST.parent.mkdir(parents=True,exist_ok=True)
 try:
  for m in [False,True]:
   out,g=draw(m);d['outputs']+=out;d['geometry_checks'].append(g);a['asset_writes']+=3;a['layout_exports']+=1
  a['status']='succeeded'
 except Exception as ex:a['status']='failed';a['error']=str(ex);raise
 finally:
  a['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['execution']={'producer_commands':len(history),'complete_commands':sum(x['status']=='succeeded' for x in history),'failed_commands':sum(x['status']=='failed' for x in history),'asset_writes':sum(x['asset_writes'] for x in history),'model_simulation_solver_runs':0};DEST.write_text(json.dumps(d,indent=2)+'\n')
 print('F18 six exports complete')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
