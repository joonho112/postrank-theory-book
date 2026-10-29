#!/usr/bin/env python3
"""Exact finite illustration of local withholding versus coherent grades.

Scientific inputs are public frozen coordinates. The thirteen saved actions
are checked directly against four states; no model or optimizer is run.
"""
from pathlib import Path
from fractions import Fraction as F
import sys, json, hashlib, datetime, platform, argparse
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch

ROOT=fs.ROOT; HERE=Path(__file__).resolve()
DATA=BASE/'data/scalar-and-common-grade.json'
DEST=ROOT/'evidence/figures/builds/F10b.json'
STEM='f10b-locally-attractive-comparisons-can-be-incoherent'


def checked_data():
    d=json.loads(DATA.read_text())['scalar_incompatible_ties']
    assert d['units']==['A','B','C'] and d['pair_order']==[['A','B'],['A','C'],['B','C']]
    assert d['M']==3 and F(d['tau'])==F(1,5)
    assert sum(F(s['probability']) for s in d['states'])==1
    assert all(len(set(s['theta']))==3 for s in d['states'])
    probability={}
    for i,a in enumerate(d['units']):
        for j,b in enumerate(d['units']):
            if i!=j:
                p=sum(F(s['probability']) for s in d['states'] if s['theta'][i]>s['theta'][j])
                assert p==F(d['pair_probabilities'][a+'>'+b])
                probability[a+'>'+b]=str(p)
    local=[]
    for row in d['isolated_pair_decisions']:
        a,b=row['pair'];cost=[1-F(probability[a+'>'+b]),1-F(probability[b+'>'+a]),F(d['tau'])]
        assert cost==[F(row[k]) for k in ['cost_first_above','cost_reverse','cost_withhold']]
        assert min(cost)==F(row['minimum'])
        local.append(str(min(cost)))
    assert d['relaxed_relations']==[0,1,0] and d['relaxed_report_feasible'] is False
    assert [r['minimizing_relations'] for r in d['isolated_pair_decisions']]==[[0],[1],[0]]
    relaxed=sum(map(F,local))/3
    assert relaxed==F(d['relaxed_minimum'])==F(1,6)
    action_checks=[]
    for row in d['coherent_actions']:
        g=row['g']; pairs=[(i,j) for i in range(3) for j in range(3) if g[i]<g[j]]
        wrong=[sum(s['theta'][i]<=s['theta'][j] for i,j in pairs) for s in d['states']]
        expected=sum(F(s['probability'])*w for s,w in zip(d['states'],wrong))
        risk=(expected+F(d['tau'])*(3-len(pairs)))/3
        assert wrong==row['state_wrong_counts'] and len(pairs)==row['N']
        assert expected==F(row['expected_wrong']) and risk==F(row['risk'])
        if pairs:assert expected/len(pairs)==F(row['disclosed_error_fraction'])
        action_checks.append({'g':g,'N':len(pairs),'expected_wrong':str(expected),'risk':str(risk)})
    assert len(action_checks)==13 and len({tuple(r['g']) for r in action_checks})==13
    minimum=min(F(r['risk']) for r in action_checks)
    argmin={tuple(r['g']) for r in action_checks if F(r['risk'])==minimum}
    assert minimum==F(d['accepted_grade_minimum'])==F(11,60)
    assert argmin=={tuple(g) for g in d['accepted_grade_argmin_set']}=={(1,1,2),(1,2,2)}
    assert minimum-relaxed==F(d['coherence_gap'])==F(1,60)
    opt=[r for r in d['coherent_actions'] if tuple(r['g']) in argmin]
    for row in opt:
        extra=[x for x in row['disclosures'] if x['above']+x['below']!='AC']
        assert len(extra)==1 and F(extra[0]['error_probability'])==F(1,4)>F(d['tau'])
        row['additional_direction']=extra[0]['above']+'>'+extra[0]['below']
    law=[]
    for s in d['states']:
        order=''.join(d['units'][i] for i in sorted(range(3),key=lambda i:s['theta'][i],reverse=True))
        law.append(order+': '+s['probability'])
    return d,opt,law,{'state_mass':'1','latent_tie_probability':'0','directional_probabilities':probability,
           'local_minima':local,'relaxed_normalized_cost':str(relaxed),
           'all_thirteen_saved_actions_checked':action_checks,
           'full_minimizing_set':[list(g) for g in sorted(argmin)],
           'minimum':str(minimum),'gap':str(minimum-relaxed),
           'additional_direction_error':'1/4 > tau=1/5',
           'check_scope':'Exact arithmetic readback of four frozen states and thirteen saved actions; no enumeration search,solver,simulation or fitted model.'}


def draw(d,opt,law,mobile):
    fig=fs.canvas(4.8 if mobile else 10.4,17 if mobile else 10,mobile)
    ax=fs.diagram_axis(fig,(.025,.02,.95,.94))
    fig.text(.04,.985,'Local choices can conflict\nwith common grades' if mobile else
             'Local choices can conflict with common grades',ha='left',va='top',
             fontsize=16,fontweight='semibold',linespacing=1.2)
    containers={};texts=[]
    size=14 if mobile else 12.5

    def panel(key,rect,color=None):
        p=FancyBboxPatch(rect[:2],rect[2],rect[3],
                        boxstyle='round,pad=0.003,rounding_size=0.008',
                        facecolor='white',edgecolor=color or fs.PALETTE['line'],linewidth=1.2,zorder=1)
        ax.add_patch(p);containers[key]=p;return rect

    def tx(key,label,xx,yy,value,font=None,weight='normal',color=None):
        x,y,w,h=rects[key]
        t=ax.text(x+w*xx,y+h*yy,value,ha='center',va='center',
                  fontsize=font or size,fontweight=weight,
                  color=color or fs.PALETTE['ink'],linespacing=1.22,zorder=3)
        texts.append((key,label,t));return t

    if mobile:
        rects={'law':(.015,.825,.97,.10),'local':(.015,.615,.97,.19),
               'logic':(.015,.495,.97,.10),'opt0':(.015,.292,.97,.165),'opt1':(.015,.107,.97,.165)}
    else:
        rects={'law':(.015,.82,.97,.12),'local':(.015,.53,.97,.265),
               'logic':(.015,.395,.97,.11),'opt0':(.015,.12,.465,.225),'opt1':(.52,.12,.465,.225)}
    for key,r in rects.items():panel(key,r,fs.PALETTE['rust'] if key=='logic' else fs.PALETTE['teal'] if key.startswith('opt') else None)
    tx('law','law heading',.5,.82,'One exact finite belief;\nall four states are tie-free.' if mobile else 'One exact finite belief; all states are tie-free.',weight='semibold')
    tx('law','law states',.5,.49,('\n'.join(['   |   '.join(law[:2]),'   |   '.join(law[2:])]) if mobile else '    |    '.join(law)))
    tx('law','law convention',.5,.16,'Orders descend; τ = 1/5.\nRisk denominator M = 3.' if mobile else 'Orders descend; τ = 1/5.  Risk denominator M = 3.',font=14 if mobile else 12)
    tx('local','local heading',.5,.90,'Independent pair choices:\ninfeasible as one report' if mobile else 'Independent pair choices: infeasible as one report',font=14 if mobile else 14,weight='semibold')
    for k,row in enumerate(d['isolated_pair_decisions']):
        x,y,w,h=rects['local'];subkey='pair'+str(k)
        r=(x+w*(.035+k*.325),y+h*.25,w*.28,h*.49)
        rects[subkey]=r;panel(subkey,r,fs.PALETTE['ochre'] if k!=1 else fs.PALETTE['teal'])
        relation='Withhold' if row['minimizing_relations']==[0] else 'A>C'
        tx(subkey,'pair action',.5,.5,''.join(row['pair'])+'\n'+relation+'\ncost '+row['minimum'],weight='semibold')
    tx('local','relaxed sum',.5,.11,'Relaxed cost =\n(1/5 + 1/10 + 1/5)/3 = 1/6' if mobile else 'Relaxed cost = (1/5 + 1/10 + 1/5)/3 = 1/6',font=14 if mobile else 13)
    tx('logic','tie transitivity',.5,.66,
       'If AB and BC share grades,\nall three must share one grade.' if mobile else
       'If AB and BC share grades, all three must share one grade.',weight='semibold',color=fs.PALETTE['rust'])
    tx('logic','conflicting endpoint',.5,.23,'This contradicts issuing A>C.',color=fs.PALETTE['rust'])
    ax.text(.5,.477 if mobile else .369,'Both minimize among all\n13 ordered partitions' if mobile else 'Both minimize over all 13 ordered partitions',ha='center',va='center',
            fontsize=14 if mobile else 13.5,fontweight='semibold')
    for k,row in enumerate(opt):
        key='opt'+str(k)
        tx(key,'equal optimum',.5,.90,'Coherent optimum',font=15 if mobile else 14,weight='semibold')
        blocks=' > '.join('{'+', '.join(b)+'}' for b in row['blocks'])
        tx(key,'ordered blocks',.5,.71,blocks,font=17 if mobile else 16,weight='semibold',color=fs.PALETTE['teal'])
        tx(key,'grade vector',.5,.54,'g = ('+', '.join(map(str,row['g']))+') in A, B, C order')
        tx(key,'risk and disclosure',.5,.37,'N = 2;  normalized risk = '+row['risk'],weight='semibold')
        tx(key,'additional direction',.5,.14,
           'Additional direction: '+row['additional_direction']+'\nError 1/4 > τ = 1/5',font=14 if mobile else 12.5)
    ax.text(.5,.078 if mobile else .075,'Coherence gap: 11/60 − 1/6 = 1/60',ha='center',va='center',
            fontsize=14 if mobile else 13.5,fontweight='semibold')
    fig.text(.04,.018,
             ('Majority order A>B>C is transitive.\nReport ties do not assert latent equality.\nAuthor construction; not KRW Gaussian data.') if mobile else
             ('Majority order A>B>C is transitive. Report ties withhold directions; they do not assert latent equality.\n'
              'Author finite construction illustrating KRW Example 1; not its Gaussian reproduction.'),
             ha='left',va='bottom',fontsize=14 if mobile else 11.5,
             linespacing=1.25,color=fs.PALETTE['muted'])
    fig.canvas.draw();renderer=fig.canvas.get_renderer();checks=[]
    for key,label,t in texts:
        bb=t.get_window_extent(renderer);rb=containers[key].get_window_extent(renderer)
        checks.append({'container':key,'label':label,'font_pt':t.get_fontsize(),
                       'inside':bool(bb.x0>=rb.x0+1 and bb.x1<=rb.x1-1 and bb.y0>=rb.y0+1 and bb.y1<=rb.y1-1)})
    alltext=list(ax.texts)+list(fig.texts)
    for i,t in enumerate(alltext):
        bb=t.get_window_extent(renderer)
        if not (bb.x0>=1 and bb.y0>=1 and bb.x1<=fig.bbox.width-1 and bb.y1<=fig.bbox.height-1):
            raise RuntimeError('Text outside canvas: '+t.get_text())
        for u in alltext[i+1:]:
            if bb.overlaps(u.get_window_extent(renderer)):
                raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
    if not all(c['inside'] for c in checks):raise RuntimeError('Container clipping: '+str([c for c in checks if not c['inside']]))
    return fs.export(fig,STEM,mobile),{'mobile':mobile,'canvas_inches':[4.8,17] if mobile else [10.4,10],
               'containment_checks':checks,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,
               'equal_optimum_card_dimensions':list(rects['opt0'][2:]),'both_optima_equally_emphasized':rects['opt0'][2:]==rects['opt1'][2:],
               'mobile_minimum_font_px_at332':14*96/72*332/(4.8*96) if mobile else None,
               'connectors':0,'connector_semantics':'No connecting optimization trajectory is implied.'}


def generate(overwrite=False):
    outputs=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (DEST.exists() or any(p.exists() for p in outputs)):
        raise SystemExit('Existing outputs; --overwrite requires an authorized recorded repair.')
    old=json.loads(DEST.read_text()) if DEST.exists() else None
    d,opt,law,checks=checked_data()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    attempt={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/F10b/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','layout_exports':0,'asset_exports':0}
    history=(old or {}).get('execution_history',[])+[attempt]
    record={'id':'F10b','step':'4.10','created_at_utc':now,'author':'JoonHo Lee (jlee296@ua.edu)',
            'status':'rendering','execution_history':history,'actual_image_views':(old or {}).get('actual_image_views',[]),
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in [DATA,BASE/'figstyle.py',HERE]],
            'exact_checks':checks,'scope':'Exact readback of the public four-state/thirteen-action example, followed by figure rendering. No model,optimizer,simulation or original example-program execution.',
            'scientific_boundaries':['The local pattern is not an issuable common grade.','The obstruction is report-tie transitivity,not a Condorcet majority cycle.','Both unrestricted coherent optima are equally emphasized.','A disclosed direction can have error above tau; risk uses M=3.','The finite law is the monograph author construction,not a reproduction of the KRW Gaussian example.'],
            'limits':['Author checks and views are not independent scientific acceptance.','Only public coordinate/style/source inputs are needed at runtime.'],
            'publication_and_licenses':'Deferred','required_repairs_remaining':[]}
    if old:record['previous_output_history']=old.get('previous_output_history',[])+[{'outputs':old.get('outputs',[]),'geometry_checks':old.get('geometry_checks',[])}]
    DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(record,indent=2)+'\n')
    try:
        files=[];geometry=[]
        for mobile in [False,True]:
            out,geo=draw(d,opt,law,mobile);files.extend(out);geometry.append(geo)
            attempt['layout_exports']+=1;attempt['asset_exports']+=3
        assert all(g['both_optima_equally_emphasized'] for g in geometry)
        assert [x['path'] for x in files]==[str(p.relative_to(ROOT)) for p in outputs]
        record['outputs']=files;record['geometry_checks']=geometry;record['status']='rendered'
        attempt['status']='succeeded'
    except Exception as exc:
        attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed'
        raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        record['execution']={'python':platform.python_version(),'renderer_invocations_total':len(history),'last_command_invocations':1,
                             'layout_exports_total':sum(x['layout_exports'] for x in history),'asset_writes_total':sum(x['asset_exports'] for x in history),
                             'model_runs':0,'optimizer_runs':0,'simulation_runs':0,'canonical_edits':0,'register_edits':0}
        DEST.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'id':'F10b','outputs':record['outputs'],'geometry':'PASS','render_commands_total':len(history)},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');generate(p.parse_args().overwrite)
