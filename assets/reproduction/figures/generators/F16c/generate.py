"""Original F16c: frozen T11 pair masks and normalized affine risk curves.

Renders the accepted seven-report coordinate table without a package, model fit,
optimizer or execution of the original exact-check program.
"""
from pathlib import Path
from fractions import Fraction as F
import csv,sys,json,hashlib,datetime,argparse
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
from pair_panel import draw_panel
import numpy as np
ACTIONS=FIGURES/'data/t11-actions.csv';PAIRS=FIGURES/'data/t11-pairs.csv'
C=fs.PALETTE
IDS=['T11_2211','T11_2221'];TAU_SWITCH=F(1,5)

def coordinates_and_checks():
    rows=list(csv.DictReader(ACTIONS.open()));byid={r['action_id']:r for r in rows}
    assert len(rows)==7
    for aid,intercept,slope in [('T11_2211',F(0),F(1,6)),('T11_2221',F(1,60),F(1,12))]:
        r=byid[aid];assert F(r['risk_intercept'])==intercept and F(r['risk_tau_slope'])==slope
        assert F(r['MR_intercept'])/6==intercept and F(r['MR_tau_slope'])/6==slope
    def risk(r,t):return F(r['risk_intercept'])+F(r['risk_tau_slope'])*t
    crosses={F(0),F(1,2)}
    for i,a in enumerate(rows):
        for b in rows[i+1:]:
            delta=F(a['risk_tau_slope'])-F(b['risk_tau_slope'])
            if delta:
                t=(F(b['risk_intercept'])-F(a['risk_intercept']))/delta
                if 0<t<=F(1,2):crosses.add(t)
    ends=sorted(crosses);test=sorted(({t for t in ends if t>0}|{(l+r)/2 for l,r in zip(ends,ends[1:])})|{F(1,10),F(3,10)})
    checks=[]
    for t in test:
        values={r['action_id']:risk(r,t) for r in rows};best=min(values.values());active={aid for aid,value in values.items() if value==best}
        expected={IDS[0]} if t<TAU_SWITCH else {IDS[1]} if t>TAU_SWITCH else set(IDS)
        assert active==expected,(t,active,expected)
        checks.append({'tau':str(t),'active_reports':sorted(active),'minimum_normalized_risk':str(best)})
    assert risk(byid[IDS[0]],F(1,10))==F(1,60)
    assert risk(byid[IDS[1]],F(3,10))==F(1,24)
    assert risk(byid[IDS[0]],TAU_SWITCH)==risk(byid[IDS[1]],TAU_SWITCH)==F(1,30)
    assert max(F(r['distinct_disclosed_Q']) for r in rows)==3<F(rows[0]['total_distinct_T'])==F(7,2)
    return rows,byid,checks,[str(t) for t in ends]

def draw_risk_panel(ax,mobile=False):
    rows,byid,checks,crosses=coordinates_and_checks()
    x=np.linspace(0,.5,501)
    styles=[(IDS[0],C['teal'],'-','o','CD > AB'),(IDS[1],C['ochre'],'--','^','D > ABC')]
    for aid,color,line,marker,label in styles:
        r=byid[aid];intercept=float(F(r['risk_intercept']));slope=float(F(r['risk_tau_slope']))
        y=intercept+slope*x
        ax.plot(x,y,color=color,linestyle=line,linewidth=1.25,alpha=.78,label=label+(':  '+r'$R=\tau/6$' if aid==IDS[0] else ':  '+r'$R=1/60+\tau/12$'),zorder=2)
        active=(x<=.2) if aid==IDS[0] else (x>=.2)
        ax.plot(x[active],y[active],color=color,linestyle=line,linewidth=3,zorder=3)
        # Zero is only a displayed limit, outside the primary penalty domain.
        ax.plot([0],[intercept],marker=marker,markersize=6,markerfacecolor='white',markeredgecolor=color,linestyle='none',clip_on=False,zorder=5)
    ax.set(xlim=(0,.5),ylim=(0,.087),xlabel=r'Withholding penalty $\tau$',ylabel=r'Normalized risk $R_{\rm TA}$')
    ax.set_xticks([0,.1,.2,.3,.4,.5],['0*','1/10','1/5','3/10','2/5','1/2'])
    ax.set_yticks([0,.02,.04,.06,.08]);ax.yaxis.set_major_formatter(fs.plt.FormatStrFormatter('%.2f'))
    fs.clean(ax,'y')
    # Distinct symbols identify the highlighted reports independently of color.
    ax.scatter([.1],[1/60],s=72,marker='o',facecolor='white',edgecolor=C['teal'],linewidth=1.8,zorder=6)
    ax.scatter([.3],[1/24],s=86,marker='^',facecolor='white',edgecolor=C['ochre'],linewidth=1.8,zorder=6)
    ax.scatter([.2],[1/30],s=56,marker='D',facecolor='white',edgecolor=C['ink'],linewidth=1.6,zorder=7)
    note_style=dict(arrowprops=dict(arrowstyle='-',linewidth=.9,color=C['muted']),fontsize=12.5 if mobile else 11.5,ha='left',va='top',linespacing=1.3,bbox=dict(facecolor='white',edgecolor='none',pad=2))
    ax.annotate(r'$\tau=1/10$'+'\n'+r'$R=1/60$',xy=(.1,1/60),xytext=(.025,.066),**note_style)
    ax.annotate(r'$\tau=3/10$'+'\n'+r'$R=1/24$',xy=(.3,1/24),xytext=(.30,.084),**note_style)
    ax.annotate(r'$\tau=1/5$'+'\nBoth reports optimal',xy=(.2,1/30),xytext=(.235,.020),**note_style)
    ax.legend(loc='lower left',bbox_to_anchor=(-.01,1.02 if mobile else 1.005),ncol=1 if mobile else 2,frameon=False,handlelength=2.5,fontsize=12 if mobile else 11.5,columnspacing=2.0)
    return {'displayed_report_ids':IDS,'risk_curves':{aid:{'intercept':byid[aid]['risk_intercept'],'slope':byid[aid]['risk_tau_slope']} for aid in IDS},'seven_report_lower_envelope_checks':checks,'all_affine_intersection_endpoints':crosses,'tau_domain':'0<tau<=1/2;0shownonlyasopen-markerlimit','switch':{'tau':'1/5','risk':'1/30','both_report_ids':IDS},'Qmax':'3','total_distinct_T':'7/2','risk_axis':'Normalized by M=6; not unnormalized MR.'}

def generate(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F16c.json'
    previous=json.loads(dest.read_text()) if dest.exists() else None
    existing=[ROOT/'assets/figures'/('tie-aware-distinct-disclosure'+suffix+'.'+ext) for suffix in ['', '-mobile'] for ext in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in existing)):
        raise SystemExit('Existing F16c outputs: use --overwrite only for an authorized observed repair; prior receipts must be retained.')
    outputs=[];semantic=[]
    for mobile in [False,True]:
        if mobile:
            fig=fs.canvas(4.8,14.6,True)
            pair_ax=fig.add_axes([.025,.505,.95,.485]);draw_panel(pair_ax,True,title='(a) Count the same six pairs')
            fig.text(.06,.485,'(b) Risk under the same family',fontsize=14,fontweight='bold',ha='left',va='top')
            fig.text(.06,.460,'Thick segments give minimum risk\namong all seven guarded reports.',fontsize=12.5,ha='left',va='top',linespacing=1.3)
            risk_ax=fig.add_axes([.16,.115,.79,.265]);semantic.append(draw_risk_panel(risk_ax,True))
            fig.text(.06,.047,'* Zero is shown only as a limit.\nFixed law, weights and at-most-two-grade\nfamily; its maximum Q is 3, below T = 7/2.',fontsize=11.5,ha='left',va='top',linespacing=1.3)
        else:
            fig=fs.canvas(10,10,False)
            pair_ax=fig.add_axes([.025,.535,.95,.44]);draw_panel(pair_ax,False,title='(a) Count the same six original pairs')
            fig.text(.065,.505,'(b) Normalized risk under the same guarded at-most-two-grade family',fontsize=14,fontweight='bold',ha='left',va='top')
            fig.text(.065,.469,'Thick segments give minimum risk among all seven reports; only the two active candidates are drawn.',fontsize=11.5,ha='left',va='top')
            risk_ax=fig.add_axes([.095,.12,.86,.30]);semantic.append(draw_risk_panel(risk_ax,False))
            fig.text(.095,.025,'* Zero is shown only as a limit.  The family has maximum Q = 3 < T = 7/2.',fontsize=11.5,color=C['muted'],ha='left',va='bottom')
        outputs.extend(fs.export(fig,'tie-aware-distinct-disclosure',mobile))
    assert semantic[0]==semantic[1]
    inputs=[ACTIONS,PAIRS,FIGURES/'figstyle.py',HERE,HERE.with_name('pair_panel.py')]
    # Private audit metadata is optional, never a scientific input to regeneration.
    contract=ROOT/'evidence/figures/contracts/F16c.json'
    if contract.exists(): inputs.append(contract)
    receipt={'step':'2.9','id':'F16c','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'rendered','command':'python3 assets/reproduction/figures/generators/F16c/generate.py'+(' --overwrite' if overwrite else ''),'scope':'Final wide/narrow static assets from accepted CSVs, plus exact affine-coordinate envelope checks; no R analysis package, model fit, optimizer, or original finite-check main-program run.','inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs],'outputs':outputs,'risk_semantics':semantic[0],'pair_panel_reuse':'pair_panel.draw_panel supplies unchanged6pairmasses/two masks and N/Q with retainedABzero tile.','encoding':'CD>AB solidteal/circle; D>ABC dashedochre/triangle. Thicksegments are activecosts. Diamond marks the switch where bothcomplete reports minimize risk.','views':[],'limits':['Only two risk curves are displayed, but the lower envelope was checked against every stored affine report at every intersection/midpoint and the highlightedpenalties.','No deterministic action is interpolated between report labels. Both reports are optimal at1/5.','At-most2family hasQmax3<T7/2; nofullclass-strictendpoint is claimed.','Allvalues are stipulated expectations under onefixedlaw, notempirical calibration orscalability results.'],'required_repairs_remaining':[]}
    if previous:
        for key in ['views','repairs','personal_visual_readback_at_utc','actual_PNG_image_views','final_retained_PNG_images_personally_viewed','view_limits','unique_affine_check_locations_per_layout','render_semantic_scope','render_tools']:
            if key in previous:receipt[key]=previous[key]
        receipt['actual_render_invocations']=previous.get('actual_render_invocations',1)+1
        receipt['render_history']=previous.get('render_history',[{'stage':'previous_exports','invocations':previous.get('actual_render_invocations',1),'receipt_outputs':previous['outputs'],'views_preserved':True}])+[{'stage':'authorized_overwrite','at_utc':receipt['created_at_utc'],'invocations':1,'command':receipt['command']}]
        receipt['status']='authorized_reexport'
    else:receipt['actual_render_invocations']=1
    dest.parent.mkdir(exist_ok=True,parents=True);dest.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs,'affine_check_points':len(semantic[0]['seven_report_lower_envelope_checks'])},indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--overwrite',action='store_true',help='Authorized observed repair only; preserve previous receipt and view history.')
    generate(parser.parse_args().overwrite)
