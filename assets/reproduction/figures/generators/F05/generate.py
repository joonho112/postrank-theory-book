#!/usr/bin/env python3
"""Original symbolic map of four alternative decisions from one posterior.
No numerical posterior, ranks, selected members or optimized grade is invented.
"""
from pathlib import Path
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
ROOT=fs.ROOT;HERE=Path(__file__).resolve();FID='F05';STEM='f05-one-posterior-several-decision-problems';BOOK=ROOT/'chapters/05-bayesian-ranking.qmd';DEST=ROOT/'evidence/figures/builds/F05.json'
CARDS=[
 {'id':'values','title':'Estimate values','target':r'$\theta_i$','loss':'Squared value error','output':'Posterior means '+r'$E(\theta_i\mid y)$','mobile_loss':'Squared value error','mobile_output':'Posterior mean\n'+r'$E(\theta_i\mid y)$'},
 {'id':'ranks','title':'Estimate ranks','target':r'$R_i^{\downarrow}$','loss':'Squared rank error','output':r'$E(R_i^{\downarrow}\mid y)$'+' may be noninteger;\nreal-valued; no permutation constraint','mobile_loss':'Squared rank error','mobile_output':r'$E(R_i^{\downarrow}\mid y)$'+'\nMay be noninteger;\nNo permutation required'},
 {'id':'topset','title':'Select a fixed top set','target':r'$T_b(\theta)$','loss':'Symmetric top-set misclassification','output':'Choose b largest membership probabilities;\ninternal order unspecified','mobile_loss':'Top-set errors;\nfixed size b','mobile_output':'Top membership\nprobabilities; b units\nNo within-set order'},
 {'id':'grades','title':'Report common grades','target':'Pairwise directions','loss':'Directional errors + withholding','output':'Jointly coherent ordered blocks;\nwithin-grade comparisons withheld','mobile_loss':'Direction errors\nand withholding','mobile_output':r'$(B_1,\ldots,B_G)$'+'\nCoherent partition;\nwithin-grade silence'},
]
def card(ax,rect,item,mobile):
 x,y,w,h=rect;outer=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.004,rounding_size=0.008',facecolor=fs.PALETTE['white'],edgecolor=fs.PALETTE['line'],linewidth=1,zorder=2);ax.add_patch(outer);texts=[]
 def tx(field,xx,yy,label,size,weight='normal'):
  a=ax.text(x+w*xx,y+h*yy,label,ha='left',va='center',fontsize=size,fontweight=weight,color=fs.PALETTE['ink'],linespacing=1.15,zorder=3);texts.append((field,a))
 tx('title',.03,.91,item['title'],15 if mobile else 13.5,'semibold')
 for role,yy in [('target',.68),('loss',.46),('output',.17)]:
  tx(role+' label',.03,yy,role.capitalize(),14 if mobile else 11.5,'semibold')
  value=item.get('mobile_'+role,item[role]) if mobile else item[role]
  tx(role+' content',.27 if mobile else .20,yy,value,14 if mobile else 12)
 return outer,texts

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 10,16.4 if mobile else 9.2,mobile);ax=fs.diagram_axis(fig,(.025,.08,.95,.85) if mobile else (.02,.11,.96,.82))
 if mobile:
  hubrect=(.25,.84,.70,.09);rects=[(.22,y,.75,.155) for y in [.64,.455,.27,.085]];busx=.08
  fig.text(.04,.986,'One posterior,\nseveral decision problems',ha='left',va='top',fontsize=15.5,fontweight='semibold')
  fig.text(.04,.014,'Same scalar posterior; no latent ties.\nValue loss: finite second moments.\nTop-set size b is fixed.\nBranches specify alternative tasks.',ha='left',va='bottom',fontsize=14,linespacing=1.2,color=fs.PALETTE['muted'])
 else:
  hubrect=(.025,.435,.23,.17);rects=[(.35,y,.62,.19) for y in [.76,.53,.30,.07]];busx=.30
  fig.text(.025,.981,'One posterior, several decision problems',ha='left',va='top',fontsize=16,fontweight='semibold')
  fig.text(.025,.025,'Fixed scalar posterior; no latent ties. Value loss assumes finite second moments; top-set size b is fixed.\nArrows specify alternative decision problems, not method ancestry or a processing sequence.',ha='left',va='bottom',fontsize=11.5,linespacing=1.25,color=fs.PALETTE['muted'])
 hub=fs.box(ax,*hubrect,'One supplied\njoint posterior\n'+r'$\Pi_s(\theta\mid y)$',fc=fs.PALETTE['light'],ec=fs.PALETTE['teal'],size=14 if mobile else 13,weight='semibold');hubtext=ax.texts[-1];drawn=[]
 for rect,item in zip(rects,CARDS):drawn.append((item['id'],*card(ax,rect,item,mobile)))
 mids=[y+h/2 for x,y,w,h in rects];hy=hubrect[1]+hubrect[3]/2
 if mobile:
  ax.plot([hubrect[0]-.013,busx],[hy,hy],color=fs.PALETTE['muted'],linewidth=1.3,zorder=1)
  ax.plot([busx,busx],[hy,min(mids)],color=fs.PALETTE['muted'],linewidth=1.3,zorder=1)
 else:
  ax.plot([hubrect[0]+hubrect[2]+.013,busx],[hy,hy],color=fs.PALETTE['muted'],linewidth=1.3,zorder=1)
  ax.plot([busx,busx],[min(mids),max(mids)],color=fs.PALETTE['muted'],linewidth=1.3,zorder=1)
 for rect,(_,patch,_) in zip(rects,drawn):
  x,y,w,h=rect;fs.arrow(ax,(busx,y+h/2),(x,y+h/2),patchB=patch)
 fig.canvas.draw();renderer=fig.canvas.get_renderer();checks=[]
 objects=[('posterior',hub,[('hub',hubtext)])]+drawn
 for cid,patch,texts in objects:
  rb=patch.get_window_extent(renderer);boxes=[]
  for role,t in texts:
   bb=t.get_window_extent(renderer);inside=bool(bb.x0>=rb.x0+2 and bb.x1<=rb.x1-2 and bb.y0>=rb.y0+2 and bb.y1<=rb.y1-2);checks.append({'card':cid,'role':role,'inside':inside,'font_pt':t.get_fontsize()});boxes.append((role,bb))
  for i,(role,bb) in enumerate(boxes):
   for role2,bb2 in boxes[i+1:]:
    if bb.overlaps(bb2):raise RuntimeError('Text overlap: '+cid+' '+role+' / '+role2)
 if not all(x['inside'] for x in checks):raise RuntimeError('Card clipping: '+str([x for x in checks if not x['inside']]))
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,16.4] if mobile else [10,9.2],'card_order':[x['id'] for x in CARDS],'text_checks':checks,'no_card_to_card_arrows':True,'branch_count':4,'mobile_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}

def generate(overwrite=False):
 old=json.loads(DEST.read_text()) if DEST.exists() else None;targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(x.exists() for x in targets)):raise SystemExit('Existing outputs; --overwrite is for an authorized recorded repair.')
 outputs=[];geometry=[]
 for mobile in [False,True]:
  files,ck=draw(mobile);outputs.extend(files);geometry.append(ck)
 assert geometry[0]['card_order']==geometry[1]['card_order'];assert [x['path'] for x in outputs]==[str(x.relative_to(ROOT)) for x in targets]
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs=[BASE/'figstyle.py',HERE]
 d={'id':FID,'step':'3.9','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','author':'JoonHo Lee (jlee296@ua.edu)','command':'python -B assets/reproduction/figures/generators/F05/generate.py'+(' --overwrite' if overwrite else ''),'scope':'Original symbolic conceptual map of four native action/loss choices from one fixed scalar posterior. No numeric posterior,rank,selected units or optimized grades computed.','inputs':[{'path':str(x.relative_to(ROOT)),'sha256':h(x)} for x in inputs],'source_refs':[str(BOOK.relative_to(ROOT))],'outputs':outputs,'native_task_labels':CARDS,'geometry_checks':geometry,'actual_image_views':[],'execution':{'python':platform.python_version(),'renderer_invocations_total':1 if old is None else old['execution']['renderer_invocations_total']+1,'last_command_invocations':1,'last_command_layout_exports':2,'last_command_asset_exports':6,'scientific_calculations':0,'R_package_runs':0,'optimizer_runs':0,'canonical_edits':0,'register_edits':0},'scientific_boundaries':['Real-valued expected rank may be noninteger and is not displayed as a permutation.','Top-set internal order is unspecified; fixedb and finite-collection membership remain distinct from population-tail selection.','Grade output is symbolic coherent blocks,not a calculated optimum or specific assignment.','Moment/no-tie/cardinality assumptions are visible; branches are parallel tasks,not chronology or dominance.'],'limits':['Color/grayscale and actual final chapter context are not accepted by this author build.','Public literal drawing source and shared style suffice; chapter source_refs are descriptive metadata, not required runtime files.'],'required_repairs_remaining':[]}
 if old:d['previous_execution_history']=old.get('previous_execution_history',[])+[{'outputs':old['outputs'],'execution':old['execution'],'actual_image_views':old.get('actual_image_views',[])}]
 DEST.parent.mkdir(exist_ok=True,parents=True);DEST.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'id':FID,'outputs':outputs,'geometry':'PASS'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
