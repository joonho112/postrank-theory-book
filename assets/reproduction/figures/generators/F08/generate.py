#!/usr/bin/env python3
"""Original symbolic count/law diagram; no numerical guarantee calculated."""
from pathlib import Path
import sys,json,hashlib,datetime
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
STEM='f08-the-denominator-and-law-determine-the-guarantee'
CARDS=[
 ('Realized state',r'$f(a,\Theta)$','One action and\none target state'),
 ('Posterior',r'$E[f(a(y),\Theta)\mid Y=y]$','Condition on the\nobserved data'),
 ('Joint model',r'$E_{\Theta,Y}[f(a(Y),\Theta)]$','Average parameters\nand data together'),
 ('Fixed parameter',r'$E_{Y\mid\theta}[f(a(Y),\theta)]$','Repeat data at\na fixed parameter'),
]
def draw(mobile):
 fig=fs.canvas(width=4.8 if mobile else 11.8,height=14.8 if mobile else 8.5,mobile=mobile)
 ax=fs.diagram_axis(fig,rect=(.04,.055,.92,.865) if mobile else (.025,.10,.95,.79));checks=[];tracked=[]
 def card(x,y,w,h,title,formula,note,size=13):
  b=fs.box(ax,x,y,w,h,'',fc=fs.PALETTE['light']);
  for yy,s,weight,fsz in [(y+h*.80,title,'bold',size),(y+h*.53,formula,'normal',size),(y+h*.24,note,'normal',size-1)]:
   t=ax.text(x+w/2,yy,s,ha='center',va='center',fontsize=fsz,weight=weight,linespacing=1.15);tracked.append((t,b))
  return b
 if mobile:
  card(.01,.82,.98,.17,'Testing convention',r'$f(a,\Theta)=F/\max\{1,R\}$','F: false claims; R: reported claims\nEmpty report: f = 0',14)
  card(.01,.64,.98,.15,'P1 displayed error rate',r'$D/N\quad\mathrm{only\ if}\ N>0$','N = 0: rate undefined\nShow disclosure separately',14)
  for i,(title,f,note) in enumerate(CARDS):
   y=.48-i*.135
   card(.01,y,.98,.12,title,f,note,14)
  fig.text(.04,.98,'Name the denominator\nand the averaging law',fontsize=17,weight='semibold',va='top')
  fig.text(.04,.015,'Correct conditional law + bound for all data\n(or almost surely) → joint-model bound.\nNo automatic fixed-parameter guarantee.',fontsize=12.8,color=fs.PALETTE['muted'],va='bottom',linespacing=1.2)
 else:
  card(.01,.68,.47,.29,'Testing convention',r'$f(a,\Theta)=F/\max\{1,R\}$','F: false claims; R: reported claims\nEmpty report: f = 0',14)
  card(.52,.68,.47,.29,'P1 displayed error rate',r'$D/N\quad\mathrm{only\ if}\ N>0$','N = 0: rate undefined\nShow disclosure separately',14)
  for i,(title,f,note) in enumerate(CARDS):card(.01+i*.25,.14,.23,.37,title,f,note,12.4)
  ax.text(.01,.57,'Which quantity is averaged, and under which law?',fontsize=14,weight='bold')
  fig.text(.025,.96,'Name the denominator and the averaging law',fontsize=18,weight='semibold',va='top')
  fig.text(.025,.05,'Correct conditional law + a bound for all data (or almost surely) → joint-model bound.\nThis does not supply a uniform fixed-parameter guarantee.',fontsize=12,color=fs.PALETTE['muted'],linespacing=1.4)
 # The integration statement is written explicitly rather than a cross-card
 # connector: no arrow can be mistaken for a frequentist implication.
 fig.canvas.draw();ren=fig.canvas.get_renderer()
 for t,b in tracked:
  tb=t.get_window_extent(ren);bb=b.get_window_extent(ren);checks.append(bool(tb.x0>=bb.x0 and tb.x1<=bb.x1 and tb.y0>=bb.y0 and tb.y1<=bb.y1))
 if not all(checks):raise RuntimeError('Text outside card '+str([i for i,c in enumerate(checks) if not c]))
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'text_containment_checks':len(checks),'all_inside':True}
files=[];geometry=[]
for mobile in [False,True]:
 f,g=draw(mobile);files+=f;geometry.append(g)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
fs.record('F08',files,[{'path':str(p.relative_to(fs.ROOT)),'sha256':sha(p)} for p in [Path(__file__),BASE/'figstyle.py']],['Symbolic law cards, not calculated probabilities or error control.','The conditional-to-joint implication is an explicit written statement with conditions; no cross-card arrow.','No invented numerical guarantee or posterior model.'])
p=fs.ROOT/'evidence/figures/builds/F08.json';d=json.loads(p.read_text());d.update(source_refs=['chapters/08-selection-abstention.qmd'],author='JoonHo Lee (jlee296@ua.edu)',created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),geometry_checks=geometry,execution={'renderer_invocations':1,'layouts':2,'exports':6,'scientific_calculations':0},actual_image_views=[]);p.write_text(json.dumps(d,indent=2)+'\n')
print('F08: six exports; text containment PASS')
