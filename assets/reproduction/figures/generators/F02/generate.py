"""F02: three dated institutional decision pipelines; original conceptual figure.

All display labels are declared here. Only public source/style files are read;
no policy data, statistical program or private contract is a runtime input.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
C=fs.PALETTE
STEM='f02-three-institutional-decision-pipelines'
LANES=[
 {'case':'California','version':'2023 assistance eligibility','unit':'District, COE or charter; student-group patterns matter','nodes':['Indicator and\nstudent-group evidence','Priority-area\neligibility rules','Eligibility\nfor assistance'],'note':'Agency eligibility is a different decision from an indicator color.','source_anchor':'sec-california-case'},
 {'case':'Tennessee','version':'2017–18 evaluation; 2019 manual','unit':'Teacher','nodes':['Estimated growth\nand precision','Benchmark-based\nindex and category','Input to\nevaluation'],'note':'A benchmark category supplies evidence for evaluation, not the entire personnel rule.','source_anchor':'sec-educational-performance'},
 {'case':'Head Start','version':'Snapshot through 22 October 2026','unit':'Child considered within family circumstances','nodes':['Family\nevidence','Eligibility\nverification','Local selection criteria\n+ enrollment constraints','Waiting list /\navailable place'],'auxiliary':'Community assessment\ninforms local priorities','note':'Selection is needed when eligible applicants exceed available places.','source_anchor':'sec-head-start-access'}
]

def node(ax,x,y,w,h,label,mobile=False,emphasis=False):
 return fs.box(ax,x,y,w,h,label,fc=C['light'] if not emphasis else C['white'],ec=C['line'] if not emphasis else C['teal'],size=13 if mobile else 12,weight='normal')

def connect(ax,a,b,vertical=False,auxiliary=False):
 # Rectangle-center connectors clipped against their actual rounded patches.
 aa=a.get_bbox();bb=b.get_bbox();start=(aa.x0+aa.width/2,aa.y0+aa.height/2);end=(bb.x0+bb.width/2,bb.y0+bb.height/2)
 fs.arrow(ax,start,end,patchA=a,patchB=b,style='--' if auxiliary else '-',color=C['muted'])

def draw_wide_lane(ax,lane,index):
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
 ax.axhline(.985,color=C['line'],linewidth=.7)
 ax.text(.015,.94,f"({chr(97+index)}) {lane['case']}",ha='left',va='top',fontsize=14,fontweight='bold')
 ax.text(.985,.94,lane['version'],ha='right',va='top',fontsize=12,color=C['muted'])
 ax.text(.015,.78,'Unit: '+lane['unit'],ha='left',va='top',fontsize=11.5)
 if index<2:
  xs=[.04,.365,.69];w=.27;y=.34;hh=.255
  patches=[node(ax,x,y,w,hh,label,emphasis=(j==2)) for j,(x,label) in enumerate(zip(xs,lane['nodes']))]
  for a,b in zip(patches,patches[1:]):connect(ax,a,b)
  ax.text(.015,.12,lane['note'],ha='left',va='center',fontsize=11.5,color=C['muted'])
 else:
  xs=[.02,.275,.53,.785];w=.195;y=.25;hh=.25
  patches=[node(ax,x,y,w,hh,label,emphasis=(j==3)) for j,(x,label) in enumerate(zip(xs,lane['nodes']))]
  for a,b in zip(patches,patches[1:]):connect(ax,a,b)
  aux=node(ax,.50,.59,.27,.16,lane['auxiliary'])
  connect(ax,aux,patches[2],auxiliary=True)
  ax.text(.015,.08,lane['note'],ha='left',va='center',fontsize=11.5,color=C['muted'])

def draw_mobile_lane(ax,lane,index):
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');ax.axhline(.99,color=C['line'],linewidth=.7)
 ax.text(.025,.955,f"({chr(97+index)}) {lane['case']}",ha='left',va='top',fontsize=15,fontweight='bold')
 # Deliberate linebreaks preserve dates and native units on a narrow page.
 versions=['2023 assistance eligibility','2017–18 evaluation;\n2019 manual','Snapshot through\n22 October 2026']
 units=['District, COE or charter;\nstudent-group patterns matter','Teacher','Child considered within\nfamily circumstances']
 ax.text(.025,.875,versions[index],ha='left',va='top',fontsize=12.5,color=C['muted'],linespacing=1.25)
 ax.text(.025,.755 if index<2 else .76,'Unit: '+units[index],ha='left',va='top',fontsize=12.5,linespacing=1.25)
 if index<2:
  ys=[.53,.34,.15];x=.07;w=.86;hh=.125
  patches=[node(ax,x,y,w,hh,label,True,j==2) for j,(y,label) in enumerate(zip(ys,lane['nodes']))]
  for a,b in zip(patches,patches[1:]):connect(ax,a,b,True)
  notes=['Agency eligibility differs\nfrom an indicator color.','This category is one input\nto an evaluation.']
  ax.text(.025,.055,notes[index],ha='left',va='center',fontsize=11.5,color=C['muted'],linespacing=1.25)
 else:
  # Community evidence enters selection priorities, not individual eligibility.
  ys=[.56,.405,.25,.095];x=.035;w=.60;hh=.105
  labels=['Family evidence','Eligibility\nverification','Local priorities +\nenrollment constraints','Waiting list /\navailable place']
  patches=[node(ax,x,y,w,hh,label,True,j==3) for j,(y,label) in enumerate(zip(ys,labels))]
  for a,b in zip(patches,patches[1:]):connect(ax,a,b,True)
  aux=node(ax,.735,.25,.23,.105,'Community\nassessment',True)
  connect(ax,aux,patches[2],auxiliary=True)
  ax.text(.025,.025,'When eligible applicants\nexceed available places.',ha='left',va='center',fontsize=11.5,color=C['muted'],linespacing=1.25)

def generate(overwrite=False):
 dest=ROOT/'evidence/figures/builds/F02.json';previous=json.loads(dest.read_text()) if dest.exists() else None
 existing=[ROOT/'assets/figures'/(STEM+suffix+'.'+ext) for suffix in ['', '-mobile'] for ext in ['svg','pdf','png']]
 if not overwrite and (dest.exists() or any(p.exists() for p in existing)):raise SystemExit('Existing F02 outputs: --overwrite is only for an authorized observed repair.')
 outputs=[]
 for mobile in [False,True]:
  if mobile:
   fig=fs.canvas(4.8,17,True)
   fig.text(.055,.99,'Three distinct institutional decisions',ha='left',va='top',fontsize=15,fontweight='bold')
   rects=[(.025,.67,.95,.28),(.025,.355,.95,.30),(.025,.025,.95,.325)]
   for index,(lane,rect) in enumerate(zip(LANES,rects)):draw_mobile_lane(fig.add_axes(rect),lane,index)
  else:
   fig=fs.canvas(10.4,9,False)
   fig.text(.045,.985,'Three distinct institutional decisions',ha='left',va='top',fontsize=16,fontweight='bold')
   rects=[(.025,.66,.95,.285),(.025,.355,.95,.285),(.025,.035,.95,.30)]
   for index,(lane,rect) in enumerate(zip(LANES,rects)):draw_wide_lane(fig.add_axes(rect),lane,index)
  outputs.extend(fs.export(fig,STEM,mobile))
 inputs=[HERE,FIGURES/'figstyle.py']
 receipt={'id':'F02','step':'3.6','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','command':'python3 -B assets/reproduction/figures/generators/F02/generate.py'+(' --overwrite' if overwrite else ''),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs],'source_refs':['chapters/02-education-access.qmd','references.bib'],'outputs':outputs,'literal_public_lane_data':LANES,'source_scope':'Dated canonicalChapter2caseaccounts and acceptedcontract. No originalpolicydocument orcurrentlawreaudit; no numericalpolicythreshold,data or causalclaim added.','arrows':'Solid clipped connectors show the main descriptive workflow; dashed branch shows communityassessment entering localpriorities ratherthan childeligibility. No causal or commonposterioralgorithm interpretation.','actual_render_invocations':1,'actual_PNG_views':0,'views':[],'repairs':[],'publication_and_licenses':'Deferred','executions':{'model_fit':0,'R_analysis_package':0,'optimizer':0,'new_policy_data':0}}
 if previous:
  for key in ['views','repairs','actual_PNG_views','personal_view_limits']:
   if key in previous:receipt[key]=previous[key]
  receipt['actual_render_invocations']=previous.get('actual_render_invocations',1)+1
  receipt['previous_export_history']=previous.get('previous_export_history',[])+[{'created_at_utc':previous['created_at_utc'],'outputs':previous['outputs']}]
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--overwrite',action='store_true');generate(parser.parse_args().overwrite)
