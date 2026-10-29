"""Original Chapter22 synthesis: distinguish claim roles, not evidence ranks.
Literal public labels and public style only. No scientific data are generated;
no private contract, source chapter, log or registry is a plotting dependency.
"""
from pathlib import Path
import sys,json,hashlib,datetime,argparse
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;HERE=Path(__file__).resolve()
STEM='f22-established-results-and-the-p1-research-agenda'
DEST=ROOT/'evidence/figures/builds/F22.json'
LAYERS=[
 ('Inherited foundations','Posterior decisions: specified loss.\nBayesian ranking: estimate/rank/select.\nKRW: coherent scalar report cards.','Inheritance,\nwith attribution.'),
 ('Adaptations and derivations','Coherent common reports and pair costs.\nDomain-specific optimization/bounds.\nMatched disclosure; evaluation laws.','Conditions: law, loss,\nfamily and assumptions.'),
 ('Documented software routes','Historical weak-error route.\nGuarded equality-neutral subset.\nImplementation scope is limited.','Not every theorem,\nprotection or diagnostic.'),
 ('Prospective P1 evidence','Differences, decomposition, settings.\nCosts under other native objectives.\nCalibration under an evaluation law.','The main empirical study\nremains prospective.')]

def identity(path):
 return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 11.8,22.2 if mobile else 13.4,mobile)
 ax=fs.diagram_axis(fig,[.045,.06,.91,.83]);ax.set(xlim=(-.025,1.025),ylim=(-.025,1.025))
 fig.text(.045,.985,'Established results and\nthe P1 research agenda' if mobile else 'Established results and the P1 research agenda',ha='left',va='top',fontsize=16 if mobile else 19,fontweight='bold',linespacing=1.15)
 fig.text(.045,.936 if mobile else .94,'Different claim roles;\nno implied empirical completion' if mobile else 'Different claim roles; no implied empirical completion',ha='left',va='top',fontsize=14 if mobile else 13.5,color=fs.PALETTE['muted'],linespacing=1.2)
 checks=[];patches=[]
 def card(x,y,w,h,title,body,fc='white'):
  p=fs.box(ax,x,y,w,h,'',fc=fs.PALETTE[fc]);patches.append(p)
  t=ax.text(x+.025,y+h*.83,title,ha='left',va='center',fontsize=14 if mobile else 13.5,fontweight='bold')
  b=ax.text(x+.025,y+h*.36,body,ha='left',va='center',fontsize=14 if mobile else 12.5,linespacing=1.25)
  checks.extend([(p,t),(p,b)]);return p
 card(0,.885,1,.105,'Keep both targets visible','Composite magnitudes: coefficients a.\nCriterion-direction errors: weights w.','light')
 for index,((title,body,scope),y) in enumerate(zip(LAYERS,[.690,.520,.350,.180])):
  p=fs.box(ax,0,y,1,.140,'',fc=fs.PALETTE['white']);patches.append(p)
  if mobile:
   title=title.replace('Adaptations and derivations','Adaptations and derivations')
   t=ax.text(.025,y+.140*.84,title,ha='left',va='center',fontsize=14,fontweight='bold')
   b=ax.text(.025,y+.140*.49,body,ha='left',va='center',fontsize=14,linespacing=1.25)
   s=ax.text(.025,y+.140*.15,scope.replace('\n',' '),ha='left',va='center',fontsize=14,color=fs.PALETTE['teal'] if index!=3 else fs.PALETTE['rust'],linespacing=1.2)
   # Keep longer qualification labels on two lines rather than shrink them.
   if index==1:s.set_text('Conditions: law, loss, family\nand assumptions.')
   if index==2:s.set_text('Not every theorem, protection\nor diagnostic.')
   if index==3:s.set_text('The main empirical study\nremains prospective.')
  else:
   title=title.replace('Adaptations and derivations','Adaptations and\nderivations')
   t=ax.text(.025,y+.140*.77,title,ha='left',va='center',fontsize=14,fontweight='bold',linespacing=1.2)
   s=ax.text(.025,y+.140*.25,scope,ha='left',va='center',fontsize=12.5,color=fs.PALETTE['teal'] if index!=3 else fs.PALETTE['rust'],linespacing=1.2)
   b=ax.text(.385,y+.140*.50,body,ha='left',va='center',fontsize=12.5,linespacing=1.3)
  checks.extend([(p,t),(p,b),(p,s)])
 evidence='Exact examples: possibilities\nunder declared finite laws.\nTwo KRW actions: bounded consistency,\nnot a superior frontier or\nproducer validation.' if mobile else 'Exact finite examples show possibilities under declared laws.\nTwo KRW action reconstructions support bounded consistency, not a superior frontier or producer validation.'
 card(0,.020,1,.115,'Bounded illustrations',evidence,'light')
 fig.text(.045,.012,'Measurement validity, authorized\npreferences and causal benefit still\nneed their own evidence.' if mobile else 'Measurement validity • authorized preferences • causal benefit: further evidence required.',ha='left',va='bottom',fontsize=14 if mobile else 12.5,linespacing=1.2,color=fs.PALETTE['muted'])
 fig.canvas.draw();ren=fig.canvas.get_renderer()
 for p,t in checks:
  bb=p.get_window_extent(ren);tb=t.get_window_extent(ren)
  assert tb.x0>=bb.x0+1 and tb.x1<=bb.x1-1 and tb.y0>=bb.y0+1 and tb.y1<=bb.y1-1,('card clipping',t.get_text())
 texts=[t for p,t in checks]+list(fig.texts)
 for i,t in enumerate(texts):
  bb=t.get_window_extent(ren);assert bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1,('canvas',t.get_text())
  for u in texts[i+1:]:assert not bb.overlaps(u.get_window_extent(ren)),('text overlap',t.get_text(),u.get_text())
  for p in patches:
   if not any(own is p and obj is t for own,obj in checks):assert not bb.overlaps(p.get_window_extent(ren)),('text meets another panel',t.get_text())
 for i,p in enumerate(patches):
  for q in patches[i+1:]:assert not p.get_window_extent(ren).overlaps(q.get_window_extent(ren)),('patch overlap',i)
 return fig,{'mobile':mobile,'equal_claim_role_bands':4,'card_text_containment_checks':len(checks),'patches':len(patches),'canvas_text_and_patch_nonoverlap':True,'minimum_core_font_pt':14 if mobile else 12.5,'mobile_core_css_px_at332':14*332/(4.8*72) if mobile else None,'meaning':'No scientific data, axes, empirical completion or inference arrows.'}

def main(overwrite=False):
 old=json.loads(DEST.read_text()) if DEST.exists() else {};assert overwrite or not old,'Existing outputs require recorded --overwrite.'
 history=old.get('execution_history',[]);a={'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'python -B assets/reproduction/figures/generators/F22/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_writes':0,'layout_exports':0};history.append(a)
 r={'id':'F22','author':'JoonHo Lee (jlee296@ua.edu)','scope':'Original conceptual synthesis, literal public labels and shared style. No new result, software audit, scientific coordinates, empirical data, model, solver or simulation.','source_provenance':'Canonical Chapter22 inheritance, established-results, prospective P1 and open-agenda distinctions; no QMD runtime read.','inputs':[identity(p) for p in [HERE,BASE/'figstyle.py']],'execution_history':history,'outputs':[],'geometry_checks':[],'actual_image_views':old.get('actual_image_views',[]),'repairs':old.get('repairs',[])}
 DEST.parent.mkdir(parents=True,exist_ok=True)
 try:
  for mobile in [False,True]:
   fig,g=draw(mobile);r['outputs']+=fs.export(fig,STEM,mobile);r['geometry_checks'].append(g);a['asset_writes']+=3;a['layout_exports']+=1
  a['status']='succeeded'
 except Exception as ex:a['status']='failed';a['error']=str(ex);raise
 finally:
  a['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();r['execution']={'producer_commands':len(history),'complete_commands':sum(x['status']=='succeeded' for x in history),'failed_commands':sum(x['status']=='failed' for x in history),'asset_writes':sum(x['asset_writes'] for x in history),'layout_exports':sum(x['layout_exports'] for x in history),'science_program_runs':0};DEST.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({'outputs':r['outputs'],'execution':r['execution']},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
