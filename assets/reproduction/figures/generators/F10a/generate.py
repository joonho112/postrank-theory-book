"""F10a: exact isolated-pair cost lines; public frozen coordinates only."""
from pathlib import Path
from fractions import Fraction as F
import argparse, datetime, hashlib, json, sys

HERE = Path(__file__).resolve()
FIGURES = HERE.parents[2]
ROOT = FIGURES.parents[2]
sys.path.insert(0, str(FIGURES))
import figstyle as fs
from matplotlib.patches import Rectangle

C = fs.PALETTE
STEM = 'f10a-the-isolated-pair-decision'
DATA = FIGURES / 'data/scalar-and-common-grade.json'


def checked_coordinates():
    d = json.loads(DATA.read_text())['isolated_pair']
    tau = F(d['tau'])
    assert tau == F(1, 5)
    assert d['cost_functions'] == {'first_above': 'e', 'reverse': '1-e', 'withhold': 'tau'}
    checks = []
    for row in d['coordinates']:
        e = F(row['forward_error'])
        costs = {'first_above': e, 'reverse': 1-e, 'withhold': tau}
        for action, key in [('first_above', 'cost_first_above'), ('reverse', 'cost_reverse'), ('withhold', 'cost_withhold')]:
            assert costs[action] == F(row[key])
        assert 1-e == F(row['forward_superiority'])
        minimum = min(costs.values())
        opts = [a for a, v in costs.items() if v == minimum]
        assert minimum == F(row['minimum_cost'])
        assert set(opts) == set(row['minimizing_actions'])
        checks.append({'e': str(e), 'costs': {k: str(v) for k,v in costs.items()},
                       'minimum': str(minimum), 'full_minimizing_set': opts, 'status': 'PASS'})
    for row in d['parameter_map']:
        t, lam = F(row['tau']), F(row['lambda'])
        assert t/(1-t) == lam and lam/(1+lam) == t
    assert tau/(1-tau) == F(1,4)
    assert {F(r['forward_error']) for r in d['coordinates']} >= {F(0), tau, F(1,2), 1-tau, F(1)}
    assert (F(1,2), 1-F(1,2), F(1,2)) == (F(1,2),)*3
    return d, checks


def costs_panel(ax, data, mobile=False):
    # Exact affine functions need only endpoint coordinates; thresholds are included.
    rows = data['coordinates']; t = float(F(data['tau']))
    x = [float(F(row['forward_error'])) for row in rows]
    ax.plot(x, [float(F(row['cost_first_above'])) for row in rows], color=C['teal'], lw=1.8, linestyle='-', zorder=2)
    ax.plot(x, [float(F(row['cost_reverse'])) for row in rows], color=C['rust'], lw=1.8, linestyle=(0,(5,3)), zorder=2)
    ax.plot(x, [float(F(row['cost_withhold'])) for row in rows], color=C['ochre'], lw=1.8, linestyle=(0,(1,2)), zorder=2)
    # Thicker segments preserve each action's style while identifying the lower envelope.
    ax.plot([0,t], [0,t], color=C['teal'], lw=4.2, solid_capstyle='round', zorder=3)
    ax.plot([t,1-t], [t,t], color=C['ochre'], lw=4.2, linestyle=(0,(1,2)), zorder=3)
    ax.plot([1-t,1], [t,0], color=C['rust'], lw=4.2, linestyle=(0,(5,3)), zorder=3)
    for e in [t,1-t]:
        ax.vlines(e, 0, t, color=C['gray'], lw=1, linestyle=(0,(2,3)), zorder=1)
        ax.scatter([e],[t],s=75 if mobile else 65,marker='o',facecolor='white',edgecolor=C['ink'],lw=1.5,zorder=5)
    ax.set(xlim=(0,1), ylim=(0,1))
    ticks = [0,.2,.5,.8,1]
    labels = ['0','1/5','1/2','4/5','1']
    ax.set_xticks(ticks, labels)
    ax.set_yticks([0,.2,.5,1], ['0','1/5','1/2','1'])
    ax.set_ylabel('Expected cost per pair', labelpad=10)
    ax.set_xlabel(r'Forward error $e=B(\theta_i\leq\theta_j)$', labelpad=10, fontsize=12.5 if mobile else 12)
    fs.clean(ax)
    label_size = 12 if mobile else 12.5
    ax.text(.58,.68,r'$i$ above $j$: $e$',color=C['teal'],fontsize=label_size,rotation=39 if mobile else 26,ha='left',va='bottom')
    ax.text(.035,.88,r'$j$ above $i$: $1-e$',color=C['rust'],fontsize=label_size,rotation=-39 if mobile else -26,ha='left',va='top')
    ax.text(.5,.27,r'Withhold: $\tau=1/5$',color=C['ochre'],fontsize=label_size,ha='center',va='bottom',bbox={'facecolor':'white','edgecolor':'none','pad':1.5})
    return {'x_limits':[0,1], 'y_limits':[0,1], 'tau':'1/5',
            'crossings':['1/5','4/5'], 'cost_lines':['e','1-e','tau'],
            'crossing_minimizers':[['first_above','withhold'],['reverse','withhold']],
            'lower_envelope':'min(e,1-e,tau)', 'normalization':'Cost per unordered pair, M=1'}


def region_strip(fig):
    ax=fig.add_axes([.095,.23,.565,.085]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    for start,width,label,color in [(0,.2,'$i$ above $j$\n$e<1/5$',C['teal']),(.2,.6,'Withhold\n$1/5<e<4/5$',C['ochre']),(.8,.2,'$j$ above $i$\n$e>4/5$',C['rust'])]:
        ax.add_patch(Rectangle((start,0),width,1,facecolor=C['light'],edgecolor=color,lw=1))
        ax.text(start+width/2,.5,label,ha='center',va='center',fontsize=11.5,linespacing=1.25)


def parameter_box(fig, rect, mobile=False):
    ax=fs.diagram_axis(fig,rect)
    if mobile:
        text='Normalized source parameter\n'+r'$\lambda=\tau/(1-\tau),\quad\tau=\lambda/(1+\lambda)$'+'\n'+r'$\tau=1/5\quad\Longleftrightarrow\quad\lambda=1/4$'
    else:
        text='Normalized source\nparameter\n\n'+r'$\tau=\lambda/(1+\lambda)$'+'\n'+r'$\lambda=\tau/(1-\tau)$'+'\n\n'+r'$\tau=1/5\quad\Longleftrightarrow\quad\lambda=1/4$'
    fs.box(ax,.025,.025,.95,.95,text,size=12.5 if mobile else 12.2)


def endpoint_box(fig,rect,mobile=False):
    ax=fs.diagram_axis(fig,rect)
    text=('Endpoint '+r'$\tau=1/2$'+('\nAt '+r'$e=1/2$'+':' if not mobile else ', '+r'$e=1/2$'+':')+'\n'+r'$e=1-e=\tau=1/2$'+'\nAll three actions minimize.')
    fs.box(ax,.025,.025,.95,.95,text,size=12.5 if mobile else 12.2)


def draw(data, mobile=False):
    if mobile:
        fig=fs.canvas(4.8,12.4,True)
        fig.text(.06,.985,'The isolated-pair decision',ha='left',va='top',fontsize=16,fontweight='bold')
        fig.text(.06,.943,'One scalar pair; no latent ties.\nCost per unordered pair (M = 1).',ha='left',va='top',fontsize=12.5,linespacing=1.3)
        semantic=costs_panel(fig.add_axes([.18,.61,.77,.255]),data,True)
        fig.text(.18,.535,'Thick segments: minimum cost',ha='left',va='top',fontsize=11.5,color=C['muted'])
        fig.text(.08,.492,'Unique minimizing action',ha='left',va='top',fontsize=13,fontweight='bold')
        for y,text in [(.463,r'$e<1/5$:  $i$ above $j$'),(.435,r'$1/5<e<4/5$:  withhold'),(.407,r'$e>4/5$:  $j$ above $i$')]:
            fig.text(.10,y,text,ha='left',va='top',fontsize=12.5)
        fig.text(.08,.362,'At e = 1/5: i above j and withhold.\nAt e = 4/5: j above i and withhold.',ha='left',va='top',fontsize=12,linespacing=1.4)
        parameter_box(fig,[.06,.183,.88,.12],True)
        endpoint_box(fig,[.06,.068,.88,.095],True)
        fig.text(.06,.034,'Local thresholds do not bind every pair\nin a coherent common grade.',ha='left',va='top',fontsize=11.5,linespacing=1.3)
    else:
        fig=fs.canvas(10.4,7.8,False)
        fig.text(.06,.965,'The isolated-pair decision',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.06,.91,'One scalar pair; no latent ties.  Cost per unordered pair (M = 1).',ha='left',va='top',fontsize=12.5)
        semantic=costs_panel(fig.add_axes([.095,.445,.565,.395]),data,False)
        fig.text(.095,.345,'Thick segments: minimum cost',ha='left',va='top',fontsize=11.5,color=C['muted'])
        region_strip(fig)
        fig.text(.095,.20,'At e = 1/5: i above j and withhold.\nAt e = 4/5: j above i and withhold.',ha='left',va='top',fontsize=12,linespacing=1.4)
        parameter_box(fig,[.715,.56,.255,.285])
        endpoint_box(fig,[.715,.245,.255,.265])
        fig.text(.06,.087,'These are local pair decisions. Coherent common grades can require a different pair action.',ha='left',va='top',fontsize=12)
        fig.text(.06,.04,'Withholding is a report action; it does not assert equal latent targets.',ha='left',va='top',fontsize=11.5,color=C['muted'])
    return fig, semantic


def generate(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F10a.json'
    prior=json.loads(dest.read_text()) if dest.exists() else None
    paths=[ROOT/'assets/figures'/(STEM+suffix+'.'+ext) for suffix in ['', '-mobile'] for ext in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in paths)):
        raise SystemExit('Existing F10a outputs: --overwrite is for an authorized observed repair.')
    data,checks=checked_coordinates()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    attempt={'started_at_utc':now,'command':'python3 -B assets/reproduction/figures/generators/F10a/generate.py'+(' --overwrite' if overwrite else ''),'status':'running'}
    attempts=(prior or {}).get('execution_history',[])+[attempt]
    record={'id':'F10a','fig_label':'fig-vis-f10a','step':'4.9','created_at_utc':now,
            'author':'JoonHo Lee (jlee296@ua.edu)','status':'rendering','execution_history':attempts,
            'actual_render_invocations':(prior or {}).get('actual_render_invocations',0)+1,
            'actual_PNG_views':(prior or {}).get('actual_PNG_views',0),'views':(prior or {}).get('views',[]),
            'repairs':(prior or {}).get('repairs',[]),
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,FIGURES/'figstyle.py',DATA]],
            'coordinate_selector':'Only isolated_pair from the public JSON. Affine cost lines evaluated at exact endpoint/threshold values; no private scientific plotting input.',
            'exact_coordinate_checks':checks,'exact_coordinate_rows_checked':len(checks),
            'parameter_checks':data['parameter_map'],'endpoint_check':'tau=e=1/2 makes e=1-e=tau=1/2; all three minimize.',
            'scope':'Original deterministic analytic figure. No simulation, fitted model, posterior draws, solver, package or original example main-program execution.',
            
            'publication_and_licenses':'Deferred'}
    if prior:
        record['previous_export_history']=prior.get('previous_export_history',[])+[{'created_at_utc':prior['created_at_utc'],'outputs':prior.get('outputs',[])}]
        for key in ['personal_view_limits']:
            if key in prior:record[key]=prior[key]
    dest.parent.mkdir(exist_ok=True,parents=True)
    dest.write_text(json.dumps(record,indent=2)+'\n')
    try:
        outputs=[];semantics=[]
        for mobile in [False,True]:
            fig,semantic=draw(data,mobile);semantics.append(semantic)
            outputs.extend(fs.export(fig,STEM,mobile))
        assert semantics[0]==semantics[1]
        record['outputs']=outputs;record['displayed_semantics']=semantics[0]
        record['status']='rendered'
        attempt['status']='succeeded';attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        attempt['output_count']=len(outputs)
    except Exception as exc:
        attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed'
        dest.write_text(json.dumps(record,indent=2)+'\n');raise
    dest.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs,'actual_render_invocations':record['actual_render_invocations']},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--overwrite',action='store_true')
    generate(parser.parse_args().overwrite)
