'Render reusable F14b cost panels.'
from pathlib import Path
import argparse,datetime,hashlib,json
import cost_panel as cp
fs=cp.fs;ROOT=fs.ROOT;HERE=Path(__file__).resolve()
DEST=ROOT/'evidence/figures/builds/F14b-costs.json'
OUT=ROOT/'evidence/figures/staging/F14b-costs'


def draw(d,mobile=False):
    if mobile:
        fig=fs.canvas(4.8,14.8,True)
        fig.text(.06,.985,'Signed block savings\nand prefix states',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.06,.922,'Fixed order: A, B, C, D.\nw = (3/5, 2/5), τ = 1/4; M = 6.',ha='left',va='top',fontsize=12,linespacing=1.3)
        a=cp.draw_cost_triangle(fig.add_axes([.18,.605,.76,.245]),d,True)
        fig.text(.06,.535,'W(a,b) covers positions a+1 through b.\nHatching: a ≥ b is not an interval.\nNegative savings remain eligible.',ha='left',va='top',fontsize=12,linespacing=1.3)
        b=cp.draw_prefix_states(fig.add_axes([.18,.185,.76,.245]),d,True)
        fig.text(.06,.108,'Both tables show unnormalized savings.\nOutlines mark one three-block solution.\n−∞ means infeasible; V₀(0)=0 is auxiliary.',ha='left',va='top',fontsize=12,linespacing=1.35)
    else:
        fig=fs.canvas(10.8,7.4,False)
        fig.text(.05,.96,'Signed block savings and prefix states',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.05,.90,'Fixed order A, B, C, D; w = (3/5, 2/5), τ = 1/4; M = 6.',ha='left',va='top',fontsize=12.5)
        a=cp.draw_cost_triangle(fig.add_axes([.08,.32,.35,.47]),d)
        b=cp.draw_prefix_states(fig.add_axes([.575,.32,.35,.47]),d)
        fig.text(.08,.24,'W(a,b) covers positions a+1 through b.\nHatching: a ≥ b is not an interval.',ha='left',va='top',fontsize=11.8,linespacing=1.3)
        fig.text(.575,.24,r'$V_h(c)$ maximizes block savings'+'\nfor h nonempty blocks in prefix c.',ha='left',va='top',fontsize=11.8,linespacing=1.3)
        fig.text(.05,.14,'Both tables show signed savings, not normalized risk. Negative interval savings remain eligible.',ha='left',va='top',fontsize=12)
        fig.text(.05,.085,'Outlined cells/states belong to the selected three-block solution.',ha='left',va='top',fontsize=11.8)
        fig.text(.05,.035,'−∞ means infeasible. The empty-prefix state V₀(0)=0 is auxiliary.',ha='left',va='top',fontsize=11.5)
    return fig,[a,b]


def generate(overwrite=False):
    expected=[OUT.with_name(OUT.name+s).with_suffix('.'+ext) for s in ['', '-mobile'] for ext in ['svg','png']]
    if not overwrite and (DEST.exists() or any(p.exists() for p in expected)):raise SystemExit('Existing staging outputs: --overwrite only for a recorded observed repair.')
    prior=json.loads(DEST.read_text()) if DEST.exists() else None
    d,checks=cp.load_checked_data();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    attempt={'started_at_utc':now,'command':'python3 -B assets/reproduction/figures/generators/F14b-costs/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_writes':0}
    record={'id':'F14b-costs','figure':'F14b','step':'5.6','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering',
            'actual_render_invocations':(prior or {}).get('actual_render_invocations',0)+1,'execution_history':(prior or {}).get('execution_history',[])+[attempt],
            'actual_PNG_views':(prior or {}).get('actual_PNG_views',0),'views':(prior or {}).get('views',[]),'repairs':(prior or {}).get('repairs',[]),
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,Path(cp.__file__),cp.DATA,cp.BASE/'figstyle.py']],
            'fresh_exact_checks':checks,'fresh_exact_checked_cells':len(checks),
            'scope':'Staged cost panels only. Staged SVG/PNG files are optional outputs, not scientific inputs to the assembled figure. No block/guard panel or final F14b exports are created.',
            'public_reuse_interface':['cost_panel.load_checked_data()','cost_panel.draw_cost_triangle(ax,data,mobile=False)','cost_panel.draw_prefix_states(ax,data,mobile=False)'],
            'scientific_execution':'Only small exact checks of six forward errors, ten W values and 25 saved prefix cells. No original DP program, numerical solver, model, simulation or package execution.',
             'publication_and_licenses':'Deferred'}
    if prior:record['previous_export_history']=prior.get('previous_export_history',[])+[{'created_at_utc':prior['created_at_utc'],'inputs':prior['inputs'],'outputs':prior.get('outputs',[])}]
    DEST.parent.mkdir(parents=True,exist_ok=True);OUT.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
    try:
        outputs=[];layouts=[]
        for mobile in [False,True]:
            fig,layout=draw(d,mobile);layouts.append(layout)
            stem=OUT.with_name(OUT.name+('-mobile' if mobile else ''))
            for ext in ['svg','png']:
                p=stem.with_suffix('.'+ext);meta={'Date':None,'Creator':'JoonHo Lee (jlee296@ua.edu)'} if ext=='svg' else {'Author': 'JoonHo Lee (jlee296@ua.edu)', 'Software': 'Matplotlib'}
                fig.savefig(p,dpi=160,metadata=meta,bbox_inches=None);outputs.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size});attempt['asset_writes']+=1
            fs.plt.close(fig)
        for idx in range(2):
            assert layouts[0][idx]['values']==layouts[1][idx]['values']
        record['outputs']=outputs;record['panel_geometry']=layouts;record['status']='staged';attempt['status']='succeeded'
    except Exception as exc:
        attempt['status']='failed';attempt['error']=str(exc);record['status']='staging_failed';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();DEST.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'receipt':str(DEST.relative_to(ROOT)),'outputs':outputs,'exact_checked_cells':len(checks)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
