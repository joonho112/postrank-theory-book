"""F19a: one exact joint law, two targets and matched-disclosure grades."""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();BASE=HERE.parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle
ROOT=fs.ROOT;C=fs.PALETTE;DATA=BASE/'data/scalar-and-common-grade.json'
STEM='f19a-from-target-states-to-matrices-to-common-grades'
PAIRS=['AB','AC','AD','BC','BD','CD']


def checked_data():
    d=json.loads(DATA.read_text())['common_grade'];w=list(map(F,d['criterion_error_weights_w']));a=list(map(F,d['composite_magnitude_coefficients_a']));tau=F(d['tau'])
    assert d['units']==list('ABCD') and d['M']==6 and w==[F(3,5),F(2,5)] and a==[F(3,4),F(1,4)] and tau==F(1,5)
    states=[(r['theta_unit_by_criterion'],F(r['probability'])) for r in d['states']];assert sum(p for _,p in states)==1
    cs=[[sum(ak*v for ak,v in zip(a,row)) for row in theta] for theta,_ in states]
    assert [[str(v) for v in row] for row in cs]==d['composite_by_state']
    checks=[]
    for row in d['forward_pair_rows']:
        i,j=map(d['units'].index,row['pair']);e=[sum(p for theta,p in states if theta[i][k]<=theta[j][k]) for k in range(2)]
        ew=sum(ww*v for ww,v in zip(w,e));ea=sum(p for (_,p),c in zip(states,cs) if c[i]<=c[j])
        assert e==list(map(F,row['criterion_errors'])) and ew==F(row['directional_error']) and ea==F(row['composite_error'])
        checks.append({'pair':row['pair'],'criterion_errors':list(map(str,e)),'weighted_error':str(ew),'composite_error':str(ea),'status':'PASS'})
    reports=[]
    for g in [[1,2,2,3],[1,1,2,3]]:
        row=next(r for r in d['selected_reports'] if r['g']==g);ds=[(i,j) for i in range(4) for j in range(4) if g[i]<g[j]]
        ec=[sum(p*sum(theta[i][k]<=theta[j][k] for i,j in ds) for theta,p in states) for k in range(2)]
        ew=sum(ww*v for ww,v in zip(w,ec));ea=sum(p*sum(c[i]<=c[j] for i,j in ds) for (_,p),c in zip(states,cs))
        assert len(ds)==row['N']==5 and ec==list(map(F,row['criterion_expected_wrong_counts']))
        for key,count in [('directional',ew),('composite',ea)]:
            assert count==F(row[key]['A']) and (count+tau)/6==F(row[key]['R'])
        assert [m['pair'] for m in row['pair_masks']]==PAIRS
        for mask in row['pair_masks']:
            i,j=map(d['units'].index,mask['pair']);assert mask['disclosed']==(g[i]!=g[j])
        reports.append(row)
    assert reports[0]['directional']['R']=='17/120' and reports[0]['composite']['R']=='3/40'
    assert reports[1]['directional']['R']=='1/6' and reports[1]['composite']['R']=='1/30'
    assert d['accepted_optima']['directional']['actions']==[[1,2,2,3]] and d['accepted_optima']['composite']['actions']==[[1,1,2,3]]
    return d,reports,checks


def state_table(ax,d,idx,mobile=False):
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');state=d['states'][idx]
    ax.text(.02,.985,'(a'+str(idx+1)+') State '+str(idx+1)+': probability '+state['probability'],ha='left',va='top',fontsize=13.5,fontweight='bold')
    for x,label in [(.10,'Unit'),(.36,r'$\theta_1$'),(.59,r'$\theta_2$'),(.84,'Composite c')]:
        ax.text(x,.77,label,ha='center',va='center',fontsize=13 if mobile else 12.5,fontweight='bold')
    ax.axvline(.72,ymin=.04,ymax=.68,color=C['line'],lw=.9)
    values=[]
    for i,(unit,row,composite) in enumerate(zip(d['units'],state['theta_unit_by_criterion'],d['composite_by_state'][idx])):
        y=.61-i*.17
        ax.text(.10,y,unit,ha='center',va='center',fontsize=14,fontweight='bold')
        for x,value in zip([.36,.59,.84],[str(row[0]),str(row[1]),composite]):ax.text(x,y,value,ha='center',va='center',fontsize=14)
        values.append({'unit':unit,'targets':row,'composite':composite})
    return {'state':idx+1,'probability':state['probability'],'values':values}


def coefficients(ax,d,mobile=False):
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    ax.text(.015,.985,'(b) Forward error coefficients',ha='left',va='top',fontsize=13.5,fontweight='bold')
    rows=d['forward_pair_rows'];assert [r['pair'] for r in rows]==PAIRS
    for j,row in enumerate(rows):
        x=.325+j*.12;ax.text(x,.70,row['pair'],ha='center',va='center',fontsize=13.5,fontweight='bold')
        for y,key in [(.45,'directional_error'),(.16,'composite_error')]:
            edge=C['ochre'] if row['pair']=='AB' else C['teal'] if row['pair']=='BC' else C['line']
            ax.add_patch(Rectangle((x-.055,y-.105),.11,.21,facecolor='white',edgecolor=edge,lw=1.5 if row['pair'] in ['AB','BC'] else .8))
            ax.text(x,y,row[key],ha='center',va='center',fontsize=14)
    ax.text(.015,.45,'Weighted\ndirection',ha='left',va='center',fontsize=12.5,linespacing=1.2)
    ax.text(.015,.16,'Composite',ha='left',va='center',fontsize=12.5)
    return {'pairs':PAIRS,'weighted_errors':[r['directional_error'] for r in rows],'composite_errors':[r['composite_error'] for r in rows],'directions':'First named unit above the second; only forward entries displayed.'}


def report_card(ax,row,target,mobile=False):
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');color=C['teal'] if target=='directional' else C['ochre']
    label='Weighted-direction optimum 1223' if target=='directional' else 'Composite optimum 1123'
    ax.text(.02,.985,'(c) '+label,ha='left',va='top',fontsize=13 if mobile else 12.8,fontweight='bold')
    left=.08
    for block in row['blocks']:
        width=.84*len(block)/4
        ax.add_patch(Rectangle((left,.57),width,.18,facecolor=C['light'],edgecolor=color,lw=1.4))
        ax.text(left+width/2,.66,'  '.join(block),ha='center',va='center',fontsize=14,fontweight='bold');left+=width
    ax.text(.50,.43,'g = ('+', '.join(map(str,row['g']))+');  N = 5',ha='center',va='center',fontsize=12.7)
    for j,mask in enumerate(row['pair_masks']):
        x=.10+j*.16;ax.text(x,.285,mask['pair'],ha='center',va='center',fontsize=13)
        ax.scatter([x],[.105],s=62,marker='o',facecolor=color if mask['disclosed'] else 'white',edgecolor=C['ink'],lw=1.3)
    return {'g':row['g'],'blocks':row['blocks'],'N':row['N'],'pair_masks':row['pair_masks'],'optimal_for':target}


def risk_table(ax,reports,mobile=False):
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    ax.text(.02,.985,'(d) Same N = 5; evaluate each loss',ha='left',va='top',fontsize=13.3,fontweight='bold')
    for x,label in [(.14,'Report'),(.50,'Weighted risk'),(.82,'Composite risk')]:
        if mobile and label!='Report':label=label.replace(' ','\n')
        ax.text(x,.70,label,ha='center',va='center',fontsize=12.7,fontweight='bold',linespacing=1.15)
    values=[]
    for y,row in zip([.43,.14],reports):
        code=''.join(map(str,row['g']));ax.text(.14,y,code,ha='center',va='center',fontsize=14)
        for x,key in [(.50,'directional'),(.82,'composite')]:
            preferred=(code=='1223' and key=='directional') or (code=='1123' and key=='composite')
            ax.add_patch(Rectangle((x-.14,y-.105),.28,.21,facecolor=C['light'] if preferred else 'white',edgecolor=C['teal'] if key=='directional' and preferred else C['ochre'] if preferred else C['line'],lw=1.7 if preferred else .8))
            ax.text(x,y,row[key]['R'],ha='center',va='center',fontsize=14.5,fontweight='bold' if preferred else 'normal')
        values.append({'g':row['g'],'R_w':row['directional']['R'],'R_a':row['composite']['R']})
    return {'values':values,'minima_scope':'Each preferred cell is compared only within its own loss column.','risk_denominator':6,'disclosure_count_both_reports':5}


def text_geometry(fig):
    fig.canvas.draw();ren=fig.canvas.get_renderer();texts=list(fig.texts)
    for ax in fig.axes:texts+=list(ax.texts)
    for t in texts:
        bb=t.get_window_extent(ren)
        if not(bb.x0>=1 and bb.x1<=fig.bbox.width-1 and bb.y0>=1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
    for i,t in enumerate(texts):
        for u in texts[i+1:]:
            if t.get_window_extent(ren).overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
    return {'text_records':len(texts),'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True}


def draw(d,reports,mobile=False):
    if mobile:
        fig=fs.canvas(4.8,24,True)
        fig.text(.06,.985,'From target states\nto two common grades',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.06,.947,'One joint law; w = (3/5, 2/5),\na = (3/4, 1/4), τ = 1/5; M = 6.',ha='left',va='top',fontsize=12.5,linespacing=1.3)
        states=[state_table(fig.add_axes([.08,.79,.84,.115]),d,0,True),state_table(fig.add_axes([.08,.64,.84,.115]),d,1,True)]
        fig.text(.06,.61,r'$c_i=(3/4)\theta_{i1}+(1/4)\theta_{i2}$'+'\nw weights directional errors.\na combines target magnitudes.',ha='left',va='top',fontsize=13.5,linespacing=1.3)
        coeff=coefficients(fig.add_axes([.04,.485,.92,.09]),d,True)
        cards=[report_card(fig.add_axes([.05,.35,.90,.10]),reports[0],'directional',True),report_card(fig.add_axes([.05,.22,.90,.10]),reports[1],'composite',True)]
        fig.text(.06,.198,'Filled: forward direction. Open: withhold.',ha='left',va='top',fontsize=12.4)
        risks=risk_table(fig.add_axes([.05,.07,.90,.11]),reports,True)
        fig.text(.06,.035,'Risk uses M = 6; fractions use N.\nLower losses across targets do not choose\nthe substantively appropriate target.',ha='left',va='top',fontsize=12.3,linespacing=1.3)
    else:
        fig=fs.canvas(10.8,12.8,False)
        fig.text(.05,.98,'From target states to two common grades',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.05,.94,'One joint law; w = (3/5, 2/5), a = (3/4, 1/4), τ = 1/5; M = 6.',ha='left',va='top',fontsize=12.5)
        states=[state_table(fig.add_axes([.07,.70,.39,.20]),d,0),state_table(fig.add_axes([.56,.70,.39,.20]),d,1)]
        fig.text(.07,.665,r'$c_i=(3/4)\theta_{i1}+(1/4)\theta_{i2}$'+'\nw weights errors; a combines target magnitudes.',ha='left',va='top',fontsize=12.5,linespacing=1.3)
        coeff=coefficients(fig.add_axes([.08,.465,.84,.15]),d)
        cards=[report_card(fig.add_axes([.05,.23,.43,.16]),reports[0],'directional'),report_card(fig.add_axes([.53,.23,.43,.16]),reports[1],'composite')]
        risks=risk_table(fig.add_axes([.05,.075,.90,.105]),reports)
        fig.text(.05,.04,'Filled circle: forward direction. Open circle: withhold. Both reports disclose five of six pairs.\nCompare minima within each target; loss magnitudes do not choose the substantive target.',ha='left',va='top',fontsize=11.5,linespacing=1.3)
    return fig,{'states':states,'coefficient_matrix':coeff,'report_cards':cards,'risk_table':risks,'geometry':text_geometry(fig)}


def main(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F19a.json';old=json.loads(dest.read_text()) if dest.exists() else None
    targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs: --overwrite only for an observed authorized repair.')
    d,reports,checks=checked_data();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    attempt={'started_at_utc':now,'status':'running','command':'python3 -B assets/reproduction/figures/generators/F19a/generate.py'+(' --overwrite' if overwrite else ''),'layout_exports':0,'asset_writes':0}
    record={'id':'F19a','step':'6.12','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':(old or {}).get('execution_history',[])+[attempt],'views':(old or {}).get('views',[]),'repairs':(old or {}).get('repairs',[]),'actual_PNG_views':(old or {}).get('actual_PNG_views',0),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,DATA,BASE/'figstyle.py']],'coordinate_selector':'common_grade only; no private fixture or contract required.','fresh_forward_pair_checks':checks,'scope':'Small exact state/pair/report arithmetic and plotting of inherited accepted optima; no original75-action program, solver, simulation, fit or package execution.','publication_and_licenses':'Deferred'}
    record['chapter_provenance_from_public_data']=[v for v in json.loads(DATA.read_text())['source_files'] if v['path']=='chapters/19-worked-examples.qmd'][0];record['chapter_runtime_read_count']=0
    if old:record['previous_export_history']=old.get('previous_export_history',[])+[{'created_at_utc':old['created_at_utc'],'inputs':old['inputs'],'outputs':old.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(record,indent=2)+'\n')
    try:
        outputs=[];layouts=[]
        for mobile in [False,True]:
            fig,layout=draw(d,reports,mobile);layouts.append(layout);out=fs.export(fig,STEM,mobile);outputs+=out;record['outputs']=outputs;attempt['layout_exports']+=1;attempt['asset_writes']+=3
        for k in ['states','coefficient_matrix','report_cards','risk_table']:assert layouts[0][k]==layouts[1][k]
        record['layouts']=layouts;record['status']='rendered';attempt['status']='succeeded'
    except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);record['status']='render_failed';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
