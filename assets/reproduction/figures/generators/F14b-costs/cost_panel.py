"""Reusable F14b interval-saving and prefix-state drawing functions.

Only public data and public figstyle supply scientific inputs. The final F14b
assembly can import this module directly; private staged graphics are optional
review outputs, never inputs to the assembled figure.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle
C=fs.PALETTE;DATA=BASE/'data/fixed-order-dp.json'
PATH_STATES={(0,0),(1,1),(2,3),(3,4)}
PATH_INTERVALS={(0,1),(1,3),(3,4)}


def load_checked_data():
    d=json.loads(DATA.read_text());units=d['units_and_fixed_order']
    assert units==['A','B','C','D'] and d['n']==4 and d['M']==6
    assert list(map(F,d['weights']))==[F(3,5),F(2,5)] and F(d['tau'])==F(1,4)
    w=list(map(F,d['weights']));tau=F(d['tau']);eta={};checks=[]
    states=[(r['theta_unit_by_criterion'],F(r['probability'])) for r in d['joint_belief']]
    assert sum(p for _,p in states)==1
    for row in d['pair_costs']:
        i,j=map(units.index,[row['above'],row['below']])
        es=[sum(p for theta,p in states if theta[i][k]<=theta[j][k]) for k in range(2)]
        assert es==list(map(F,row['criterion_errors']))
        e=sum(ww*v for ww,v in zip(w,es));v=e-tau
        assert e==F(row['weighted_error']) and v==F(row['eta_error_minus_tau'])
        eta[i+1,j+1]=v
    W={}
    for row in d['block_savings']:
        a,b=row['a']-1,row['b'];v=sum((v for (i,j),v in eta.items() if a<i<j<=b),F(0))
        assert v==F(row['W']) and -v==F(row['merge_risk_adjustment_unnormalized'])
        W[a,b]=v;checks.append({'object':'W','a':a,'b':b,'value':str(v),'status':'PASS'})
    assert len(W)==10 and sum(eta.values())==F(-9,20)
    states={(r['h'],r['r']):r for r in d['dp_states']};assert len(states)==25
    for (h,c),row in states.items():
        value=row['maximum_saving']
        if h==0 and c==0:assert value=='0'
        elif h==0 or h>c:assert value is None
        else:
            candidate={b:F(states[h-1,b]['maximum_saving'])+W[b,c] for b in range(h-1,c) if states[h-1,b]['maximum_saving'] is not None}
            best=max(candidate.values());assert F(value)==best
            assert row['optimal_predecessor_endpoints']==[b for b,v in candidate.items() if v==best]
        checks.append({'object':'V','h':h,'c':c,'value':value,'status':'PASS'})
    assert [states[h,c]['maximum_saving'] for h,c in [(0,0),(1,1),(2,3),(3,4)]]==['0','0','3/20','3/20']
    return d,checks


def _label(value):
    if value is None:return r'$-\infty$'
    q=F(value)
    return ('+' if q>0 else '')+str(q).replace('-','−')


def _cell(ax,x,y,value,selected=False,invalid_interval=False,size=13):
    infeasible=value is None and not invalid_interval
    v=F(value) if value is not None else None
    face=C['light'] if v is not None and v>0 else '#FBF4F1' if v is not None and v<0 else 'white'
    patch=Rectangle((x-.5,y-.5),1,1,facecolor=face,edgecolor=C['teal'] if selected else C['line'],
                    lw=2.4 if selected else .8,hatch='///' if invalid_interval else None,zorder=2 if selected else 1)
    ax.add_patch(patch)
    text='—' if invalid_interval else _label(value)
    t=ax.text(x,y,text,ha='center',va='center',fontsize=size,fontweight='bold' if selected else 'normal',
              color=C['muted'] if invalid_interval or infeasible else C['rust'] if v<0 else C['ink'],zorder=3)
    return patch,t


def _geometry(ax,objects):
    ax.figure.canvas.draw();ren=ax.figure.canvas.get_renderer();checks=[]
    for key,p,t in objects:
        pb=p.get_window_extent(ren);tb=t.get_window_extent(ren)
        inside=bool(tb.x0>pb.x0+2 and tb.x1<pb.x1-2 and tb.y0>pb.y0+2 and tb.y1<pb.y1-2)
        ab=ax.get_window_extent(ren)
        patch_inside=bool(pb.x0>ab.x0+2 and pb.x1<ab.x1-2 and pb.y0>ab.y0+2 and pb.y1<ab.y1-2)
        checks.append({'cell':key,'text':t.get_text(),'inside_cell':inside,'whole_patch_inside_axes':patch_inside,'font_pt':t.get_fontsize()})
    assert all(row['inside_cell'] for row in checks),'Cell label clipping'
    assert all(row['whole_patch_inside_axes'] for row in checks),'Cell border clipping'
    return checks


def draw_cost_triangle(ax,d,mobile=False,title=r'(a) Signed interval savings $W(a,b)$'):
    bycut={(r['a']-1,r['b']):r['W'] for r in d['block_savings']};objects=[];values=[]
    for a in range(4):
        for b in range(1,5):
            valid=a<b;v=bycut.get((a,b));selected=(a,b) in PATH_INTERVALS
            p,t=_cell(ax,b,3-a,v,selected,not valid,14 if mobile else 13)
            objects.append((str((a,b)),p,t))
            if valid:values.append({'a':a,'b':b,'interval':d['units_and_fixed_order'][a:b],'W':v,'selected':selected})
    ax.set(xlim=(.45,4.55),ylim=(-.55,3.55),aspect='equal')
    ax.set_xticks([1,2,3,4]);ax.set_yticks([3,2,1,0],['0','1','2','3'])
    ax.set_xlabel(r'Right cut boundary $b$',labelpad=9,fontsize=13 if mobile else 12)
    ax.set_ylabel(r'Left cut boundary $a$',labelpad=9,fontsize=13 if mobile else 12)
    ax.tick_params(axis='both',length=0,pad=7,labelsize=13 if mobile else 12)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.set_title(title,loc='left',pad=16,fontsize=13.5 if mobile else 14,fontweight='bold')
    return {'panel':'interval_savings','values':values,'valid_intervals':10,'noninterval_cells':6,
            'indexing':'Displayed W(a,b) uses positions a+1 through b; public inclusive endpoints [a,b] map to W(a-1,b).',
            'units':'Unnormalized signed block savings, not normalized risk','geometry':_geometry(ax,objects)}


def draw_prefix_states(ax,d,mobile=False,title=r'(b) Prefix maximum savings $V_h(c)$'):
    states={(r['h'],r['r']):r for r in d['dp_states']};objects=[];values=[]
    for h in range(5):
        for c in range(5):
            v=states[h,c]['maximum_saving'];selected=(h,c) in PATH_STATES
            p,t=_cell(ax,c,4-h,v,selected,False,14 if mobile else 13)
            objects.append((str((h,c)),p,t));values.append({'h':h,'c':c,'V':v,'selected':selected})
    ax.set(xlim=(-.55,4.55),ylim=(-.55,4.55),aspect='equal')
    ax.set_xticks(range(5));ax.set_yticks([4,3,2,1,0],['0','1','2','3','4'])
    ax.set_xlabel(r'Prefix length $c$',labelpad=9,fontsize=13 if mobile else 12)
    ax.set_ylabel(r'Nonempty blocks $h$',labelpad=9,fontsize=13 if mobile else 12)
    ax.tick_params(axis='both',length=0,pad=7,labelsize=13 if mobile else 12)
    for spine in ax.spines.values():spine.set_visible(False)
    ax.set_title(title,loc='left',pad=16,fontsize=13.5 if mobile else 14,fontweight='bold')
    return {'panel':'prefix_states','values':values,'state_count':25,'finite_states':sum(r['V'] is not None for r in values),
            'infeasible_states':sum(r['V'] is None for r in values),'selected_states':[[0,0],[1,1],[2,3],[3,4]],
            'input_to_canonical_mapping':'JSON h is h; JSON r is canonical c. Null means -infinity.',
            'units':'Maximum unnormalized saving; never a prefix risk','geometry':_geometry(ax,objects)}
