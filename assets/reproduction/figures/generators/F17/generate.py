#!/usr/bin/env python3
"""Original comparator specification map; symbolic actions, no numeric fixture."""
from pathlib import Path
import sys,json,datetime,hashlib,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;HERE=Path(__file__).resolve();STEM='f17-a-fair-comparator-specification';DEST=ROOT/'evidence/figures/builds/F17.json'
CARDS=[('Score tiers',r'$g=\mathrm{tiers}(u)$','Declare score scale and reference.\nPreserve its tie rule and actual grades.\nConstructed recipe; no general\nreporting-loss optimality guarantee.'),('Reporting optimizer',r'$g^*\in\arg\min_{g\in\mathcal{F}}R(g)$','Minimize the declared reporting risk.\nExact claims need exact coefficients\nand the entire feasible family.\nKeep its law, objective and restrictions.'),('Exact-budget selection',r'$S\subseteq\{1,\ldots,n\},\quad |S|=b$','Maximize conditional mean utilities\nsummed over the selected subset.\nConverting a grade into an allocation\nrequires another explicit rule.'),('Threshold classification',r'$a_i\in\{0,1\}$','Declare the event and both error costs.\nThe simple cutoff assumes unrestricted\nbinary declarations. Combining flags\ninto grades requires a reporting check.')]

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 11.8,22 if mobile else 11.6,mobile);ax=fs.diagram_axis(fig,[.035,.025,.93,.925]);ax.set(xlim=(-.025,1.025),ylim=(-.025,1.025));objects=[]
 fig.text(.04,.985,'Specify a comparator\nbefore comparing performance' if mobile else 'Specify a comparator before comparing performance',va='top',fontsize=16 if mobile else 18,weight='semibold')
 def text(x,y,s,size=14,weight='normal',va='center'):return ax.text(x,y,s,fontsize=size,weight=weight,va=va,ha='left',linespacing=1.25)
 def panel(x,y,w,h,heading,body,fc='white',body_size=14):
  patch=fs.box(ax,x,y,w,h,'',fc=fs.PALETTE[fc]);a=text(x+.025,y+h*.82,heading,14 if mobile else 13.5,'semibold');b=text(x+.025,y+h*.34,body,body_size);objects.extend([(patch,a),(patch,b)]);return patch
 if mobile:
  panel(0,.865,1,.085,'The shared comparator contract','Information • target and law • units\nSource role • ties and constraints','light')
  for i,(heading,action,body) in enumerate(CARDS):
   y=.66-i*.165;p=fs.box(ax,0,y,1,.130,'',fc='white');a=text(.025,y+.122,heading,15,'semibold');b=text(.025,y+.088,action,14);c=text(.025,y+.035,body,14);objects.extend([(p,t) for t in [a,b,c]])
  panel(0,.035,1,.100,'A new combined report','Criterion cards → midrank sum/max\n→ combined report (constructed).\nNo automatic joint optimum,\nprotection or inherited grade cap.','light')
  fig.text(.04,.006,'Choose fixed τ, matched expected N,\nor exact G/block-size matching.\nEvaluate both co-primary targets.',va='bottom',fontsize=14,color=fs.PALETTE['muted'],linespacing=1.2)
 else:
  panel(0,.855,1,.095,'The shared comparator contract','Information • target and law • eligible units • evidence role • ties and constraints','light',12.5)
  for i,(heading,action,body) in enumerate(CARDS):
   x=0 if i%2==0 else .53;y=.565 if i<2 else .285;p=fs.box(ax,x,y,.47,.235,'',fc='white');a=text(x+.025,y+.200,heading,14,'semibold');b=text(x+.025,y+.150,action,14);c=text(x+.025,y+.062,body,12.5);objects.extend([(p,t) for t in [a,b,c]])
  panel(0,.120,1,.115,'A new combined report','Separate criterion cards → declared midrank sum/maximum → combined report\nConstructed adaptation: no automatic joint optimum, protection or inherited grade cap.','light',12.5)
  panel(0,.005,1,.070,'Choose the operating-point comparison','Fixed τ  •  matched expected N  •  exact G / block sizes; evaluate both co-primary targets.','white',12.5)
 fig.canvas.draw();r=fig.canvas.get_renderer()
 for p,t in objects:
  bb=p.get_window_extent(r);tb=t.get_window_extent(r);ab=ax.get_window_extent(r);assert bb.x0>=ab.x0 and bb.x1<=ab.x1 and bb.y0>=ab.y0 and bb.y1<=ab.y1,('patchoutsideaxes',t.get_text());assert tb.x0>=bb.x0+1 and tb.x1<=bb.x1-1 and tb.y0>=bb.y0+1 and tb.y1<=bb.y1-1,('cardclipping',t.get_text())
 texts=[t for _,t in objects]+list(fig.texts)
 for i,t in enumerate(texts):
  bb=t.get_window_extent(r);assert bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height,('canvas',t.get_text())
  for u in texts[i+1:]:assert not bb.overlaps(u.get_window_extent(r)),('overlap',t.get_text(),u.get_text())
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'text_containment_checks':len(objects),'all_canvas_and_nonoverlap':True,'encoding':'No numeric axis/areas; action formulas and original conceptual labels only.'}

def main(overwrite):
 old=json.loads(DEST.read_text()) if DEST.exists() else {};assert overwrite or not old,'Existing outputs require recorded --overwrite.'
 h=old.get('execution_history',[]);a={'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':'python -B assets/reproduction/figures/generators/F17/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_writes':0,'layout_exports':0};h.append(a)
 d={'id':'F17','author':'JoonHo Lee (jlee296@ua.edu)','scope':'Conceptual source-based native-action/operating-point map; no numerical fixture, scientific model, optimization or simulation.','inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,BASE/'figstyle.py']],'outputs':[],'geometry_checks':[],'execution_history':h,'actual_image_views':old.get('actual_image_views',[])};DEST.parent.mkdir(parents=True,exist_ok=True)
 try:
  for m in [False,True]:
   out,g=draw(m);d['outputs']+=out;d['geometry_checks'].append(g);a['asset_writes']+=3;a['layout_exports']+=1
  a['status']='succeeded'
 except Exception as ex:a['status']='failed';a['error']=str(ex);raise
 finally:
  a['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['execution']={'producer_commands':len(h),'complete_commands':sum(x['status']=='succeeded' for x in h),'failed_commands':sum(x['status']=='failed' for x in h),'asset_writes':sum(x['asset_writes'] for x in h),'model_simulation_solver_runs':0};DEST.write_text(json.dumps(d,indent=2)+'\n')
 print('F17 six exports complete')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
