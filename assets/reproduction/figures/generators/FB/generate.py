"""FB: event/law/denominator types and the inspected tie-aware API names."""
from pathlib import Path
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();BASE=HERE.parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;C=fs.PALETTE;STEM='fb-counts-laws-denominators-and-the-api-crosswalk'
PRED={
 'weak':r'$\sum_{i\ne j}x_{ij}\mathbf{1}\{\theta_{ik}\leq\theta_{jk}\}$',
 'strict':r'$\sum_{i\ne j}x_{ij}\mathbf{1}\{\theta_{ik}<\theta_{jk}\}$',
 'distinct':r'$\sum_{i\ne j}x_{ij}\mathbf{1}\{\theta_{ik}\ne\theta_{jk}\}$'}


def geometry(fig,objects):
    fig.canvas.draw();ren=fig.canvas.get_renderer();texts=list(fig.texts)
    for ax in fig.axes:texts+=list(ax.texts)
    texts=[t for t in texts if t.get_text()]
    for t in texts:
        b=t.get_window_extent(ren);assert b.x0>=1 and b.x1<=fig.bbox.width-1 and b.y0>=1 and b.y1<=fig.bbox.height-1,('outside canvas',t.get_text())
    for i,t in enumerate(texts):
        for u in texts[i+1:]:assert not t.get_window_extent(ren).overlaps(u.get_window_extent(ren)),('text overlap',t.get_text(),u.get_text())
    for p,t in objects:
        pb=p.get_window_extent(ren);b=t.get_window_extent(ren);assert b.x0>=pb.x0+1 and b.x1<=pb.x1-1 and b.y0>=pb.y0+1 and b.y1<=pb.y1-1,('card containment',t.get_text())
    return {'visible_text_records':len(texts),'card_containment_checks':len(objects),'canvas_and_text_nonoverlap':True,'numerical_coordinates':False}


def draw(mobile=False):
    objects=[];fig=fs.canvas(4.8 if mobile else 12.8,34.6 if mobile else 16,mobile)
    fig.text(.055 if mobile else .04,.983,'Counts, laws, denominators\nand API field names' if mobile else 'Counts, laws, denominators and API field names',ha='left',va='top',fontsize=16 if mobile else 18,fontweight='bold',linespacing=1.2)
    fig.text(.055 if mobile else .04,.946 if mobile else .94,'Fix report g and information y.\nChoose ν = s (supplied) or P (evaluation).\nWeights: nonnegative and sum to one.' if mobile else 'Fix report g, information y and normalized nonnegative weights. Choose ν = s (supplied) or P (evaluation).',ha='left',va='top',fontsize=14 if mobile else 13.5,linespacing=1.25)
    ax=fs.diagram_axis(fig,[.05,.085,.90,.80] if mobile else [.04,.23,.92,.64]);ax.set(xlim=(-.02,1.02),ylim=(-.015,1.015))
    def box(x,y,w,h,fc='white'):return fs.box(ax,x,y,w,h,'',fc=fc)
    def text(p,x,y,s,size=14,weight='normal',ha='left',va='center'):
        t=ax.text(x,y,s,ha=ha,va=va,fontsize=size,fontweight=weight,linespacing=1.2);objects.append((p,t));return t
    if mobile:
        p=box(0,.935,1,.05,C['light'])
        text(p,.035,.976,'Original report frame',weight='bold')
        text(p,.035,.961,r'$M=\binom{n}{2}>0,\quad x_{ij}=\mathbf{1}\{g_i<g_j\}$')
        text(p,.035,.943,r'$N(g)=\sum_{i\ne j}x_{ij};\quad\mathrm{raw\ disclosure}=N/M$')
        p=box(0,.770,1,.12)
        text(p,.035,.875,'Weak direction error (≤)',weight='bold')
        text(p,.035,.851,r'$D_k(g,\Theta)=$')
        text(p,.035,.831,PRED['weak'])
        text(p,.035,.812,'Average under ν at fixed y ↓')
        text(p,.035,.795,r'$E_k^\nu(g)=\mathbb{E}_\nu[D_k\mid y]$')
        text(p,.035,.779,r'$E_k^\nu(g)/N(g),\quad N(g)>0$')
        p=box(0,.585,1,.145)
        text(p,.035,.715,'Strict reversal (<)',weight='bold')
        text(p,.035,.691,PRED['strict'])
        text(p,.035,.668,'Average under ν at fixed y ↓')
        text(p,.035,.649,r'$E_k^{b,\nu}(g)$'+'  expected strict-error count')
        text(p,.035,.630,'Two rates; different denominators:')
        text(p,.035,.611,r'$E_k^{b,\nu}(g)/N(g),\quad N(g)>0$')
        text(p,.035,.594,r'$E_k^{b,\nu}(g)/Q_k^\nu(g),\quad Q_k^\nu(g)>0$')
        p=box(0,.425,1,.12)
        text(p,.035,.530,'Distinct opportunity (≠)',weight='bold')
        text(p,.035,.505,PRED['distinct'])
        text(p,.035,.486,'Average under ν at fixed y ↓')
        text(p,.035,.468,r'$Q_k^\nu(g)$'+'  expected distinct mass')
        text(p,.035,.451,'Weighted distinct disclosure:')
        text(p,.035,.434,r'$Q_w^\nu(g)/T_w^\nu,\quad T_w^\nu>0$')
        p=box(0,.285,1,.10,C['light'])
        text(p,.035,.370,'Weighting and total opportunity',weight='bold')
        text(p,.035,.349,r'$Q_w^\nu(g)=\sum_k w_kQ_k^\nu(g)$')
        text(p,.035,.330,r'$T_w^\nu=\sum_{i<j}\sum_k w_kd_{ij,k}^\nu$')
        text(p,.035,.313,r'$d_{ij,k}^\nu=\Pr_\nu(\theta_{ik}\ne\theta_{jk}\mid y)$')
        text(p,.035,.294,'T covers all original unordered pairs.')
        p=box(0,.175,1,.07,C['light'])
        text(p,.035,.230,'Inspected tie_aware_v1 field names',weight='bold')
        text(p,.035,.209,'API D ↔ '+r'$Q_w^s(g)$'+';  API T ↔ '+r'$T_w^s$')
        text(p,.035,.187,'Supplied-law aliases. Book '+r'$D_k$'+' retains its\nrealized weak wrong-count meaning.')
        p=box(0,.005,1,.13,C['light'])
        text(p,.035,.120,'Zero denominators stay undefined',weight='bold')
        notes=r'$N=0$: all disclosed counts are zero.'+'\n'+r'$N$-rates are NA; raw $N/M=0$.'+'\n'+r'$Q_w^\nu/T_w^\nu=0$ only if $T_w^\nu>0$.'+'\n'+r'$Q_k^\nu=0$: $E_k^{b,\nu}/Q_k^\nu$ is NA.'+'\n'+r'$T_w^\nu=0$: $Q_w^\nu/T_w^\nu$ is NA;'+'\n'+r'neutral risk and $R_0^\nu$ are zero.'+'\n'+r'Raw $N$ can still be positive outside'+'\n'+'a guard-restricted family.'
        text(p,.035,.101,notes,va='top')
        fig.text(.055,.069,'When whole reports or datasets vary,\nlet '+r'$A=\sum_k w_kD_k$'+'.\nE[A]/E[N] and E[A/N | N > 0]\nare generally different summaries.\nName the law and positive denominator.\nDifferent types can share numeric values.',ha='left',va='top',fontsize=14,linespacing=1.25)
    else:
        p=box(0,.93,1,.07,C['light'])
        text(p,.02,.965,'Raw report frame',weight='bold')
        text(p,.255,.986,r'$M=\binom{n}{2}>0,\quad x_{ij}=\mathbf{1}\{g_i<g_j\},\quad N(g)=\sum_{i\ne j}x_{ij}$')
        text(p,.255,.944,r'$N(g)/M$'+' is raw disclosure; it is fixed by g.')
        for x,h in [(.145,'Realized/action object'),(.515,'Conditional expectation'),(.855,'Rate and condition')]:ax.text(x,.895,h,ha='center',va='center',fontsize=14,fontweight='bold')
        for key,y,title in [('weak',.71,'Weak direction error (≤)'),('strict',.50,'Strict reversal (<)'),('distinct',.29,'Distinct opportunity (≠)')]:
            p=box(0,y,1,.16)
            text(p,.02,y+.141,title,weight='bold')
            if key=='weak':text(p,.145,y+.095,r'$D_k(g,\Theta)=$',ha='center')
            text(p,.145,y+(.044 if key=='weak' else .077),PRED[key],ha='center',size=13.5)
            fs.arrow(ax,(.30,y+.077),(.365,y+.077));text(p,.3325,y+.113,r'$\mathbb{E}_\nu[\cdot\mid y]$',size=12,ha='center')
            fs.arrow(ax,(.68,y+.077),(.74,y+.077));text(p,.710,y+.113,'weight; divide' if key=='distinct' else 'divide',size=12,ha='center')
            if key=='weak':
                text(p,.515,y+.077,r'$E_k^\nu(g)=\mathbb{E}_\nu[D_k\mid y]$',ha='center')
                text(p,.855,y+.077,r'$E_k^\nu(g)/N(g)$'+'\n'+r'$N(g)>0$',ha='center')
            elif key=='strict':
                text(p,.515,y+.090,r'$E_k^{b,\nu}(g)$',ha='center');text(p,.515,y+.047,'Expected strict-error count',ha='center',size=13)
                text(p,.855,y+.092,r'$E_k^{b,\nu}(g)/N(g),\ N(g)>0$',ha='center',size=13.5)
                text(p,.855,y+.035,r'$E_k^{b,\nu}(g)/Q_k^\nu(g),\ Q_k^\nu(g)>0$',ha='center',size=13.5)
            else:
                text(p,.515,y+.090,r'$Q_k^\nu(g)$',ha='center');text(p,.515,y+.047,'Expected distinct mass',ha='center',size=13)
                text(p,.855,y+.077,r'$Q_w^\nu(g)/T_w^\nu$'+'\n'+r'$T_w^\nu>0$',ha='center')
        p=box(0,.045,.62,.18,C['light'])
        text(p,.02,.200,'Weighting and total opportunity',weight='bold')
        text(p,.02,.162,r'$Q_w^\nu(g)=\sum_k w_kQ_k^\nu(g),\quad T_w^\nu=\sum_{i<j}\sum_k w_kd_{ij,k}^\nu$')
        text(p,.02,.116,r'$d_{ij,k}^\nu=\Pr_\nu(\theta_{ik}\ne\theta_{jk}\mid y)$')
        text(p,.02,.073,'T uses every original unordered pair; Q uses disclosed directions.',size=13)
        p=box(.675,.045,.325,.18,C['light'])
        text(p,.695,.194,'Inspected tie_aware_v1\nfield-name correspondence',weight='bold')
        text(p,.695,.133,'API D ↔ '+r'$Q_w^s(g)$'+';  API T ↔ '+r'$T_w^s$')
        text(p,.695,.080,'Supplied-law aliases; book '+r'$D_k$'+'\nremains a realized wrong-count.',size=13)
        za=fs.diagram_axis(fig,[.04,.11,.92,.105]);za.set(xlim=(-.02,1.02),ylim=(-.04,1.04))
        zero=[(r'$N=0$','All disclosed counts are zero.\n'+r'$N$-rates: NA; raw $N/M=0$.'+'\n'+r'$Q_w^\nu/T_w^\nu=0$ only if $T_w^\nu>0$.'),(r'$Q_k^\nu=0$',r'$E_k^{b,\nu}/Q_k^\nu$ is NA.'+'\nNo conditional-distinct accuracy\nis assigned.'),(r'$T_w^\nu=0$',r'$Q_w^\nu/T_w^\nu$ is NA; neutral risk'+'\n'+r'and $R_0^\nu$ are zero. Raw $N$ can be'+'\n'+'positive outside a guarded family.')]
        for x,(heading,body) in zip([0,.355,.710],zero):
            p=fs.box(za,x,0,.29,1,'',fc=C['light']);t=za.text(x+.015,.84,heading,ha='left',va='center',fontsize=14,fontweight='bold');u=za.text(x+.015,.39,body,ha='left',va='center',fontsize=13,linespacing=1.2);objects.extend([(p,t),(p,u)])
        fig.text(.04,.071,'When reports or datasets vary, let '+r'$A=\sum_k w_kD_k$'+'. E[A]/E[N] and E[A/N | N > 0] generally differ.\nName that averaging law and a positive denominator. Different types can have equal numerical values.',ha='left',va='top',fontsize=13.5,linespacing=1.3)
    return fig,{'semantic_rows':['realized weak error ≤','realized strict reversal <','realized distinct opportunity ≠'],'named_laws':['s supplied','P conditional evaluation'],'API_aliases':{'D':'Q_w^s(g)','T':'T_w^s'},'raw_count_is_fixed_by_report':True,'zero_T_does_not_force_zero_N_outside_guard':True,'expected_ratio_not_silently_ratio_of_expectations':True,'geometry':geometry(fig,objects)}


def main(overwrite=False):
    dest=ROOT/'evidence/figures/builds/FB.json';old=json.loads(dest.read_text()) if dest.exists() else None
    targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite only for an observed authorized repair.')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();a={'started_at_utc':now,'status':'running','command':'python -B assets/reproduction/figures/generators/FB/generate.py'+(' --overwrite' if overwrite else ''),'asset_writes':0,'layout_exports':0}
    r={'id':'FB','step':'7.10','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':(old or {}).get('execution_history',[])+[a],'views':(old or {}).get('views',[]),'actual_PNG_views':(old or {}).get('actual_PNG_views',0),'repairs':(old or {}).get('repairs',[]),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,BASE/'figstyle.py']],'scientific_inputs':'Literal symbolic formulas/labels and public shared style only; no numerical coordinates, canonical QMD, package or private scientific input. Optional old own receipt is audit history only.','scope':'Conceptual event/law/denominator map of canonical definitions and inspected tie-aware field names. No installed-library audit, package, optimizer, model, simulation or empirical execution.','publication_and_licenses':'Deferred'}
    if old:r['previous_export_history']=old.get('previous_export_history',[])+[{'created_at_utc':old['created_at_utc'],'inputs':old['inputs'],'outputs':old.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(r,indent=2)+'\n')
    try:
        outputs=[];layouts=[]
        for mobile in [False,True]:
            fig,layout=draw(mobile);layouts.append(layout);outputs+=fs.export(fig,STEM,mobile);r['outputs']=outputs;a['asset_writes']+=3;a['layout_exports']+=1
        r['layouts']=layouts;a['status']='succeeded';r['status']='rendered'
    except Exception as exc:a['status']='failed';a['error']=str(exc);r['status']='render_failed';raise
    finally:
        a['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':r['outputs']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
