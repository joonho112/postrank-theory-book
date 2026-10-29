#!/usr/bin/env python3
"""Exact stipulated profile guard, original pair multiplicities and theorem scope."""
from pathlib import Path
import sys,json,hashlib,datetime
from fractions import Fraction as F
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
STEM='f11c-a-full-profile-guard-retains-original-multiplicities';DATA=BASE/'data/full-profile-guard.json';D=json.loads(DATA.read_text())
assert D['weights']==['1/4','3/4'] and D['full_active_profile_classes']==[['A','B'],['C'],['D']]
assert sum(D['original_pair_multiplicities'].values())==D['original_M']==6
assert sum(F(x['weighted_distinct_delta']) for x in D['pairs'])==F(7,2)
for s in D['states']:assert s['targets'][0]==s['targets'][1] and s['targets'][0][1]==s['targets'][2][1] and s['targets'][0][0]!=s['targets'][2][0]

def matrix(ax,mobile):
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');f=14 if mobile else 13
 ax.text(.01,.98,'Complete profiles\nunder the stipulated law' if mobile else 'Complete profiles under the stipulated law',va='top',fontsize=f+1,weight='bold')
 ax.text(.34,.84,'State 1\nmass 3/5' if mobile else 'State 1: mass 3/5',ha='center',va='center',fontsize=f)
 ax.text(.76,.84,'State 2\nmass 2/5' if mobile else 'State 2: mass 2/5',ha='center',va='center',fontsize=f)
 xs=[.25,.44,.67,.86]
 for x,k in zip(xs,[1,2,1,2]):ax.text(x,.75,f'Criterion {k}' if not mobile else f'Crit. {k}',ha='center',fontsize=f-1)
 for i,u in enumerate(D['units']):
  y=.63-i*.145;ax.text(.04,y,u,fontsize=f+1,weight='bold',va='center')
  for j,x in enumerate(xs):
   state=j//2;k=j%2;v=D['states'][state]['targets'][i][k]
   fs.box(ax,x-.078,y-.053,.156,.106,str(v),size=f+1,fc=fs.PALETTE['light'] if i<2 else 'white',ec=fs.PALETTE['teal'] if i<2 else fs.PALETTE['line'])
 ax.text(.01,.05,'A and B: full active-profile match.\nA and C: criterion 2 only; no required guard.',fontsize=f-1,va='bottom',linespacing=1.2)

def graph(ax,mobile):
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');f=14 if mobile else 12.8
 ax.text(.5,.98,'Retain the original pair frame',ha='center',va='top',fontsize=f+1,weight='bold')
 fs.box(ax,.10,.60,.80,.29,'',ec=fs.PALETTE['teal'],fc=fs.PALETTE['light'])
 ax.text(.5,.855,'Guard class H',ha='center',va='center',fontsize=f)
 for x,u in [(.29,'A'),(.71,'B')]:fs.box(ax,x-.065,.69,.13,.085,u,size=f+1,fc='white',ec=fs.PALETTE['teal'])
 ax.plot([.37,.63],[.73,.73],color=fs.PALETTE['muted'],ls='--',lw=1)
 ax.text(.5,.625,'AB: 1 pair, distinct mass 0',ha='center',va='center',fontsize=f-1)
 for x,u in [(.20,'C'),(.80,'D')]:fs.box(ax,x-.065,.17,.13,.10,u,size=f+1,fc='white')
 for x1,x2 in [(.24,.20),(.76,.80)]:
  for offset in [-.012,.012]:ax.plot([x1+offset,x2+offset],[.585,.29],color=fs.PALETTE['teal'],lw=1.3)
 ax.text(.04,.43,'AC, BC\n2 pairs',fontsize=f-1,ha='left',va='center')
 ax.text(.96,.43,'AD, BD\n2 pairs',fontsize=f-1,ha='right',va='center')
 ax.plot([.28,.72],[.22,.22],color=fs.PALETTE['muted'],lw=1.3)
 ax.text(.5,.13,'CD: 1 pair',ha='center',fontsize=f-1)
 ax.text(.5,.01,'1 + 2 + 2 + 1 = 6 original pairs',ha='center',fontsize=f,weight='semibold')

def draw(mobile):
 fig=fs.canvas(4.8 if mobile else 11.8,15.6 if mobile else 8.5,mobile)
 if mobile:
  fig.text(.04,.985,'A full-profile guard\nkeeps the original comparisons',va='top',fontsize=16,weight='bold')
  fig.text(.04,.927,'Both criteria active: w = (1/4, 3/4)',fontsize=13.5)
  matrix(fig.add_axes([.04,.55,.92,.34]),True);graph(fig.add_axes([.08,.18,.84,.31]),True)
  footer='Guard: gA = gB; other ties remain permissible.\nPreserves existence of a weighted\nneutral-risk minimizer in the full\nat-most-G family, without extra restrictions.\nOriginal M = 6; no unweighted collapse.\nThis is not an arbitrary merging rule.'
  fig.text(.04,.015,footer,fontsize=13.3,va='bottom',linespacing=1.25,color=fs.PALETTE['muted'])
 else:
  fig.text(.035,.97,'A full-profile guard keeps the original comparisons',va='top',fontsize=18,weight='bold')
  fig.text(.035,.89,'Complete two-state law; both criteria active with w = (1/4, 3/4)',fontsize=13)
  matrix(fig.add_axes([.035,.25,.52,.59]),False);graph(fig.add_axes([.61,.24,.35,.60]),False)
  footer='Guard: gA = gB; other reported ties remain permissible.\nPreserves existence of a weighted neutral-risk minimizer in the full at-most-G family.\nNo extra restrictions; original M = 6. This is not an arbitrary merging rule.'
  fig.text(.035,.045,footer,fontsize=12.4,va='bottom',linespacing=1.4,color=fs.PALETTE['muted'])
 fig.canvas.draw();ren=fig.canvas.get_renderer();checks=[]
 for t in fig.findobj(match=lambda x:isinstance(x,fs.plt.Text)):
  if not t.get_text():continue
  bb=t.get_window_extent(ren);inside=bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height;checks.append(bool(inside))
 if not all(checks):
  bad=[t.get_text() for t in fig.findobj(match=lambda x:isinstance(x,fs.plt.Text)) if t.get_text() and (t.get_window_extent(ren).x0<0 or t.get_window_extent(ren).y0<0 or t.get_window_extent(ren).x1>fig.bbox.width or t.get_window_extent(ren).y1>fig.bbox.height)]
  raise RuntimeError('Text outside canvas: '+str(bad))
 return fs.export(fig,STEM,mobile),{'mobile':mobile,'all_text_canvas_checks':len(checks),'all_inside':True}
files=[];geometry=[]
for mobile in [False,True]:
 f,g=draw(mobile);files+=f;geometry.append(g)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
fs.record('F11c',files,[{'path':str(p.relative_to(fs.ROOT)),'sha256':sha(p)} for p in [Path(__file__),DATA,BASE/'figstyle.py']],['Complete stipulated law, not estimated/sample equality.','Original units and pair counts retained; no optimizer or class-collapse computation.'])
p=fs.ROOT/'evidence/figures/builds/F11c.json';b=json.loads(p.read_text());b.update(author='JoonHo Lee (jlee296@ua.edu)',created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),geometry_checks=geometry,execution={'renderer_invocations_current_command':1,'production_invocations_total':1,'exports':6,'model_runs':0,'optimizer_runs':0},actual_image_views=[]);p.write_text(json.dumps(b,indent=2)+'\n');print('F11c six exports; exact source assertions and canvas checks PASS')
