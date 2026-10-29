#!/usr/bin/env python3
"""F01: original conceptual decision map; no scientific numerical inputs.
Run with an existing Matplotlib environment. SVG labels use portable outlines.
"""
from pathlib import Path
import sys,json,hashlib,datetime,platform,argparse
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;HERE=Path(__file__).resolve();FID='F01';STEM='f01-from-noisy-indicators-to-a-reporting-decision'
SOURCE_REF='chapters/01-public-decisions.qmd';DEST=ROOT/'evidence/figures/builds/F01.json'
GEO={False:{'purpose':(.015,.61,.205,.19),'evidence':(.27,.61,.205,.19),'choice':(.525,.61,.205,.19),'report':(.78,.61,.205,.19),'rules':(.26,.09,.32,.19),'action':(.65,.09,.32,.19)},True:{'purpose':(.12,.82,.76,.10),'evidence':(.12,.65,.76,.10),'choice':(.12,.48,.76,.10),'report':(.12,.28,.76,.15),'rules':(.035,.04,.43,.15),'action':(.55,.04,.415,.15)}}
LABELS={'purpose':'Declare purpose\nand targets','evidence':'Represent\nuncertain evidence','choice':'Choose comparisons:\nissue or withhold','report':'Common grades:\nordered groups','rules':'Additional institutional\nrules and evidence','action':'Institutional action\n(assistance or enrollment)'}
def port(rect,side,f=.5):
 x,y,w,h=rect
 return {'left':(x,y+h*f),'right':(x+w,y+h*f),'top':(x+w*f,y+h),'bottom':(x+w*f,y)}[side]
def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 10,11.5 if mobile else 6.5,mobile)
 ax=fs.diagram_axis(fig,(.025,.07,.95,.88) if mobile else (.02,.07,.96,.83));geo=GEO[mobile];nodes={};texts={};size=14 if mobile else 12.5
 for key,rect in geo.items():
  text=LABELS[key]
  if mobile and key=='report':text='Common grades\nAcross groups: issue a direction\nWithin groups: withhold it'
  if mobile and key=='rules':text='Additional rules\nand evidence'
  if mobile and key=='action':text='Institutional action\n(assistance or\nenrollment)'
  ec=fs.PALETTE['teal'] if key in ['choice','report'] else fs.PALETTE['ochre'] if key in ['rules','action'] else fs.PALETTE['line']
  fc=fs.PALETTE['light'] if key in ['choice','report'] else fs.PALETTE['white']
  nodes[key]=fs.box(ax,*rect,text,fc=fc,ec=ec,size=size,weight='semibold' if key in ['choice','report'] else 'normal');texts[key]=ax.texts[-1]
 if mobile:
  edges=[('purpose','bottom',.5,'evidence','top',.5),('evidence','bottom',.5,'choice','top',.5),('choice','bottom',.5,'report','top',.5),('report','bottom',.60,'action','top',.5),('rules','right',.5,'action','left',.5)]
  fig.text(.04,.986,'From noisy indicators\nto a reporting decision',ha='left',va='top',fontsize=15.5,fontweight='semibold')
  fig.text(.04,.02,'A shared grade withholds a direction.\nArrows are analytical, not causal.',ha='left',va='bottom',fontsize=14,linespacing=1.2,color=fs.PALETTE['muted'])
 else:
  edges=[('purpose','right',.5,'evidence','left',.5),('evidence','right',.5,'choice','left',.5),('choice','right',.5,'report','left',.5),('report','bottom',.5,'action','top',.74),('rules','right',.5,'action','left',.5)]
  fig.text(.025,.971,'From noisy indicators to a reporting decision',ha='left',va='top',fontsize=16,fontweight='semibold')
  ax.text(.015,.91,'Construct the common report',ha='left',va='center',fontsize=13,fontweight='semibold')
  ax.text(.035,.515,'Across grades: a direction is reported.\nWithin a grade: the direction is withheld.',ha='left',va='top',fontsize=12.5,linespacing=1.3,color=fs.PALETTE['muted'])
  ax.plot([.015,.98],[.365,.365],color=fs.PALETTE['line'],linewidth=.8,zorder=0)
  ax.text(.015,.325,'Use the report with further institutional rules',ha='left',va='center',fontsize=13,fontweight='semibold')
  fig.text(.025,.025,'Arrows show analytical dependencies and decision roles, not causal effects.',ha='left',va='bottom',fontsize=11.5,color=fs.PALETTE['muted'])
 for a,sa,oa,b,sb,ob in edges:fs.arrow(ax,port(geo[a],sa,oa),port(geo[b],sb,ob),patchA=nodes[a],patchB=nodes[b])
 fig.canvas.draw();renderer=fig.canvas.get_renderer();checks=[]
 for key in nodes:
  rb=nodes[key].get_window_extent(renderer);tb=texts[key].get_window_extent(renderer);inside=bool(tb.x0>=rb.x0+2 and tb.x1<=rb.x1-2 and tb.y0>=rb.y0+2 and tb.y1<=rb.y1-2)
  checks.append({'node':key,'text_inside_box':inside,'font_pt':texts[key].get_fontsize(),'node_px':[float(rb.width),float(rb.height)],'text_px':[float(tb.width),float(tb.height)]})
 if not all(x['text_inside_box'] for x in checks):raise RuntimeError('Node clipping: '+str([x['node'] for x in checks if not x['text_inside_box']]))
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,11.5] if mobile else [10,6.5],'nodes':checks,'edges':[[x[0],x[3]] for x in edges],'mobile_font_px_at332':14*96/72*332/(4.8*96) if mobile else None}
def generate(overwrite=False):
 previous=json.loads(DEST.read_text()) if DEST.exists() else None
 targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
 if not overwrite and (DEST.exists() or any(x.exists() for x in targets)):raise SystemExit('Refuse overwrite; use --overwrite for an authorized recorded repair.')
 outputs=[];geometry=[]
 for mobile in [False,True]:
  files,ck=draw(mobile);outputs.extend(files);geometry.append(ck)
 assert [x['path'] for x in outputs]==[str(p.relative_to(ROOT)) for p in targets];assert geometry[0]['edges']==geometry[1]['edges']==[['purpose','evidence'],['evidence','choice'],['choice','report'],['report','action'],['rules','action']]
 h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs=[BASE/'figstyle.py',HERE]
 d={'id':FID,'step':'3.5','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','author':'JoonHo Lee (jlee296@ua.edu)','scope':'Original conceptual diagram from public chapter/contract; no numerical evidence,empirical data,policy rule or scientific calculation introduced.','command':'python -B assets/reproduction/figures/generators/F01/generate.py'+(' --overwrite' if overwrite else ''),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in inputs],'source_refs':[SOURCE_REF],'outputs':outputs,'geometry_checks':geometry,'actual_image_views':[],'execution':{'python':platform.python_version(),'renderer_invocations_total':1 if previous is None else previous['execution']['renderer_invocations_total']+1,'last_command_invocations':1,'last_command_layout_exports':2,'last_command_asset_exports':6,'scientific_calculations':0,'R_package_runs':0,'optimizer_runs':0,'canonical_edits':0,'register_edits':0},'semantic_notes':['Both layouts preserve the six contracted nodes and five dependency edges.','Reporting-choice/common-grade nodes are teal and directly labeled; institutional-use nodes are ochre and separately labeled. No meaning relies on color alone.','Institutional action has separate report and additional-rules/evidence inputs; a grade does not by itself allocate funding or a place.','Within-grade silence does not assert latent equality,eligibility equivalence or entitlement.'],'required_repairs_remaining':[],'limits':['Author asset views are recorded after actual inspection.','SVG glyph outlines require accessible caption/alt supplied by the contract; no causal or calibration claim.']}
 if previous:d['previous_execution_history']=previous.get('previous_execution_history',[])+[{'receipt_outputs':previous['outputs'],'execution':previous['execution'],'actual_image_views':previous.get('actual_image_views',[])}]
 DEST.parent.mkdir(exist_ok=True,parents=True);DEST.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'id':FID,'outputs':outputs,'geometry':'PASS','receipt':str(DEST.relative_to(ROOT))},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
