"""F20: two archived common actions on a shared 97-firm count scale."""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();BASE=HERE.parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle
ROOT=fs.ROOT;C=fs.PALETTE;DATA=BASE/'data/krw-common-actions.json'
STEM='f20-two-reconstructed-krw-grade-actions'

def checked_data():
    d=json.loads(DATA.read_text());n=d['n'];M=n*(n-1)//2
    assert n==97 and M==d['M']==4656 and d['directional_weights']=={'race':'1/2','gender':'1/2'}
    checks=[]
    for r in d['rows']:
        s=r['grade_sizes_highest_first'];b=[0]
        for size in s:b.append(b[-1]+size)
        N=sum(s[i]*s[j] for i in range(len(s)) for j in range(i+1,len(s)));H=sum(v*(v-1)//2 for v in s)
        assert b==r['cumulative_firm_boundaries'] and b[-1]==n
        assert len(s)==r['occupied_grades']<=r['grade_cap']==4 and N==r['disclosed_pairs'] and H==r['withheld_pairs'] and N+H==M
        dr,dg=(F(r['coefficient_error_sums'][k]) for k in ('race','gender'))
        metrics={'disclosure':F(N,M),'wrong_race':dr/N,'wrong_gender':dg/N,'normalized_risk':((dr+dg)/2+F(r['tau'])*H)/M}
        assert str(metrics['disclosure'])==r['disclosure_fraction']
        for key,v in metrics.items():assert format(float(v),'.4f' if key=='normalized_risk' else '.3f')==r['printed_metrics'][key]
        checks.append({'action_id':r['action_id'],'sizes':s,'cumulative_boundaries':b,'N':N,'withheld':H,'M':M,'exact_derived_metrics':{k:str(v) for k,v in metrics.items()},'printed_metrics':r['printed_metrics'],'status':'PASS_exact_counts_and_finite_decimal_arithmetic'})
    assert [r['grade_sizes_highest_first'] for r in d['rows']]==[[6,90,1],[16,37,30,14]]
    return d,checks

def ribbon(ax,r,mobile=False):
    ax.set(xlim=(0,97),ylim=(-.45,1.45))
    ax.spines[['left','top','right']].set_visible(False);ax.spines['bottom'].set_position(('data',-.17))
    ax.set_yticks([]);ax.set_xticks([0,25,50,75,97]);ax.tick_params(axis='x',labelsize=13,pad=6,length=3)
    fills=[C['light'],'#D8E7E5','#BBD3D1','#A1C0BE'];records=[]
    sizes=r['grade_sizes_highest_first'];bound=r['cumulative_firm_boundaries']
    for j,(a,b,size) in enumerate(zip(bound[:-1],bound[1:],sizes)):
        ax.add_patch(Rectangle((a,0),b-a,.55,facecolor=fills[j],edgecolor=C['ink'],lw=1.2))
        if len(sizes)==3 and j!=1:
            anchor=0 if j==0 else 97;ha='left' if j==0 else 'right'
            label='Grade '+str(j+1)+': '+str(size)+(' firm' if size==1 else ' firms')
            ax.text(anchor,1.12,label,ha=ha,va='center',fontsize=13.5,fontweight='bold')
            ax.plot([(a+b)/2,(a+b)/2,anchor],[.57,.84,.99],color=C['muted'],lw=1,clip_on=False)
        else:
            label=('Grade '+str(j+1)+'\n'+str(size)+' firms') if len(sizes)==3 else ('G'+str(j+1)+'\n'+str(size))
            ax.text((a+b)/2,.275,label,ha='center',va='center',fontsize=14,fontweight='bold',linespacing=1.12)
        records.append({'grade':j+1,'firms':size,'left':a,'right':b,'width':b-a,'external_label':len(sizes)==3 and j!=1})
    return {'scale':[0,97],'highest_priority':'left; grade1','blocks':records,'one_firm_width_preserved':True}

def metrics(ax,r,mobile=False):
    ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');p=r['printed_metrics']
    labels=['Disclosed pairs N / M','Disclosure N / M','Race wrong fraction D_R / N','Gender wrong fraction D_G / N','Risk at this row’s τ']
    values=[f"{r['disclosed_pairs']:,} / 4,656",p['disclosure'],p['wrong_race'],p['wrong_gender'],p['normalized_risk']]
    if mobile:
        labels=['Disclosed pairs N / M','Disclosure N / M','Race wrong fraction','Gender wrong fraction','Risk at this row’s τ']
        for y,label,value in zip([.90,.70,.50,.30,.10],labels,values):
            ax.text(.0,y,label,ha='left',va='center',fontsize=13.5)
            ax.text(1,y,value,ha='right',va='center',fontsize=14,fontweight='bold')
            if y>.11:ax.axhline(y-.10,color=C['line'],lw=.6)
    else:
        labels=['Disclosed pairs\nN / M','Disclosure\nN / M','Race wrong fraction\nD_R / N','Gender wrong fraction\nD_G / N','Risk at this\nrow’s τ']
        for j,(label,value) in enumerate(zip(labels,values)):
            x=.10+j*.20;ax.text(x,.80,label,ha='center',va='center',fontsize=12.5,linespacing=1.15)
            ax.text(x,.28,value,ha='center',va='center',fontsize=15,fontweight='bold')
            if j:ax.axvline(j*.20,color=C['line'],lw=.8,ymin=.12,ymax=.94)
    return {'labels':labels,'values':values,'wrong_fraction_denominator':'N','risk_denominator':'M=4656','risk_tau':r['tau']}

def geometry(fig):
    fig.canvas.draw();ren=fig.canvas.get_renderer();texts=list(fig.texts)
    for ax in fig.axes:texts+=list(ax.texts)
    for t in texts:
        b=t.get_window_extent(ren)
        if not(b.x0>=1 and b.x1<=fig.bbox.width-1 and b.y0>=1 and b.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
    for i,t in enumerate(texts):
        for u in texts[i+1:]:
            if t.get_window_extent(ren).overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
    return {'explicit_text_records':len(texts),'canvas_containment':'PASS','explicit_text_pairwise_nonoverlap':'PASS','axis_ticks':'0,25,50,75,97; personally inspect labels after export'}

def draw(d,mobile=False):
    rows=d['rows'];layout=[]
    if mobile:
        fig=fs.canvas(4.8,17.5,True)
        fig.text(.06,.98,'Two reconstructed\ncommon grade actions',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.06,.925,'97 firms; equal race/gender weights.\nSigned-target coefficients; highest\npriority at left. Width = firm count.',ha='left',va='top',fontsize=13,linespacing=1.3)
        titleys=[.85,.465];ribys=[.695,.31];metys=[.515,.13]
        for r,ty,ry,my in zip(rows,titleys,ribys,metys):
            fig.text(.06,ty,'τ = '+r['tau']+'  ('+r['tau_printed']+');  '+str(r['occupied_grades'])+' of at most 4 grades',ha='left',va='top',fontsize=13.5,fontweight='bold')
            rib=ribbon(fig.add_axes([.08,ry,.84,.125]),r,True)
            fig.text(.50,ry-.015,'Cumulative firm count',ha='center',va='top',fontsize=12.8)
            met=metrics(fig.add_axes([.06,my,.88,.15]),r,True);layout.append({'action':r['action_id'],'ribbon':rib,'metrics':met})
        fig.text(.06,.095,'Wrong fractions divide by disclosed pairs N.\nRisks use each row’s own withholding cost.',ha='left',va='top',fontsize=12.8,linespacing=1.3)
        fig.text(.06,.050,'Historical coefficient convention.\nCommon actions are an analyst extension.\nDifferent costs: no common-loss ranking,\nfrontier or optimality certificate.',ha='left',va='top',fontsize=12.4,linespacing=1.3)
    else:
        fig=fs.canvas(10.8,9.4)
        fig.text(.05,.97,'Two reconstructed common grade actions',ha='left',va='top',fontsize=17,fontweight='bold')
        fig.text(.05,.92,'97 firms; equal race/gender directional weights; signed-target coefficients.\nHighest priority at left; grade width is firm count.',ha='left',va='top',fontsize=12.8,linespacing=1.3)
        titleys=[.835,.47];ribys=[.665,.30];metys=[.515,.15]
        for r,ty,ry,my in zip(rows,titleys,ribys,metys):
            fig.text(.05,ty,'τ = '+r['tau']+'  ('+r['tau_printed']+');  '+str(r['occupied_grades'])+' of at most 4 grades',ha='left',va='top',fontsize=14,fontweight='bold')
            rib=ribbon(fig.add_axes([.08,ry,.84,.145]),r)
            fig.text(.5,ry-.019,'Cumulative firm count',ha='center',va='top',fontsize=12)
            met=metrics(fig.add_axes([.05,my,.90,.09]),r);layout.append({'action':r['action_id'],'ribbon':rib,'metrics':met})
        fig.text(.05,.105,'Wrong fractions use disclosed pairs N; risk uses M = 4,656 and the row’s own withholding cost.\nHistorical coefficient convention; common actions are an analyst extension of KRW’s scalar cards.\nDifferent costs do not establish a common-loss improvement, a frontier or an optimality certificate.',ha='left',va='top',fontsize=12,linespacing=1.3)
    return fig,{'rows':layout,'geometry':geometry(fig)}

def main(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F20.json';old=json.loads(dest.read_text()) if dest.exists() else None
    targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite only for an observed authorized repair.')
    d,checks=checked_data();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    attempt={'started_at_utc':now,'status':'running','command':'python3 -B assets/reproduction/figures/generators/F20/generate.py'+(' --overwrite' if overwrite else ''),'layout_exports':0,'asset_writes':0}
    rec={'id':'F20','step':'6.13','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':(old or {}).get('execution_history',[])+[attempt],'actual_PNG_views':(old or {}).get('actual_PNG_views',0),'views':(old or {}).get('views',[]),'repairs':(old or {}).get('repairs',[]),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,DATA,BASE/'figstyle.py']],'exact_checks':checks,'scope':'Plotting and tiny exact aggregate arithmetic only. No raw pair arrays, firm identities, private scientific runtime inputs, historical program, optimizer, model or simulation. Optional prior own receipt is bookkeeping only.','publication_and_licenses':'Deferred'}
    rec['chapter_provenance_from_public_data']=d['source'];rec['chapter_runtime_read_count']=0
    if old:rec['previous_export_history']=old.get('previous_export_history',[])+[{'created_at_utc':old['created_at_utc'],'inputs':old['inputs'],'outputs':old.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(rec,indent=2)+'\n')
    try:
        outputs=[];layouts=[]
        for mobile in [False,True]:
            fig,layout=draw(d,mobile);layouts.append(layout);outputs+=fs.export(fig,STEM,mobile);rec['outputs']=outputs;attempt['layout_exports']+=1;attempt['asset_writes']+=3
        assert [r['ribbon'] for r in layouts[0]['rows']]==[r['ribbon'] for r in layouts[1]['rows']]
        rec['layouts']=layouts;rec['status']='rendered';attempt['status']='succeeded'
    except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);rec['status']='render_failed';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':outputs},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
