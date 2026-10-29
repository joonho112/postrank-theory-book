#!/usr/bin/env python3
"""Three inspected software domains; conceptual capabilities, no package execution."""
from pathlib import Path
import sys,json,datetime,hashlib,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;HERE=Path(__file__).resolve();STEM='fd-software-domains-and-actual-capabilities';DEST=ROOT/'evidence/figures/builds/FD.json'
LANES=[
 ('Legacy canonical inputs',[
  ('INPUT','Joint or criterionwise\nequal-weight draws;\nexact finite law.\nTie-free input contract.'),
  ('PAIRWISE','postrank_pairwise\nWeak error event:\n'+r'$e_{ij}=P(\theta_i\leq\theta_j)$'),
  ('ELIGIBLE FAMILIES','Weighted or minimax;\ncap, exact G, q rows\nwhere supported and\nvalidated.'),
  ('LEGACY SOLVE','staged or label_mip\nLegacy fit and\naction evaluation.')]),
 ('Legacy typed coefficients',[
  ('INPUT','Conditional Gaussian\nor shared-state mixture.\nEntities independent\nconditional on state.'),
  ('TYPED ARTIFACT','postrank_coefficients\nMeans, probabilities\nand provenance\nstay together.'),
  ('WEIGHTED CAP ONLY','At most G;\nno q, exact G\nor minimax.'),
  ('LEGACY SOLVE','staged or label_mip\nLegacy fit and\naction evaluation.')]),
 ('Separate opt-in equality-neutral inputs',[
  ('INPUT','Joint equal-weight\ndraws or complete\nexact finite law;\nequality evidence.'),
  ('STRICT / EQUAL\n/ DISTINCT','postrank_tie_pairwise\n'+r'$b_{ij}=P(\theta_i<\theta_j)$'+'\n'+r'$d_{ij}=P(\theta_i\ne\theta_j)$'),
  ('WEIGHTED + GUARD','At most G; full\nactive-profile guard.\nOriginal entities and\npair frame retained.'),
  ('DEDICATED TIE SOLVE','label_mip only\nSeparate tie fit\nand evaluator.')])]
MOBILE=[
 ('Legacy canonical inputs','INPUT → PAIRWISE\nJoint/criterion equal-weight draws;\nor complete exact law.\nTie-free → weak error e.\n\nFAMILY → SOLVE\nValidated weighted/minimax;\ncap, exact G or q as supported.\nstaged or label_mip; legacy fit.'),
 ('Legacy typed coefficients','INPUT → TYPED COEFFICIENTS\nGaussian / shared-state mixture.\nEntities independent given that state;\nmeans and probabilities stay typed.\n\nFAMILY → SOLVE\nWeighted at-most-G only.\nstaged or label_mip; legacy fit.'),
 ('Separate equality-neutral opt-in','INPUT → STRICT / EQUAL / DISTINCT\nJoint equal-weight draws;\nor complete exact law.\nEquality evidence; separate objects.\n\nFAMILY → SOLVE\nWeighted at-most-G only.\nFull active-profile guard.\nOriginal units/pairs; label_mip only.\nDedicated tie fit and evaluation.')]

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 13.2,22 if mobile else 11.4,mobile);ax=fs.diagram_axis(fig,[.035,.025,.93,.91]);ax.set(xlim=(-.025,1.025),ylim=(-.025,1.025));objects=[]
 fig.text(.04,.985,'Input domains keep\ntheir own capabilities' if mobile else 'Input domains keep their own capabilities',va='top',fontsize=16 if mobile else 19,weight='semibold')
 if mobile:
  fig.text(.04,.930,'Inspected postrank 0.9.0 snapshots.\nNo package execution or new release.',va='top',fontsize=14,linespacing=1.2)
  for i,(title,body) in enumerate(MOBILE):
   y=.645-i*.235;p=fs.box(ax,0,y,1,.195,'',fc=fs.PALETTE['light'] if i==2 else 'white');t=ax.text(.025,y+.184,title,ha='left',va='top',fontsize=14,weight='semibold');b=ax.text(.025,y+.155,body,ha='left',va='top',fontsize=14,linespacing=1.2);objects.extend([(p,t),(p,b)])
  fig.text(.04,.155,'Not supplied by the opt-in route:',va='top',fontsize=14,weight='semibold')
  fig.text(.04,.130,'Criterionwise or typed inputs; staged;\nexact G, q, minimax; legacy reports,\nplots, MC diagnostics, IID/regret\nor protection-bound helpers.\n\nWeighted offsets: legacy τ; neutral R0.\nBackend explicit; no automatic fallback.\nNumerical status is not exact proof.',va='top',fontsize=14,linespacing=1.2)
 else:
  fig.text(.04,.938,'Dated postrank 0.9.0 correspondence: original legacy scope and the separately inspected opt-in expansion. No automatic object conversion.',va='top',fontsize=12.5)
  xs=[0,.27,.54,.81];w=.19
  for i,(title,cards) in enumerate(LANES):
   y=.640-i*.230;ax.text(.0,y+.190,title,ha='left',va='bottom',fontsize=14,weight='semibold')
   boxes=[]
   for x,(head,body) in zip(xs,cards):
    p=fs.box(ax,x,y,w,.170,'',fc=fs.PALETTE['light'] if i==2 else 'white');t=ax.text(x+.012,y+.151,head,ha='left',va='center',fontsize=11.7,weight='semibold');b=ax.text(x+.012,y+.072,body,ha='left',va='center',fontsize=12.2,linespacing=1.25);objects.extend([(p,t),(p,b)]);boxes.append(p)
   for j in range(3):fs.arrow(ax,(xs[j]+w,y+.0925),(xs[j+1],y+.0925),patchA=boxes[j],patchB=boxes[j+1])
  fig.text(.04,.125,'Not supplied by the opt-in route: criterionwise / typed inputs; staged; exact G, q or minimax;\nlegacy reports/plots, MC diagnostics, uniform IID, regret or protection-bound helpers.',va='top',fontsize=12.5,linespacing=1.25)
  fig.text(.04,.052,'Weighted-loss offsets: legacy τ; equality-neutral R0. Gurobi is the default; HiGHS must be selected explicitly, with no automatic fallback.\nSource/help inspection is not installed-runtime verification; returned numerical status or a zero gap is not an exact proof.',va='top',fontsize=11.8,color=fs.PALETTE['muted'],linespacing=1.25)
 fig.canvas.draw();r=fig.canvas.get_renderer();ab=ax.get_window_extent(r)
 for p,t in objects:
  pb=p.get_window_extent(r);tb=t.get_window_extent(r);assert pb.x0>=ab.x0 and pb.x1<=ab.x1 and pb.y0>=ab.y0 and pb.y1<=ab.y1,('patchbounds',t.get_text());assert tb.x0>=pb.x0+1 and tb.x1<=pb.x1-1 and tb.y0>=pb.y0+1 and tb.y1<=pb.y1-1,('cardtext',t.get_text())
 texts=[t for t in list(ax.texts)+list(fig.texts) if t.get_text().strip()]
 for i,t in enumerate(texts):
  bb=t.get_window_extent(r);assert bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height,('canvas',t.get_text())
  for u in texts[i+1:]:assert not bb.overlaps(u.get_window_extent(r)),('overlap',t.get_text(),u.get_text())
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'card_text_checks':len(objects),'all_patch_inside_axes':True,'all_text_canvas_and_nonoverlap':True,'numeric_data':'None; symbolic route/capability statements only.'}

def main(overwrite):
 old=json.loads(DEST.read_text()) if DEST.exists() else {};assert overwrite or not old,'Existing output; use --overwrite only for recorded repair/replay.'
 h=old.get('execution_history',[]);a={'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'python -B assets/reproduction/figures/generators/FD/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_writes':0,'layout_exports':0};h.append(a)
 d={'id':'FD','author':'JoonHo Lee (jlee296@ua.edu)','scope':'Original source-backed capability figure, no package/install/load/solve/model/simulation/numericfixture.','inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,BASE/'figstyle.py']],'outputs':[],'geometry_checks':[],'execution_history':h,'actual_image_views':old.get('actual_image_views',[])};DEST.parent.mkdir(parents=True,exist_ok=True)
 try:
  for m in [False,True]:
   out,g=draw(m);d['outputs']+=out;d['geometry_checks'].append(g);a['asset_writes']+=3;a['layout_exports']+=1
  a['status']='succeeded'
 except Exception as ex:a['status']='failed';a['error']=str(ex);raise
 finally:
  a['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['execution']={'producer_commands':len(h),'complete_commands':sum(x['status']=='succeeded' for x in h),'failed_commands':sum(x['status']=='failed' for x in h),'asset_writes':sum(x['asset_writes'] for x in h),'scientific_or_package_runs':0};DEST.write_text(json.dumps(d,indent=2)+'\n')
 print('FD exported; independent source/capability/actualpresentation checks remain')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
