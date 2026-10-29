#!/usr/bin/env python3
"""F03 original four-case field map, with public-only render inputs.
No numerical policy or empirical values are generated. SVG text is outlined.
"""
from pathlib import Path
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
ROOT=fs.ROOT;HERE=Path(__file__).resolve();FID='F03';STEM='f03-shared-comparison-structure-across-institutions';DEST=ROOT/'evidence/figures/builds/F03.json';SOURCE_REF='chapters/03-institutional-practice.qmd'
CASES=[
 {'id':'hospital','title':'Hospital stars','version':'CMS April 2026, methodology v5.1','unit':'Eligible acute-care hospital','evidence':'Mortality, safety, readmission;\nexperience and timely care','report':'Stars within peer groups;\npatient-safety cap','use':'Public information;\nbenefit not established here'},
 {'id':'clinical','title':'Clinical benefit–risk','version':'Li et al. (2019), creatine reanalysis','unit':'Treatment alternatives for\na specified patient','evidence':'Outcome predictions;\nproxy or simulated weights','report':'SMAA rank acceptability\n(method illustration)','use':'Analytical decision aid;\nadoption not established'},
 {'id':'spatial','title':'Spatial deprivation','version':'England IMD25 / Pride in Place 2026','unit':'LSOA index units;\nMSOA allocation units','evidence':'Deprivation domains;\ncommunity need in selection','report':'IMD25 ranks and deciles','use':'Selection adds aggregation;\ncohesion + constituency cap'},
 {'id':'employer','title':'Employer report cards','version':'KRW 2024; earlier audit data','unit':'Retained firms in the audit','evidence':'Race and gender contact gaps\nwith EB uncertainty','report':'Separate criterion grades\nand posterior summaries','use':'Public research disclosure;\ninvestigative uses proposed'}]

def panel(ax,rect,case,mobile=False):
 x,y,w,h=rect
 outer=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.004,rounding_size=0.008',facecolor=fs.PALETTE['white'],edgecolor=fs.PALETTE['line'],linewidth=1,zorder=1);ax.add_patch(outer)
 inner=FancyBboxPatch((x+w*.02,y+h*.02),w*.96,h*.19,boxstyle='round,pad=0.001,rounding_size=0.004',facecolor=fs.PALETTE['white'],edgecolor=fs.PALETTE['ochre'],linewidth=.9,zorder=2);ax.add_patch(inner)
 artists=[]
 def text(label,xx,yy,content,size,weight='normal',ha='left'):
  a=ax.text(x+w*xx,y+h*yy,content,ha=ha,va='center',fontsize=size,fontweight=weight,zorder=3,color=fs.PALETTE['ink'],linespacing=1.20);artists.append((label,a))
 text('case title',.035,.935,case['title'],15 if mobile else 13.5,'semibold')
 text('dated version',.035,.85,case['version'],14 if mobile else 11.5)
 for key,yy,label in [('unit',.68,'Unit'),('evidence',.50,'Evidence'),('report',.32,'Report'),('use',.115,'Use /\nlimit')]:
  text(key+' label',.035,yy,label,14 if mobile else 11.5,'semibold')
  text(key+' content',.32,yy,case[key],14 if mobile else 12)
 return outer,artists

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 10,16.8 if mobile else 8.8,mobile);ax=fs.diagram_axis(fig,(.025,.045,.95,.92) if mobile else (.02,.055,.96,.875))
 rects=[(.015,y,.97,.215) for y in [.75,.51,.27,.03]] if mobile else [(.025,.52,.46,.44),(.515,.52,.46,.44),(.025,.04,.46,.44),(.515,.04,.46,.44)]
 panels=[]
 for rect,case in zip(rects,CASES):panels.append((case['id'],*panel(ax,rect,case,mobile)))
 if mobile:
  fig.text(.04,.987,'One comparison structure,\nfour institutional decisions',ha='left',va='top',fontsize=15.5,fontweight='semibold')
  fig.text(.04,.012,'Common fields do not imply common\nobjectives, adoption, or effects.',ha='left',va='bottom',fontsize=14,linespacing=1.2,color=fs.PALETTE['muted'])
 else:
  fig.text(.025,.985,'Shared comparison structure across institutions',ha='left',va='top',fontsize=16,fontweight='semibold')
  fig.text(.025,.014,'The same descriptive fields preserve different units, objectives, adoption status, and decision rules.',ha='left',va='bottom',fontsize=11.5,color=fs.PALETTE['muted'])
 fig.canvas.draw();renderer=fig.canvas.get_renderer();checks=[]
 for cid,outer,artists in panels:
  rb=outer.get_window_extent(renderer);bbs=[]
  for label,artist in artists:
   tb=artist.get_window_extent(renderer);inside=bool(tb.x0>=rb.x0+2 and tb.x1<=rb.x1-2 and tb.y0>=rb.y0+2 and tb.y1<=rb.y1-2)
   checks.append({'case':cid,'field':label,'inside_card':inside,'font_pt':artist.get_fontsize()});bbs.append((label,tb))
  for i,(label,bb) in enumerate(bbs):
   for other,ob in bbs[i+1:]:
    if bb.overlaps(ob):raise RuntimeError('Text overlap: '+cid+' '+label+' / '+other)
 if not all(x['inside_card'] for x in checks):raise RuntimeError('Card clipping: '+str([x for x in checks if not x['inside_card']]))
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,16.8] if mobile else [10,8.8],'case_order':[x['id'] for x in CASES],'text_geometry_checks':checks,'all_card_text_nonoverlapping':True,'mobile_min_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}

def generate(overwrite=False):
 previous=json.loads(DEST.read_text()) if DEST.exists() else None
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(x.exists() for x in targets)):raise SystemExit('Refuse overwrite; use --overwrite only for an authorized recorded repair.')
 files=[];checks=[]
 for mobile in [False,True]:
  out,ck=draw(mobile);files.extend(out);checks.append(ck)
 assert [x['path'] for x in files]==[str(x.relative_to(ROOT)) for x in targets];assert checks[0]['case_order']==checks[1]['case_order']
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs=[BASE/'figstyle.py',HERE]
 d={'id':FID,'step':'3.7','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','author':'JoonHo Lee (jlee296@ua.edu)','command':'python -B assets/reproduction/figures/generators/F03/generate.py'+(' --overwrite' if overwrite else ''),'scope':'Original conceptual synthesis of four dated canonical Chapter3caseaccounts; no numeric policy thresholds,empirical estimates,shared loss or causal effect introduced.','inputs':[{'path':str(x.relative_to(ROOT)),'sha256':h(x)} for x in inputs],'source_refs':[SOURCE_REF],'outputs':files,'case_labels':CASES,'geometry_checks':checks,'actual_image_views':[],'execution':{'python':platform.python_version(),'renderer_invocations_total':1 if previous is None else previous['execution']['renderer_invocations_total']+1,'last_command_invocations':1,'last_command_layout_exports':2,'last_command_asset_exports':6,'scientific_calculations':0,'R_package_runs':0,'optimizer_runs':0,'canonical_edits':0,'register_edits':0},'limits':['No fresh policy/source-paper verification; canonical chapter defines all versions and source boundaries.','Public generator/style suffice; the canonical chapter is descriptive provenance. Private contracts/registries are not required.'],'required_repairs_remaining':[]}
 if previous:d['previous_execution_history']=previous.get('previous_execution_history',[])+[{'outputs':previous['outputs'],'execution':previous['execution'],'actual_image_views':previous.get('actual_image_views',[])}]
 DEST.parent.mkdir(exist_ok=True,parents=True);DEST.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'id':FID,'outputs':files,'geometry':'PASS'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
