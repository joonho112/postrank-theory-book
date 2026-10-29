#!/usr/bin/env python3
"""Original analytical-dependency diagram, with separate desktop/mobile layouts.
Run from any directory using an existing Python environment with Matplotlib.
No scientific target values, empirical data, random draws or optimizer are used.
"""
from pathlib import Path
import sys, json, hashlib, datetime, platform, argparse
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT
STEM='information-beliefs-laws'
parser=argparse.ArgumentParser();parser.add_argument('--overwrite',action='store_true');args=parser.parse_args()
for suffix in ['', '-mobile']:
 for ext in ['svg','pdf','png']:
  p=ROOT/'assets/figures'/f'{STEM}{suffix}.{ext}'
  if p.exists() and not args.overwrite:raise SystemExit('Refuse overwrite; use --overwrite only for a recorded repair.')
LABELS={
 'Y':'Declared\ninformation $Y=y$',
 'M':'Producer model\nand computation',
 'B':'Selection beliefs\n$\\Pi_s(\\cdot\\mid y)$',
 'V':'Targets, loss\nand constraints',
 'G':'Selected feasible\ngrade action $g$',
 'T':'Target state\n$\\Theta$',
 'L':'Realized loss\n$L(g,\\Theta)$',
 'P':'Declared\nevaluation law $\\nu$',
 'R':'Conditional risk\n$R^{\\nu}(g\\mid y)$',
}
GEOMETRY={
 False:{'Y':(.02,.71,.20,.13),'M':(.02,.38,.20,.15),'B':(.29,.60,.23,.17),'V':(.29,.21,.23,.18),'G':(.56,.47,.18,.18),'T':(.80,.73,.18,.13),'L':(.80,.47,.18,.18),'P':(.55,.15,.18,.18),'R':(.80,.15,.18,.18)},
 True:{'Y':(.05,.84,.41,.095),'M':(.54,.84,.41,.095),'B':(.23,.665,.54,.105),'V':(.05,.48,.41,.12),'G':(.54,.48,.41,.12),'T':(.05,.285,.41,.12),'L':(.54,.285,.41,.12),'P':(.05,.09,.41,.12),'R':(.54,.09,.41,.12)},
}
def anchor(rect,side,offset=.5):
 x,y,w,h=rect
 return {'left':(x,y+h*offset),'right':(x+w,y+h*offset),'top':(x+w*offset,y+h),'bottom':(x+w*offset,y)}[side]
def one(mobile=False):
 fig=fs.canvas(width=4.8 if mobile else 10,height=10.8 if mobile else 6,mobile=mobile)
 ax=fs.diagram_axis(fig,rect=(.025,.045,.95,.89) if mobile else (.02,.07,.96,.83))
 geo=GEOMETRY[mobile];nodes={};texts={};minfont=14 if mobile else 12
 for key,rect in geo.items():
  ec=fs.PALETTE['teal'] if key in ['B','G'] else fs.PALETTE['ochre'] if key in ['P','R'] else fs.PALETTE['line']
  fc=fs.PALETTE['light'] if key in ['B','G','L'] else fs.PALETTE['white']
  label=LABELS[key]
  if key=='P' and mobile:label='Declared\nevaluation law $\\nu$'
  size=minfont
  nodes[key]=fs.box(ax,*rect,label,fc=fc,ec=ec,size=size,weight='semibold' if key in ['B','G','R'] else 'normal')
  texts[key]=ax.texts[-1]
 if mobile:
  edges=[('Y','bottom',.7,'B','top',.28),('M','bottom',.3,'B','top',.72),('B','bottom',.72,'G','top',.5),('V','right',.5,'G','left',.5),('G','bottom',.5,'L','top',.5),('T','right',.5,'L','left',.5),('L','bottom',.5,'R','top',.5)]
 else:
  edges=[('Y','right',.5,'B','left',.72),('M','right',.5,'B','left',.27),('B','right',.5,'G','left',.68),('V','right',.5,'G','left',.30),('G','right',.5,'L','left',.5),('T','bottom',.5,'L','top',.5),('L','bottom',.5,'R','top',.5)]
 def connect(a,sa,oa,b,sb,ob,dashed=False):
  # Clip against the actual padded rounded patches, keeping arrowheads visible.
  ar=fs.FancyArrowPatch(anchor(geo[a],sa,oa),anchor(geo[b],sb,ob),patchA=nodes[a],patchB=nodes[b],shrinkA=2,shrinkB=3,arrowstyle='-|>',mutation_scale=13,linewidth=1.3,color=fs.PALETTE['ochre'] if dashed else fs.PALETTE['muted'],linestyle=(0,(3,2)) if dashed else '-',zorder=4)
  ax.add_patch(ar)
 for edge in edges:connect(*edge)
 connect('P','right',.5,'R','left',.5,dashed=True)
 if mobile:
  fig.text(.04,.985,'From information to grades\nand evaluated risk',ha='left',va='top',fontsize=15.5,weight='semibold')
  fig.text(.04,.025,'Analytical dependencies;\nno causal interpretation.\nDashed arrow: declared law\nused to average loss.',ha='left',va='bottom',fontsize=14,linespacing=1.15,color=fs.PALETTE['muted'])
 else:
  fig.text(.025,.97,'From information to a report and its evaluated risk',ha='left',va='top',fontsize=16,weight='semibold')
  fig.text(.025,.025,'Arrows are analytical dependencies. The dashed arrow specifies the law used to average realized loss.',ha='left',va='bottom',fontsize=11,color=fs.PALETTE['muted'])
 fig.canvas.draw();renderer=fig.canvas.get_renderer();checks=[]
 for key in nodes:
  rb=nodes[key].get_window_extent(renderer);tb=texts[key].get_window_extent(renderer)
  inside=bool(tb.x0>=rb.x0+2 and tb.x1<=rb.x1-2 and tb.y0>=rb.y0+2 and tb.y1<=rb.y1-2)
  checks.append({'node':key,'text_inside_node':inside,'font_pt':texts[key].get_fontsize(),'text_box_px':[round(tb.width,3),round(tb.height,3)],'node_box_px':[round(rb.width,3),round(rb.height,3)]})
 if not all(x['text_inside_node'] for x in checks):raise RuntimeError('Text clipping: '+str([x for x in checks if not x['text_inside_node']]))
 files=fs.export(fig,STEM,mobile=mobile)
 return files,{'layout':'mobile' if mobile else 'desktop','canvas_inches':[4.8,10.8] if mobile else [10,6],'node_checks':checks,'minimum_node_font_pt':minfont,'minimum_footer_font_pt':14 if mobile else 11,'mobile_display_font_estimate_px_at_332':14*96/72*332/(4.8*96) if mobile else None,'checks_scope':'Text bounding boxes within nodes; arrow placement and final presentation are not tested by this check.'}
files=[];checks=[]
for mobile in [False,True]:
 out,ck=one(mobile);files+=out;checks.append(ck)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
fs.record('F09c',files,inputs=[{'path':'assets/reproduction/figures/figstyle.py','sha256':sha(BASE/'figstyle.py')}],notes=['Original redraw of existing analytical-dependency diagram, explicitly separating realized loss and conditional averaging.','No causal arrows, numerical fixture, simulation, package run, optimizer or empirical study.','Desktop and narrow layouts are distinct deterministic geometries.','Rendering does not edit the chapter source or verify interpretation in context.'])
p=ROOT/'evidence/figures/builds/F09c.json';d=json.loads(p.read_text());d.update(source_refs=['chapters/09-targets-actions-laws.qmd (controlling text; not a runtime input)'],created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),author='JoonHo Lee (jlee296@ua.edu)',generator={'path':str(Path(__file__).relative_to(ROOT)),'sha256':sha(Path(__file__))},execution={'python':platform.python_version(),'renderer_invocations':1,'layout_exports':2,'plots_or_diagrams_generated':2,'scientific_calculations':0,'package_runs':0,'optimizer_runs':0},geometry_checks=checks,actual_image_views=[]);p.write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({'id':'F09c','outputs':files,'node_geometry_checks':'PASS','build_record':str(p.relative_to(ROOT))},indent=2))
