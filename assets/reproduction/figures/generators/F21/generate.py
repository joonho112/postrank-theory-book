"""Original illustrative communication specimen; no data are analyzed.

Literal labels and schematic grade bands explain the canonical Chapter21
recommendations. No private contract, chapter, registry or evidence input is
required. A prior own receipt is optional audit bookkeeping only.
"""
from pathlib import Path
import sys, json, hashlib, datetime, argparse
BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle

ROOT=fs.ROOT; HERE=Path(__file__).resolve()
STEM='f21-a-grade-report-a-reader-can-inspect'
DEST=ROOT/'evidence/figures/builds/F21.json'
CARDS=[
 ('Read the grade','Earlier: adopted-rule priority.\nShared: no internal direction.\nKeep criterion profiles visible.'),
 ('Inspect the release','Declare targets and a / w / τ.\nRecord origins and restrictions.\nKeep data/model/policy versions.'),
 ('Read the uncertainty','Summaries depend on the model.\nSeparate preferences and numerics.\nNo disclosure: fraction undefined.'),
 ('Specify the next action','Eligibility, budget and selection\nneed a separate published rule.\nBenefit requires intervention analysis.')]
ROUTES=[
 ('Input or computational error?','→ Correction review\nRecalculate; record cohort\nand version changes.'),
 ('Meaning or priority disputed?','→ Adopting authority\nRecord its decision or\nunresolved disagreement.')]

def identity(path):
 return {'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 11.8,25.5 if mobile else 13.2,mobile)
 ax=fs.diagram_axis(fig,[.045,.025,.91,.875]);ax.set(xlim=(-.025,1.025),ylim=(-.025,1.025))
 fig.text(.045,.984,'A grade report\na reader can inspect' if mobile else 'A grade report a reader can inspect',ha='left',va='top',fontsize=16 if mobile else 19,fontweight='bold',linespacing=1.15)
 fig.text(.045,.942 if mobile else .945,'ILLUSTRATIVE DESIGN\nNO DATA ANALYZED' if mobile else 'ILLUSTRATIVE DESIGN • NO DATA ANALYZED',ha='left',va='top',fontsize=14 if mobile else 13.5,fontweight='bold',color=fs.PALETTE['teal'],linespacing=1.2)
 checks=[]
 def card(x,y,w,h,title,body,fc='white',size=None):
  p=fs.box(ax,x,y,w,h,'',fc=fs.PALETTE[fc]);size=size or (14 if mobile else 12.5)
  t=ax.text(x+.025,y+h*.81,title,ha='left',va='center',fontsize=14 if mobile else 13.5,fontweight='bold',linespacing=1.2)
  b=ax.text(x+.025,y+h*.36,body,ha='left',va='center',fontsize=size,linespacing=1.28)
  checks.extend([(p,t),(p,b)]);return p
 if mobile:
  card(0,.900,1,.090,'Release fields to complete','Population and period: [declare]\nData/model/policy versions: [record]\nAdopting authority: [name role]','light')
  sy=.755
  positions=[(0,.610,1,.100),(0,.475,1,.100),(0,.340,1,.100),(0,.205,1,.100)]
  routepositions=[(0,.100,1,.075),(0,-.010,1,.075)]
 else:
  card(0,.885,1,.105,'Release fields to complete','Population and period: [declare]     Data/model/policy versions: [record]\nAdopting authority: [name role]','light')
  sy=.735
  positions=[(0,.505,.47,.18),(.53,.505,.47,.18),(0,.285,.47,.18),(.53,.285,.47,.18)]
  routepositions=[(0,.025,.47,.20),(.53,.025,.47,.20)]
 # Schematic layout, not a calculated report. Box areas encode no magnitude.
 ax.text(0,sy+.115,'Label convention • schematic only',ha='left',va='bottom',fontsize=14 if mobile else 13.5,fontweight='bold')
 ordered=Rectangle((0,sy),.62,.095,facecolor='white',edgecolor=fs.PALETTE['ink'],lw=1.2);ax.add_patch(ordered)
 ax.plot([.31,.31],[sy,sy+.095],color=fs.PALETTE['ink'],lw=1.2)
 for x,unit,meaning in [(.155,'A','Earlier'),(.465,'B, C','Shared')]:
  a=ax.text(x,sy+.068,unit,ha='center',va='center',fontsize=15,fontweight='bold')
  b=ax.text(x,sy+.027,meaning,ha='center',va='center',fontsize=14 if mobile else 12.5)
  checks.extend([(ordered,a),(ordered,b)])
 status=Rectangle((.70,sy),.30,.095,facecolor=fs.PALETTE['light'],edgecolor=fs.PALETTE['line'],lw=1.2);ax.add_patch(status)
 a=ax.text(.85,sy+.070,'Not\nassessed' if mobile else 'Unassessed',ha='center',va='center',fontsize=14 if mobile else 12.5,fontweight='bold',linespacing=1.1)
 b=ax.text(.85,sy+.025,'Outside\ngrades',ha='center',va='center',fontsize=14 if mobile else 12,linespacing=1.0)
 checks.extend([(status,a),(status,b)])
 for (title,body),(x,y,w,h) in zip(CARDS,positions):card(x,y,w,h,title,body)
 for (title,body),(x,y,w,h) in zip(ROUTES,routepositions):card(x,y,w,h,title,body,'light')
 fig.canvas.draw();ren=fig.canvas.get_renderer()
 for patch,t in checks:
  bb=patch.get_window_extent(ren);tb=t.get_window_extent(ren)
  assert tb.x0>=bb.x0+1 and tb.x1<=bb.x1-1 and tb.y0>=bb.y0+1 and tb.y1<=bb.y1-1,('card clipping',t.get_text())
 texts=[t for patch,t in checks]+list(fig.texts)+[t for t in ax.texts if t not in [x for p,x in checks] and t.get_text()]
 for i,t in enumerate(texts):
  bb=t.get_window_extent(ren)
  assert bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1,('canvas',t.get_text())
  for u in texts[i+1:]:assert not bb.overlaps(u.get_window_extent(ren)),('text overlap',t.get_text(),u.get_text())
 patches=list(dict.fromkeys(p for p,t in checks))
 for i,patch in enumerate(patches):
  for other in patches[i+1:]:assert not patch.get_window_extent(ren).overlaps(other.get_window_extent(ren)),('patch overlap',i)
 for t in texts:
  for patch in patches:
   if not any(own is patch and txt is t for own,txt in checks):assert not t.get_window_extent(ren).overlaps(patch.get_window_extent(ren)),('text meets another panel',t.get_text())
 return fig,{'mobile':mobile,'card_text_containment':len(checks),'canvas_and_text_nonoverlap':True,'minimum_core_font_pt':14 if mobile else 12,'mobile_css_core_px_at332':14*332/(4.8*72) if mobile else None,'science':'No data or numerical target; grade bands and release fields are explicitly schematic.'}

def main(overwrite=False):
 old=json.loads(DEST.read_text()) if DEST.exists() else {}
 assert overwrite or not old,'Existing outputs require recorded --overwrite.'
 history=old.get('execution_history',[]);a={'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'python -B assets/reproduction/figures/generators/F21/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_writes':0,'layout_exports':0};history.append(a)
 r={'id':'F21','author':'JoonHo Lee (jlee296@ua.edu)','scope':'Original illustrative communication specimen, no data analyzed. Literal public labels and shared style; no fitted/model/solver/simulation run.','inputs':[identity(p) for p in [HERE,BASE/'figstyle.py']],'source_provenance':'Canonical Chapter21 governance/communication recommendations and hypothetical model explanation; no chapter runtime read.','execution_history':history,'outputs':[],'geometry_checks':[],'actual_image_views':old.get('actual_image_views',[]),'repairs':old.get('repairs',[])}
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
