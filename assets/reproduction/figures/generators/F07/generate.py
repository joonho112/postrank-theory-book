#!/usr/bin/env python3
"""Original conceptual task map. No scientific data, probabilities or optimization.
Public reproduction: python -B assets/reproduction/figures/generators/F07/generate.py
"""
from pathlib import Path
import sys,json,hashlib,datetime,textwrap
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
STEM='f07-a-task-map-of-neighboring-methods'
ROWS=[
 ('Ranking aggregation','Supplied rankings','Consensus ranking\nor bucket order','Disagreement between\nsupplied relations'),
 ('SMAA-2','Criteria and a modeled\nspace of valuations','Rank-acceptability\nprofiles','Variation across modeled\ncriteria and valuations'),
 ('Preference sorting','Performances and\nclass judgments','Assignments to\npredefined classes','Unknown preference model;\nconsultation in one variant'),
 ('Multidomain posets','Known domain-specific\npartial orders','Simplified relation\nor ordered buckets','Uniform linear extensions\nof specified posets'),
 ('Comparative judgement','Assessor choices\nbetween items','Pair support and\nrank summaries','Uncertain assessor\npreference propensities'),
 ('Posterior grading','Beliefs about latent\ncriterion targets','One coherent\nordered grade report','Expected reporting loss\nunder a declared law'),
]
HEAD=['Task / method','Supplied input','Native output','Role of uncertainty / discrepancy']
def wrapped(s,width):return '\n'.join(textwrap.fill(l,width=width) for l in s.split('\n'))
def draw(mobile):
 fig=fs.canvas(width=4.8 if mobile else 12,height=19.2 if mobile else 8.2,mobile=mobile)
 ax=fs.diagram_axis(fig,rect=(.04,.035,.92,.88) if mobile else (.025,.09,.95,.79)); texts=[]
 if mobile:
  for i,row in enumerate(ROWS):
   top=1-i/6; h=.151
   rect=fs.box(ax,.0,top-h,.99,h,'',fc=fs.PALETTE['light'] if i%2==0 else 'white')
   t=ax.text(.04,top-.015,row[0],fontsize=15,weight='bold',va='top');texts.append((t,rect))
   for j,(label,s) in enumerate(zip(['Input','Output','Role'],row[1:])):
    yy=top-.045-j*.033
    t=ax.text(.04,yy,label.upper(),fontsize=11.8,color=fs.PALETTE['teal'],va='top',weight='semibold');texts.append((t,rect))
    t=ax.text(.35,yy,wrapped(s,26),fontsize=13.5,va='top',linespacing=1.1);texts.append((t,rect))
  fig.text(.04,.98,'Choose the comparator\nby the institutional task',va='top',fontsize=17,weight='semibold')
  fig.text(.04,.015,'Native tasks differ. No common objective,\nprobability law or action family is implied.',fontsize=12.5,color=fs.PALETTE['muted'],va='bottom')
 else:
  xs=[.02,.24,.48,.70];widths=[.2,.22,.2,.28]
  for x,h in zip(xs,HEAD):ax.text(x,.985,wrapped(h,28),fontsize=12,weight='bold',va='top')
  for i,row in enumerate(ROWS):
   top=.88-i*.145; rect=fs.box(ax,0,top-.12,.99,.12,'',fc=fs.PALETTE['light'] if i%2==0 else 'white')
   for j,(x,s) in enumerate(zip(xs,row)):
    t=ax.text(x,top-.06,s,fontsize=12,weight='semibold' if j==0 else 'normal',va='center',linespacing=1.25);texts.append((t,rect))
  fig.text(.025,.96,'Choose the comparator by the institutional task',fontsize=18,weight='semibold',va='top')
  fig.text(.025,.035,'Rows summarize distinct native tasks. Shared output labels do not imply the same target, objective, law or feasible family.',fontsize=11.5,color=fs.PALETTE['muted'])
 fig.canvas.draw();r=fig.canvas.get_renderer();checks=[]
 for t,b in texts:
  tb=t.get_window_extent(r);bb=b.get_window_extent(r)
  checks.append(bool(tb.x0>=bb.x0 and tb.x1<=bb.x1 and tb.y0>=bb.y0 and tb.y1<=bb.y1))
 if not all(checks):raise RuntimeError('Text outside row/card: '+str([i for i,c in enumerate(checks) if not c]))
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'text_containment_checks':len(checks),'all_inside':True}
files=[];geometry=[]
for mobile in [False,True]:
 f,g=draw(mobile);files+=f;geometry.append(g)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
fs.record('F07',files,[{'path':str(p.relative_to(fs.ROOT)),'sha256':sha(p)} for p in [Path(__file__),BASE/'figstyle.py']],['Original operational map; no ancestry, equivalence, dominance or exhaustive taxonomy claim.','No fitted model, scientific probabilities, optimizer or numerical analysis.'])
p=fs.ROOT/'evidence/figures/builds/F07.json';d=json.loads(p.read_text());d.update(source_refs=['chapters/07-aggregation-mcda.qmd'],author='JoonHo Lee (jlee296@ua.edu)',created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),geometry_checks=geometry,execution={'renderer_invocations':1,'layouts':2,'exports':6,'scientific_calculations':0},actual_image_views=[]);p.write_text(json.dumps(d,indent=2)+'\n')
print('F07: six exports; text containment PASS')
