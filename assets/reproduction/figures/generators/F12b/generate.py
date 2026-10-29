"""F12b: exact known-criterion cycle and all thirteen coherent report risks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
from matplotlib.patches import Circle
C=fs.PALETTE;STEM='f12b-local-lower-bounds-and-attainable-common-grades'
DATA=FIGURES/'data/f12b-cyclic-conflict.json'


def checked_coordinates():
    d=json.loads(DATA.read_text());theta=d['law']['theta_unit_by_criterion']
    assert d['units']==['A','B','C'] and theta==[[3,1,2],[2,3,1],[1,2,3]]
    w=list(map(F,d['weights']));tau=F(d['tau']);assert w==[F(1,3)]*3 and tau==F(9,20) and d['M']==3
    errors={};error_checks=[]
    for row in d['ordered_pair_errors']:
        i,j=map(d['units'].index,[row['above'],row['below']])
        es=[F(int(theta[i][k]<=theta[j][k])) for k in range(3)]
        cost=sum(ww*e for ww,e in zip(w,es));assert es==list(map(F,row['criterion_errors'])) and cost==F(row['weighted_error'])
        errors[i,j]=cost;error_checks.append({'direction':row['above']+'>'+row['below'],'error':str(cost),'status':'PASS'})
    for edge in d['preferred_cycle']:
        i,j=map(d['units'].index,[edge['above'],edge['below']])
        support=[k+1 for k in range(3) if theta[i][k]>theta[j][k]]
        assert support==edge['supporting_criteria'] and errors[i,j]==F(1,3)
        assert sum(w[k-1] for k in support)==F(edge['support_weight'])==F(2,3)
    expected={g for g in product(range(1,4),repeat=3) if set(g)==set(range(1,max(g)+1))}
    assert {tuple(r['g']) for r in d['all_actions']}==expected and len(expected)==13
    groups=Counter();action_checks=[]
    for row in d['all_actions']:
        g=row['g'];ds=[(i,j) for i in range(3) for j in range(3) if g[i]<g[j]]
        wrong=sum(errors[i,j] for i,j in ds);hold=tau*(3-len(ds));risk=(wrong+hold)/3
        assert len(ds)==row['N'] and max(g)==row['G'] and wrong==F(row['weighted_expected_wrong'])
        assert hold==F(row['withholding_cost_unnormalized']) and risk==F(row['risk'])
        groups[max(g),risk]+=1
        action_checks.append({'g':g,'N':len(ds),'weighted_wrong':str(wrong),'withholding_count_cost':str(hold),'risk':str(risk),'status':'PASS'})
    assert groups==Counter({(1,F(9,20)):1,(2,F(29,60)):6,(3,F(4,9)):3,(3,F(5,9)):3})
    assert groups==Counter({(r['G'],F(r['risk'])):r['action_count'] for r in d['risk_groups']})
    risks=[(r['g'],F(r['risk'])) for r in d['all_actions']]
    assert min(r for _,r in risks)==F(4,9)
    assert {tuple(g) for g,r in risks if r==F(4,9)}=={(1,2,3),(2,3,1),(3,1,2)}
    cap2=[(g,r) for g,r in risks if max(g)<=2]
    assert min(r for _,r in cap2)==F(9,20) and [g for g,r in cap2 if r==F(9,20)]==[[1,1,1]]
    local=sum(min(errors[i,j],errors[j,i],tau) for i,j in [(0,1),(0,2),(1,2)])/3
    assert local==F(1,3) and all(r>local for _,r in risks)
    assert F(9,20)-F(4,9)==F(1,180) and F(4,9)-local==F(1,9)
    return d,{'directed_error_checks':error_checks,'action_risk_checks':action_checks,
              'complete_canonical_action_count':len(expected),'group_counts':[{'G':g,'risk':str(r),'reports':c} for (g,r),c in groups.items()],
              'local_bound':str(local),'minimum':'4/9','all_minimizers':[[1,2,3],[2,3,1],[3,1,2]],
              'at_most_two_unique_minimizer':[1,1,1],'at_most_two_risk':'9/20','exactly_two_risk':'29/60',
              'improvement':'1/180','coherence_gap':'1/9','status':'PASS'}


def cycle_panel(ax,d,mobile=False):
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    ax.text(.02,.985,'(a) Known criteria produce a cycle',ha='left',va='top',fontsize=13 if mobile else 13.5,fontweight='bold')
    for k,order in enumerate(d['criterion_orders']):
        ax.text(.50,.89-k*.075,'Criterion '+str(k+1)+':  '+' > '.join(order),ha='center',va='center',fontsize=12.2)
    centers={'A':(.50,.60),'B':(.84,.23),'C':(.16,.23)};nodes={}
    for unit,(x,y) in centers.items():
        p=Circle((x,y),.065,facecolor='white',edgecolor=C['teal'],lw=1.7,zorder=3);ax.add_patch(p);nodes[unit]=p
        ax.text(x,y,unit,ha='center',va='center',fontsize=15,fontweight='bold',zorder=4)
    labelpos={('A','B'):(.815,.445),('B','C'):(.50,.105),('C','A'):(.185,.445)}
    edges=[]
    for row in d['preferred_cycle']:
        u,v=row['above'],row['below'];fs.arrow(ax,centers[u],centers[v],patchA=nodes[u],patchB=nodes[v],color=C['teal'])
        x,y=labelpos[u,v];ax.text(x,y,'Support '+row['support_weight']+'\nError '+row['directional_error'],ha='center',va='center',fontsize=11 if mobile else 11.2,linespacing=1.3,bbox={'facecolor':'white','edgecolor':'none','pad':1.5},zorder=5)
        edges.append({'above':u,'below':v,'support':row['support_weight'],'weighted_error':row['directional_error']})
    return {'criterion_orders':d['criterion_orders'],'cycle_edges':edges,'node_count':3,'arrow_count':3,
            'interpretation':'Two-of-three known criterion support; point-mass law, not a scalar posterior-majority assertion.'}


def risk_panel(ax,d,mobile=False):
    ax.set(xlim=(.55,3.75),ylim=(0,2/3))
    ax.set_xticks([1,2,3],['1','2','3']);ax.set_yticks([0,1/3,2/3],['0','1/3','2/3'])
    ax.set_xlabel(r'Occupied grades $G(g)$',labelpad=9,fontsize=12 if mobile else 12)
    ax.set_ylabel('Normalized risk',labelpad=9,fontsize=12.5)
    ax.set_title('(b) All 13 coherent reports',loc='left',pad=18,fontsize=13 if mobile else 13.5,fontweight='bold')
    fs.clean(ax)
    lb=float(F(d['summary']['pairwise_relaxation_lower_bound']))
    ax.axhline(lb,color=C['ink'],lw=1.3,linestyle=(0,(5,3)),zorder=1)
    ax.text(.67,lb-.035,'Pairwise bound 1/3\nUnattained',ha='left',va='top',fontsize=11.3 if mobile else 11.5,linespacing=1.3)
    marks=[]
    for row in d['risk_groups']:
        g=row['G'];r=F(row['risk']);n=row['action_count']
        optimum=(g==3 and r==F(4,9));allhold=(g==1)
        color=C['teal'] if optimum else C['ochre'] if allhold else C['muted']
        marker='^' if optimum else 's' if allhold else 'o'
        ax.scatter([g],[float(r)],s=95 if mobile else 88,marker=marker,
                   facecolor=color if optimum or allhold else 'white',edgecolor=color,lw=1.7,zorder=4)
        label=row['risk']+'\n'+str(n)+(' report' if n==1 else ' reports')
        if optimum:
            ax.annotate(label,xy=(g,float(r)),xytext=(10,-2),textcoords='offset points',ha='left',va='center',fontsize=11.8 if mobile else 12,color=C['ink'],linespacing=1.3)
        else:
            ax.annotate(label,xy=(g,float(r)),xytext=(0,13),textcoords='offset points',ha='center',va='bottom',fontsize=11.8 if mobile else 12,color=C['ink'],linespacing=1.3)
        marks.append({'G':g,'risk':row['risk'],'report_count':n,'marker':marker,'is_unrestricted_optimal_group':optimum})
    return {'risk_marks':marks,'total_action_multiplicity':sum(r['report_count'] for r in marks),
            'x_axis':'Occupied grade count; categorical, not available cap','risk_limits':['0','2/3'],
            'lower_bound':'1/3','lower_bound_attained':False,'lines_between_risk_groups':0}


def cap_cards(fig,mobile=False):
    if mobile:
        ax=fs.diagram_axis(fig,[.06,.168,.88,.078])
        fs.box(ax,.02,.02,.96,.96,'At most 2 grades\nUnique optimum: all-withhold\nRisk 9/20',fc='white',ec=C['ochre'],size=12.4)
        ax=fs.diagram_axis(fig,[.06,.058,.88,.094])
        fs.box(ax,.02,.02,.96,.96,'At most 3 grades\nThree co-optimal strict reports: ABC, BCA, CAB\nRisk 4/9; improvement 1/180\n(orders are listed from highest to lowest)',fc='white',ec=C['teal'],size=11.5)
    else:
        ax=fs.diagram_axis(fig,[.05,.10,.90,.135])
        fs.box(ax,.015,.025,.455,.95,'At most 2 grades\nUnique optimum: all-withhold\nRisk 9/20',fc='white',ec=C['ochre'],size=12.5)
        fs.box(ax,.53,.025,.455,.95,'At most 3 grades\nThree co-optimal strict orders: ABC, BCA, CAB\nRisk 4/9; improvement 1/180',fc='white',ec=C['teal'],size=12)


def draw(d,mobile=False):
    if mobile:
        fig=fs.canvas(4.8,16.4,True)
        fig.text(.06,.985,'Local bounds and\nattainable common grades',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.06,.937,'Known criteria; w = (1/3, 1/3, 1/3).\n'+r'$\tau=9/20$, $M=3$'+'. No latent criterion ties.',ha='left',va='top',fontsize=11.7,linespacing=1.3)
        cyc=cycle_panel(fig.add_axes([.06,.61,.88,.285]),d,True)
        risk=risk_panel(fig.add_axes([.18,.30,.73,.245]),d,True)
        cap_cards(fig,True)
        fig.text(.06,.033,'Exactly two grades: risk 29/60 for all six reports.\nAll-withhold is excluded.',ha='left',va='top',fontsize=11.2,linespacing=1.3)
    else:
        fig=fs.canvas(10.8,9.2,False)
        fig.text(.055,.965,'Local preferences and attainable common grades',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.055,.91,'Known criterion conflict: '+r'$w=(1/3,1/3,1/3)$, $\tau=9/20$, $M=3$'+'. No latent criterion ties.',ha='left',va='top',fontsize=12.2)
        cyc=cycle_panel(fig.add_axes([.05,.315,.43,.50]),d)
        risk=risk_panel(fig.add_axes([.56,.34,.39,.45]),d)
        cap_cards(fig)
        fig.text(.055,.057,'Exactly two grades excludes all-withhold: all six reports have risk 29/60.',ha='left',va='top',fontsize=11.7)
        fig.text(.055,.022,'Dots group equal risks; their report multiplicities sum to 13. Orders are listed from highest to lowest.',ha='left',va='top',fontsize=11.2,color=C['muted'])
    return fig,{'cycle':cyc,'risk':risk}


def generate(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F12b.json';prior=json.loads(dest.read_text()) if dest.exists() else None
    paths=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in paths)):raise SystemExit('Existing F12b outputs: --overwrite is for an authorized observed repair.')
    d,checks=checked_coordinates();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    attempt={'started_at_utc':now,'status':'running','command':'python3 -B assets/reproduction/figures/generators/F12b/generate.py'+(' --overwrite' if overwrite else '')}
    record={'id':'F12b','fig_label':'fig-vis-f12b','step':'4.15','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,
            'status':'rendering','actual_render_invocations':(prior or {}).get('actual_render_invocations',0)+1,
            'execution_history':(prior or {}).get('execution_history',[])+[attempt],
            'actual_PNG_views':(prior or {}).get('actual_PNG_views',0),'views':(prior or {}).get('views',[]),'repairs':(prior or {}).get('repairs',[]),
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,FIGURES/'figstyle.py',DATA]],
            'coordinate_selector':'Only the public ALLTIE-C extraction f12b-cyclic-conflict.json. No private scientific plotting input.',
            'fresh_exact_checks':checks,'scope':'Small exact arithmetic and finite 27-vector canonical-set completeness check; no original scientific program, solver, simulation, R package or empirical model run.',
            
            'publication_and_licenses':'Deferred'}
    if prior:record['previous_export_history']=prior.get('previous_export_history',[])+[{'created_at_utc':prior['created_at_utc'],'inputs':prior['inputs'],'outputs':prior.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(record,indent=2)+'\n')
    try:
        outputs=[];semantics=[]
        for mobile in [False,True]:
            fig,s=draw(d,mobile);semantics.append(s);outputs.extend(fs.export(fig,STEM,mobile))
        assert semantics[0]==semantics[1]
        record['outputs']=outputs;record['displayed_semantics']=semantics[0]
        record['status']='rendered';attempt.update({'status':'succeeded','output_count':6,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    except Exception as exc:
        attempt.update({'status':'failed','error':str(exc)});record['status']='render_failed';dest.write_text(json.dumps(record,indent=2)+'\n');raise
    dest.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
