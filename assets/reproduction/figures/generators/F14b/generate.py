"""F14b assembled fixed-order segmentation figure; public functions/data only."""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();FIGURES=HERE.parents[2]
sys.path.insert(0,str(FIGURES/'generators/F14b-costs'))
import cost_panel as cp
fs=cp.fs;ROOT=fs.ROOT;C=fs.PALETTE;STEM='fixed-order-segmentation'
from matplotlib.patches import Circle


def recovered_solution(d):
    states={(r['h'],r['r']):r for r in d['dp_states']};h,c=3,4;back=[(h,c)];endpoints=[]
    while h:
        row=states[h,c];assert len(row['optimal_predecessor_endpoints'])==1
        endpoints.append(c);c=row['optimal_predecessor_endpoints'][0];h-=1;back.append((h,c))
    assert (h,c)==(0,0)
    cuts=[0]+list(reversed(endpoints));assert cuts==[0,1,3,4]
    units=d['units_and_fixed_order'];blocks=[units[a:b] for a,b in zip(cuts,cuts[1:])]
    row=next(r for r in d['all_contiguous_partitions'] if r['endpoints']==cuts[1:])
    assert row['g']==[1,2,2,3] and row['N']==5 and row['blocks']==blocks
    W={(r['a']-1,r['b']):F(r['W']) for r in d['block_savings']};saving=sum(W[a,b] for a,b in zip(cuts,cuts[1:]))
    base=F(d['full_disclosure_risk']);risk=base-saving/d['M']
    assert saving==F(3,20) and saving/d['M']==F(1,40) and risk==F(row['risk'])==F(3,20)
    assert F(row['total_unnormalized_cost'])==F(9,10) and F(row['weighted_expected_error_count'])==F(13,20)
    last=d['exact_and_capped_optima'][-1]
    assert last['G_or_cap']==4 and F(last['exact_minimum_risk'])==F(7,40) and F(last['at_most_minimum_risk'])==F(3,20)
    assert last['exact_all_minimizers']==[[1,2,3,4]] and last['at_most_all_minimizers']==[[1,2,2,3]]
    return {'cuts':cuts,'backtracking_states':[list(x) for x in back],'forward_states':[list(x) for x in reversed(back)],
            'blocks':blocks,'grades':row['g'],'N':row['N'],'unnormalized_saving':str(saving),'risk_reduction':str(saving/d['M']),
            'full_disclosure_risk':str(base),'normalized_risk':str(risk),'unnormalized_total_cost':row['total_unnormalized_cost'],
            'exact4':last['exact_minimum_risk'],'at_most4':last['at_most_minimum_risk'],'status':'PASS'}


def recurrence(fig,rect,mobile=False):
    ax=fs.diagram_axis(fig,rect)
    if mobile:
        text='Maximum over the previous cut b:\n'+r'$V_h(c)=\max_b\{V_{h-1}(b)+W(b,c)\}$'+'\nwhere '+r'$h-1\leq b<c$'+'.'
    else:
        text=r'$V_h(c)=\max_{h-1\leq b<c}\{V_{h-1}(b)+W(b,c)\}$'+'\nThe state value is an unnormalized maximum saving.'
    fs.box(ax,.02,.02,.96,.96,text,size=13.5 if mobile else 14)


def recovery(fig,rect,solution,mobile=False):
    ax=fs.diagram_axis(fig,rect)
    ax.text(.02,.985,'(c) Recover the three-block report',ha='left',va='top',fontsize=13.5,fontweight='bold')
    x=lambda cut:.10+.80*cut/4
    nodes={};cy=.71;width=.085 if mobile else .07
    for cut in solution['cuts']:
        nodes[cut]=fs.box(ax,x(cut)-width/2,cy-.065,width,.13,str(cut),fc='white',ec=C['teal'],size=14 if mobile else 13.5)
    for left,right in zip(solution['cuts'],solution['cuts'][1:]):
        fs.arrow(ax,(x(left),cy),(x(right),cy),patchA=nodes[left],patchB=nodes[right])
    for grade,((left,right),block) in enumerate(zip(zip(solution['cuts'],solution['cuts'][1:]),solution['blocks']),1):
        xx=x(left);ww=x(right)-xx
        fs.box(ax,xx,.345,ww,.16,'  '.join(block),ec=C['teal'],size=14 if mobile else 13.5,weight='bold')
        ax.text(xx+ww/2,.205,'Grade '+str(grade),ha='center',va='center',fontsize=12.5 if mobile else 12)
    ax.text(.50,.045,r'$g=(1,2,2,3),\quad N=5$',ha='center',va='center',fontsize=14 if mobile else 13.5)
    return {'cut_nodes':4,'arrows':3,'blocks':solution['blocks'],'labelled_grades':[1,2,3],
            'semantics':'Recovered cut sequence, not time, sampling, an unrestricted search or a continuous action path.'}


def cap_cards(fig,rect,mobile=False):
    ax=fs.diagram_axis(fig,rect)
    fs.box(ax,.02,.06,.44,.88,'Exactly 4 grades\nRisk 7/40',fc='white',ec=C['ochre'],size=14 if mobile else 13)
    fs.box(ax,.54,.06,.44,.88,'At most 4 grades\nRisk 3/20',fc='white',ec=C['teal'],size=14 if mobile else 13)


def guard(fig,rect,mobile=False):
    ax=fs.diagram_axis(fig,rect)
    ax.text(.02,.985,'(d) Guarded neutral extension',ha='left',va='top',fontsize=13.5,fontweight='bold')
    ax.text(.02,.912,'Separate symbolic qualification',ha='left',va='top',fontsize=12.2,color=C['muted'])
    ax.text(.50,.84,'A full active-profile equality class H\nmust stay within one grade.',ha='center',va='top',fontsize=12.2 if mobile else 12.5,linespacing=1.25)
    # These are schematic class-extremum positions, not units from the numeric fixture.
    for xx,label in [(.15,'first H'),(.85,'last H')]:
        ax.add_patch(Circle((xx,.56),.035,facecolor='white',edgecolor=C['ink'],lw=1.4,zorder=3))
        ax.text(xx,.64,label,ha='center',va='center',fontsize=12.2)
    ax.plot([.185,.815],[.56,.56],color=C['line'],lw=2,zorder=1)
    ax.plot([.47,.53],[.53,.59],color=C['rust'],lw=2,zorder=4)
    ax.plot([.47,.53],[.59,.53],color=C['rust'],lw=2,zorder=4)
    ax.text(.50,.465,'forbidden cut t',ha='center',va='center',fontsize=13,color=C['rust'])
    ax.text(.50,.355,'No cut may split H between\nits first and last positions.',ha='center',va='top',fontsize=13.2,linespacing=1.25)
    ax.text(.50,.205,'Use the neutral loss and its baseline.\nKeep original units and pair multiplicities.',ha='center',va='top',fontsize=12 if mobile else 12.2,linespacing=1.25)
    ax.text(.50,.068,'Separate from the tie-free example;\nno package DP implementation is asserted.',ha='center',va='top',fontsize=11.7 if mobile else 12,linespacing=1.25,color=C['muted'])
    return {'symbolic_only':True,'applied_to_numeric_fixture':False,'class':'Full active-profile almost-sure equality class H',
            'forbidden_integer_cuts':'firstpos(H)<=t<lastpos(H)','actual_fixture_nontrivial_classes':0,
            'neutral_objective_qualification':'Use c_ij^s-tau*delta_ij^s and neutral baseline R0^s, retaining original M and all external pair multiplicities.',
            'package_DP_implementation_claim':False}


def check_canvas_text(fig):
    fig.canvas.draw();ren=fig.canvas.get_renderer();texts=list(fig.texts)
    for ax in fig.axes:
        texts.extend(ax.texts)
        if ax.axison:
            texts.extend([ax.title,ax.xaxis.label,ax.yaxis.label]+list(ax.get_xticklabels())+list(ax.get_yticklabels()))
    texts=[t for t in texts if t.get_text()]
    for t in texts:
        b=t.get_window_extent(ren)
        if not (b.x0>=1 and b.y0>=1 and b.x1<=fig.bbox.width-1 and b.y1<=fig.bbox.height-1):
            raise RuntimeError('Text outside canvas: '+t.get_text())
    for i,t in enumerate(texts):
        for u in texts[i+1:]:
            if t.get_window_extent(ren).overlaps(u.get_window_extent(ren)):
                raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
    return {'texts_checked':len(texts),'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True}


def draw(d,solution,mobile=False):
    if mobile:
        fig=fs.canvas(4.8,25.2,True)
        fig.text(.06,.985,'A dynamic program chooses\ngrade boundaries',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.06,.945,'Fixed order: A, B, C, D.\nw = (3/5, 2/5), τ = 1/4; M = 6.',ha='left',va='top',fontsize=12.5,linespacing=1.3)
        a=cp.draw_cost_triangle(fig.add_axes([.18,.745,.76,.145]),d,True)
        fig.text(.06,.705,'W(a,b) covers positions a+1 through b.\nSigned savings may be negative.',ha='left',va='top',fontsize=12.5,linespacing=1.3)
        b=cp.draw_prefix_states(fig.add_axes([.18,.50,.76,.145]),d,True)
        fig.text(.06,.463,'−∞ is infeasible; V₀(0)=0 is auxiliary.',ha='left',va='top',fontsize=12)
        recurrence(fig,[.05,.390,.90,.05],True)
        rec=recovery(fig,[.05,.268,.90,.10],solution,True)
        fig.text(.50,.245,'Saving 3/20; risk reduction 1/40.',ha='center',va='top',fontsize=13.5)
        fig.text(.50,.226,r'$R=7/40-(3/20)/6=3/20$',ha='center',va='top',fontsize=14.5)
        cap_cards(fig,[.05,.16,.90,.05],True)
        gu=guard(fig,[.05,.015,.90,.13],True)
    else:
        fig=fs.canvas(10.8,11.8,False)
        fig.text(.05,.98,'A dynamic program chooses grade boundaries',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.05,.935,'Fixed order A, B, C, D; w = (3/5, 2/5), τ = 1/4; M = 6.',ha='left',va='top',fontsize=12.5)
        a=cp.draw_cost_triangle(fig.add_axes([.08,.58,.35,.30]),d)
        b=cp.draw_prefix_states(fig.add_axes([.575,.58,.35,.30]),d)
        fig.text(.08,.525,'W(a,b) covers positions a+1 through b.\nSigned savings may be negative.',ha='left',va='top',fontsize=11.8,linespacing=1.3)
        fig.text(.575,.525,'−∞ is infeasible; V₀(0)=0 is auxiliary.\nOutlines select the three-block solution.',ha='left',va='top',fontsize=11.8,linespacing=1.3)
        recurrence(fig,[.05,.425,.90,.055])
        rec=recovery(fig,[.05,.205,.43,.19],solution)
        fig.text(.265,.175,'Saving 3/20; risk reduction 1/40.',ha='center',va='top',fontsize=12.5)
        fig.text(.265,.15,r'$R=7/40-(3/20)/6=3/20$',ha='center',va='top',fontsize=14)
        cap_cards(fig,[.05,.025,.43,.10])
        gu=guard(fig,[.55,.04,.40,.35])
    textcheck=check_canvas_text(fig)
    return fig,{'cost_panel':a,'prefix_panel':b,'recovery':rec,'guard':gu,'canvas_geometry':textcheck}


def generate(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F14b.json';prior=json.loads(dest.read_text()) if dest.exists() else None
    targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing F14b exports: --overwrite only for an authorized observed repair.')
    d,checks=cp.load_checked_data();solution=recovered_solution(d);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    attempt={'started_at_utc':now,'command':'python3 -B assets/reproduction/figures/generators/F14b/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_writes':0}
    record={'id':'F14b','fig_label':'fig-vis-f14b','step':'5.7','author':'JoonHo Lee (jlee296@ua.edu)',
            'created_at_utc':now,'status':'rendering','actual_render_invocations':(prior or {}).get('actual_render_invocations',0)+1,
            'execution_history':(prior or {}).get('execution_history',[])+[attempt],'actual_PNG_views':(prior or {}).get('actual_PNG_views',0),
            'views':(prior or {}).get('views',[]),'repairs':(prior or {}).get('repairs',[]),
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,Path(cp.__file__),cp.DATA,cp.BASE/'figstyle.py']],
            'source_refs':['chapters/14-computing-grades.qmd (controlling text; not a runtime input)'],
            'scientific_input_policy':'Only public data, reusable drawing functions and style. No canonical chapter, private staging image, contract or register is required. An optional prior own receipt supplies bookkeeping only.',
            'reused_public_module':str(Path(cp.__file__).relative_to(ROOT)),
            'stage_execution_relation':'This is final assembly Step5.7; command/output/view counts here exclude the distinct Step5.6 staging producer.',
            'fresh_exact_table_checks':checks,'fresh_exact_table_cells':len(checks),'recovered_solution':solution,
            'scope':'Exact small saved-instance checks and deterministic rendering. No original DP program, numerical solver, simulation, package or model execution.',
            
            'publication_and_licenses':'Deferred'}
    if prior:record['previous_export_history']=prior.get('previous_export_history',[])+[{'created_at_utc':prior['created_at_utc'],'inputs':prior['inputs'],'outputs':prior.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(record,indent=2)+'\n')
    try:
        outputs=[];layouts=[]
        for mobile in [False,True]:
            fig,layout=draw(d,solution,mobile);layouts.append(layout);outputs.extend(fs.export(fig,STEM,mobile));attempt['layout_exports']+=1;attempt['asset_writes']+=3
        for k in ['recovery','guard']:assert layouts[0][k]==layouts[1][k]
        assert layouts[0]['cost_panel']['values']==layouts[1]['cost_panel']['values'] and layouts[0]['prefix_panel']['values']==layouts[1]['prefix_panel']['values']
        record['outputs']=outputs;record['layouts']=layouts;record['status']='rendered';attempt['status']='succeeded'
    except Exception as exc:
        attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
