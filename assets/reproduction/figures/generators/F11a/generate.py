"""F11a: one categorical selector selects a complete criterion vector."""
from pathlib import Path
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2];ROOT=FIGURES.parents[2]
sys.path.insert(0,str(FIGURES))
import figstyle as fs
from matplotlib.patches import Rectangle
C=fs.PALETTE;STEM='f11a-one-selector-chooses-one-whole-criterion-vector'


def matrix(ax,bounds,mobile=False):
    x,y,w,h=bounds
    outer=fs.box(ax,x,y,w,h,'',fc='white')
    cx=x+w*.61;cw=w*.20
    highlight=Rectangle((cx-cw/2,y+h*.07),cw,h*.84,facecolor=C['light'],edgecolor=C['teal'],lw=1.5,zorder=2)
    ax.add_patch(highlight)
    ax.text(x,y+h+.035,r'Supplied array $\Theta$',ha='left',va='bottom',fontsize=12.5)
    ax.text(cx,y+h*.83,r'$\kappa$',ha='center',va='center',fontsize=14,color=C['teal'])
    for xx in [x+w*.34,x+w*.88]:ax.text(xx,y+h*.83,r'$\cdots$',ha='center',va='center',fontsize=14)
    for r,(unit,entry) in enumerate([('1',r'$\theta_{1\kappa}$'),('2',r'$\theta_{2\kappa}$'),(r'$\vdots$',r'$\vdots$'),('n',r'$\theta_{n\kappa}$')]):
        yy=y+h*(.65-r*.17)
        ax.text(x+w*.14,yy,('Unit '+unit if r!=2 else unit),ha='center',va='center',fontsize=12 if mobile else 12.5)
        for xx in [x+w*.34,x+w*.88]:ax.text(xx,yy,r'$\cdots$',ha='center',va='center',fontsize=14)
        ax.text(cx,yy,entry,ha='center',va='center',fontsize=14,zorder=3)
    return outer,highlight,cx


def main_diagram(fig,mobile=False):
    ax=fs.diagram_axis(fig,[.04,.42,.92,.48] if mobile else [.05,.38,.90,.46])
    if mobile:
        arr,selected,cx=matrix(ax,(.07,.48,.86,.35),True)
        selector=fs.box(ax,.25,.91,.50,.07,r'$\kappa\sim\operatorname{Cat}(w)$',size=14)
        ax.text(.66,.88,r'$\kappa\perp\Theta\mid y$',ha='left',va='center',fontsize=11.5)
        vector=fs.box(ax,.36,.225,.28,.17,r'$\theta_{1\kappa}$'+'\n'+r'$\theta_{2\kappa}$'+'\n'+r'$\vdots$'+'\n'+r'$\theta_{n\kappa}$',fc='white',ec=C['teal'],size=13.5)
        ax.text(.06,.31,r'$Z=\Theta_{\cdot\kappa}$',ha='left',va='center',fontsize=14)
        g=fs.box(ax,.04,.035,.42,.10,'Same report '+r'$g$'+'\nfixed before '+r'$\kappa$',size=12)
        ev=fs.box(ax,.58,.035,.37,.10,'Evaluate\n'+r'$L_\tau(g,Z)$',size=13)
        arrow_defs=[('selector_to_column',(.50,.945),(cx,.48+.35*.91),selector,selected),
                    ('whole_column_to_Z',(.50,.65),(.50,.31),arr,vector),
                    ('fixed_g_to_loss',(.25,.085),(.765,.085),g,ev),
                    ('Z_to_loss',(.50,.31),(.765,.085),vector,ev)]
        ax.text(.68,.435,'Whole\ncolumn',ha='left',va='center',fontsize=11.5,linespacing=1.2)
    else:
        arr,selected,cx=matrix(ax,(.02,.225,.48,.53))
        selector=fs.box(ax,.18,.88,.29,.10,r'$\kappa\sim\operatorname{Cat}(w)$',size=14)
        ax.text(.51,.88,r'$\kappa\perp\Theta\mid y$',ha='left',va='center',fontsize=12)
        vector=fs.box(ax,.69,.23,.20,.50,r'$\theta_{1\kappa}$'+'\n'+r'$\theta_{2\kappa}$'+'\n'+r'$\vdots$'+'\n'+r'$\theta_{n\kappa}$',fc='white',ec=C['teal'],size=15)
        ax.text(.69,.775,r'$Z=\Theta_{\cdot\kappa}$',ha='left',va='bottom',fontsize=15)
        g=fs.box(ax,.04,.035,.36,.11,'Same predeclared report '+r'$g$'+'\nfixed before '+r'$\kappa$',size=12.5)
        ev=fs.box(ax,.63,.035,.32,.11,'Evaluate '+r'$L_\tau(g,Z)$',size=13.5)
        arrow_defs=[('selector_to_column',(.325,.93),(cx,.225+.53*.91),selector,selected),
                    ('whole_column_to_Z',(.26,.49),(.79,.49),arr,vector),
                    ('fixed_g_to_loss',(.22,.09),(.79,.09),g,ev),
                    ('Z_to_loss',(.79,.48),(.79,.09),vector,ev)]
        ax.text(.595,.62,'Copy the whole\nselected column',ha='center',va='center',fontsize=11.5,linespacing=1.3)
    for name,start,end,pa,pb in arrow_defs:fs.arrow(ax,start,end,patchA=pa,patchB=pb)
    return {'categorical_selector_count':1,'whole_column_output_count':1,'fixed_report_input_count':1,
            'main_patches':6,'directed_connectors':len(arrow_defs),
            'connector_roles':[a[0] for a in arrow_defs],'selected_entry_labels':['theta_1kappa','theta_2kappa','vdots','theta_nkappa'],
            'unit_order_preserved':True,'arrow_width_is_quantitative':False,
            'selector_independence':'kappa independent of Theta conditional on y; no within-array independence asserted'}


def identities(fig,mobile=False):
    if mobile:
        ax=fs.diagram_axis(fig,[.05,.265,.90,.13])
        text='Whole-vector law\n'+r'$B_w=\sum_k w_kB_k$'+'\nWeak-error mixture identity\n'+r'$E_{B_w}[L_\tau(g,Z)\mid y]=R^s_{w,\tau}(g\mid y)$'+'\nSame g and feasible family.\nLatent equality is allowed.'
        fs.box(ax,.02,.02,.96,.96,text,size=12.3)
        fig.text(.07,.247,'This mixes vector laws; no magnitude\naverage of the targets is constructed.',ha='left',va='top',fontsize=11.5,linespacing=1.3)
    else:
        ax=fs.diagram_axis(fig,[.06,.205,.88,.12])
        text='Whole-vector law:  '+r'$B_w=\sum_k w_kB_k$'+'\n'+r'$E_{B_w}[L_\tau(g,Z)\mid y]=R^s_{w,\tau}(g\mid y)$'+'\nSame g, same feasible family; latent equality is allowed.'
        fs.box(ax,.02,.02,.96,.96,text,size=13)
        fig.text(.06,.177,'This mixes vector laws; no magnitude average of the targets is constructed.',ha='left',va='top',fontsize=11.5)


def neutral_inset(fig,mobile=False):
    ax=fs.diagram_axis(fig,[.05,.025,.90,.19] if mobile else [.06,.02,.88,.12])
    if mobile:
        text=('Equality-neutral pair only\nFor one fixed pair:\n'
              'Condition on distinct targets\nin the selected criterion.\n'
              'With positive distinct mass,\n'+r'$c^s_{ij}/\delta^s_{ij}$'+' is the conditional error.\n'
              'Conditioning generally reweights\nwhich criterion is selected.\n'
              'At zero distinct mass:\nthe ratio is undefined;\n'
              'all three neutral pair costs are zero.')
    else:
        text='Equality-neutral pair only: selected-coordinate distinctness, '+r'$\delta^s_{ij}>0$'+'\n'+r'$c^s_{ij}/\delta^s_{ij}=P(Z_i<Z_j\mid Z_i\ne Z_j,y)$'+r'$\qquad P(\kappa=k\mid Z_i\ne Z_j,y)=w_kd^s_{ij,k}/\delta^s_{ij}$'+'\nAt '+r'$\delta^s_{ij}=0$'+', the ratio is undefined and all three neutral pair costs are zero.'
    fs.box(ax,.02,.02,.96,.96,text,fc='white',ec=C['line'],size=14 if mobile else 11.7)


def draw(mobile=False):
    fig=fs.canvas(4.8,17.2,True) if mobile else fs.canvas(10.8,9.4,False)
    if mobile:
        fig.text(.06,.985,'One selector chooses\none whole vector',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.06,.94,'Fix y, weights w and the same report g\nbefore drawing the auxiliary criterion.',ha='left',va='top',fontsize=12,linespacing=1.3)
    else:
        fig.text(.06,.965,'One selector chooses one whole vector',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.06,.91,'Fix observed information y, weights w and the same report g before the auxiliary draw.',ha='left',va='top',fontsize=12.5)
        fig.text(.06,.866,'Schematic array: arbitrary unit and criterion counts; within-column dependence is retained.',ha='left',va='top',fontsize=11.5,color=C['muted'])
    semantics=main_diagram(fig,mobile);identities(fig,mobile);neutral_inset(fig,mobile)
    return fig,semantics


def generate(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F11a.json';prior=json.loads(dest.read_text()) if dest.exists() else None
    paths=[ROOT/'assets/figures'/(STEM+s+'.'+ext) for s in ['', '-mobile'] for ext in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in paths)):raise SystemExit('Existing F11a outputs: --overwrite is for an authorized observed repair.')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    command='python3 -B assets/reproduction/figures/generators/F11a/generate.py'+(' --overwrite' if overwrite else '')
    attempt={'started_at_utc':now,'command':command,'status':'running'}
    record={'id':'F11a','fig_label':'fig-vis-f11a','step':'4.11','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,
            'status':'rendering','actual_render_invocations':(prior or {}).get('actual_render_invocations',0)+1,
            'execution_history':(prior or {}).get('execution_history',[])+[attempt],
            'actual_PNG_views':(prior or {}).get('actual_PNG_views',0),'views':(prior or {}).get('views',[]),'repairs':(prior or {}).get('repairs',[]),
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,FIGURES/'figstyle.py']],
            'source_refs':['chapters/11-multicriteria-loss.qmd (controlling text; not a runtime input)'],
            'scientific_inputs':'Literal symbolic labels and public style. Optional prior own receipt supplies bookkeeping only.',
            'numeric_coordinates':'Not applicable: array entries, criterion probabilities and loss quantities remain symbolic. Plot geometry has no scientific scale.',
            'neutral_inset_included':True,'caption_alt_sync_required':False,
            'scope':'Original conceptual rendering only. No numerical experiment, posterior draw, optimizer, package or scientific main-program execution.',
            
            'publication_and_licenses':'Deferred'}
    if prior:record['previous_export_history']=prior.get('previous_export_history',[])+[{'created_at_utc':prior['created_at_utc'],'inputs':prior['inputs'],'outputs':prior.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(record,indent=2)+'\n')
    try:
        outputs=[];ss=[]
        for mobile in [False,True]:
            fig,s=draw(mobile);ss.append(s);outputs.extend(fs.export(fig,STEM,mobile))
        assert ss[0]==ss[1]
        record['outputs']=outputs;record['diagram_counts_and_roles']=ss[0]
        record['status']='rendered'
        attempt.update({'status':'succeeded','output_count':6,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    except Exception as exc:
        attempt.update({'status':'failed','error':str(exc)});record['status']='render_failed';dest.write_text(json.dumps(record,indent=2)+'\n');raise
    dest.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
