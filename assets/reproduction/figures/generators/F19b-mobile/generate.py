"""F19b mobile companion: stack the two retained scientific contrasts.
The existing desktop SVG is an input identity check and is never overwritten.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();BASE=HERE.parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.ticker import PercentFormatter
ROOT=fs.ROOT;C=fs.PALETTE;DATA=BASE/'data/f19b-objective-contrast.json';STEM='objective-contrast'
DESKTOP=ROOT/'assets/figures/objective-contrast.svg'
DESKTOP_SHA='ee194ff6a01208da7569fe72e39b42fc2c93a48d2441372166d622a9edc010bd'

def checked_data():
    d=json.loads(DATA.read_text());assert d['n']==3 and d['K']==2 and d['M']==3
    assert d['units']==list('ABC') and d['w']==['3/5','2/5'] and d['a']==['3/4','1/4']
    states=[(r['theta'],F(r['probability'])) for r in d['states']];assert sum(p for _,p in states)==1
    assert all(row[0]==row[1] for theta,p in states for row in theta)
    a=list(map(F,d['a']));cs=[[sum(ak*v for ak,v in zip(a,row)) for row in theta] for theta,p in states]
    moments=[]
    for i,row in enumerate(d['allocation_singletons']):
        mean=sum(p*c[i] for (theta,p),c in zip(states,cs));top=sum(p for (theta,p),c in zip(states,cs) if c[i]==max(c))
        assert mean==F(row['expected_selected_value']) and top==F(row['probability_select_best']);moments.append({'unit':row['unit'],'mean':str(mean),'top_probability':str(top)})
    assert [r['mean'] for r in moments]==['6','4','3'] and [r['top_probability'] for r in moments]==['3/10','7/10','0']
    selected={'unrestricted':[[1,1,1],[2,1,2],[3,1,2]],'mean_order_ABC':[[1,1,1],[1,1,2],[1,2,3]]};vertices=[]
    for family,gs in selected.items():
        for g,coordinate in zip(gs,d['families'][family]['hull']):
            ds=[(i,j) for i in range(3) for j in range(3) if g[i]<g[j]]
            wrong=sum(p*sum(c[i]<=c[j] for i,j in ds) for (theta,p),c in zip(states,cs))
            assert len(ds)==coordinate[0] and wrong==F(coordinate[1]);vertices.append({'family':family,'g':g,'N':len(ds),'A':str(wrong)})
    l=d['added_AB_lottery'];assert l['report']==[1,1,2] and l['probabilities']==['1/2','1/2']
    assert F(l['expected_selected_value'])==(F(moments[0]['mean'])+F(moments[1]['mean']))/2==5
    assert F(l['probability_select_best'])==(F(moments[0]['top_probability'])+F(moments[1]['top_probability']))/2==F(1,2)
    assert hashlib.sha256(DESKTOP.read_bytes()).hexdigest()==DESKTOP_SHA
    return d,{'moments':moments,'selected_report_vertices':vertices,'lottery':{'value':'5','top_probability':'1/2'},'scope':'Selected exact state arithmetic only; inherited hulls not reconstructed,13-report enumeration not run.'}

def geometry(fig):
    fig.canvas.draw();ren=fig.canvas.get_renderer();texts=list(fig.texts)
    for ax in fig.axes:
        texts+=list(ax.texts)+[ax.xaxis.label,ax.yaxis.label]+ax.get_xticklabels()+ax.get_yticklabels()
    texts=[t for t in texts if t.get_text()]
    for t in texts:
        b=t.get_window_extent(ren)
        if not(b.x0>=1 and b.x1<=fig.bbox.width-1 and b.y0>=1 and b.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
    for i,t in enumerate(texts):
        for u in texts[i+1:]:
            if t.get_window_extent(ren).overlaps(u.get_window_extent(ren)):raise RuntimeError('Text overlap: '+t.get_text()+' / '+u.get_text())
    return {'text_records_including_axis_labels_and_ticks':len(texts),'canvas_containment':'PASS','pairwise_text_nonoverlap':'PASS','legend_personal_readback_required':True}

def draw(d):
    fig=fs.canvas(4.8,15,True)
    fig.text(.06,.982,'Three units,\ntwo objective contrasts',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
    fig.text(.06,.927,'One exact synthetic law; larger targets\nhave higher priority. No causal effect\nor empirical policy benefit is shown.',ha='left',va='top',fontsize=13,linespacing=1.3)
    fig.text(.06,.853,'A. Reporting under\none conditional law',ha='left',va='top',fontsize=14,fontweight='bold',linespacing=1.2)
    ax=fig.add_axes([.19,.545,.75,.255]);fs.clean(ax)
    for family,label,color,ls in [('unrestricted','All coherent reports',C['teal'],'-'),('mean_order_ABC','Mean-order reports',C['ochre'],'--')]:
        h=d['families'][family]['hull'];ax.plot([p[0] for p in h],[float(F(p[1])) for p in h],color=color,linestyle=ls,marker='o',markersize=6,lw=2,label=label)
    spec=d['panel_specs']['reporting'];ax.set(xlim=(-.06,3.06),ylim=(0,1.5),xticks=spec['x_ticks'],yticks=[float(F(v)) for v in spec['y_ticks']])
    ax.set_xlabel('Expected number of\ndisclosed pairs',fontsize=14,labelpad=8,linespacing=1.15);ax.set_ylabel('Expected wrong count',fontsize=14,labelpad=8)
    ax.legend(loc='upper left',bbox_to_anchor=(-.02,-.29),fontsize=13,frameon=False,handlelength=2.2,borderaxespad=0)
    fig.text(.06,.427,'Segments mix whole reports.\nN = 1 is not a deterministic report.',ha='left',va='top',fontsize=13,linespacing=1.3)
    fig.text(.06,.375,'B. A budget of one:\ndifferent objectives',ha='left',va='top',fontsize=14,fontweight='bold',linespacing=1.2)
    bx=fig.add_axes([.19,.112,.75,.215]);fs.clean(bx)
    for r in d['allocation_singletons']:
        x=float(F(r['expected_selected_value']));y=float(F(r['probability_select_best']))
        bx.scatter([x],[y],s=65,color=C['teal'],edgecolor=C['ink'],lw=.7,zorder=3)
        bx.annotate(r['unit'],(x,y),xytext=(0,9),textcoords='offset points',ha='center',va='bottom',fontsize=14,fontweight='bold')
    l=d['added_AB_lottery'];x=float(F(l['expected_selected_value']));y=float(F(l['probability_select_best']))
    bx.scatter([x],[y],marker='D',s=65,color=C['gray'],edgecolor=C['ink'],lw=.7,zorder=3)
    bx.annotate('A–B lottery',(x,y),xytext=(0,9),textcoords='offset points',ha='center',va='bottom',fontsize=12.7,fontweight='bold')
    spec=d['panel_specs']['allocation'];bx.set(xlim=tuple(float(F(v)) for v in spec['x_limits']),ylim=tuple(float(F(v)) for v in spec['y_limits']),xticks=spec['x_ticks'],yticks=[float(F(v)) for v in spec['y_ticks']]);bx.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
    bx.set_xlabel('Expected selected target value',fontsize=13.5,labelpad=8);bx.set_ylabel('Probability of selecting the best',fontsize=13.5,labelpad=8)
    fig.text(.06,.062,'Circles select one named unit.\nThe diamond adds an independent, uniform\nA–B selection lottery to report 112.\nA reported tie does not select a unit.',ha='left',va='top',fontsize=12.7,linespacing=1.3)
    return fig,{'reporting_hulls':d['families'],'reporting_limits':[0,1.5],'allocation_limits':d['panel_specs']['allocation'],'geometry':geometry(fig)}

def main(overwrite=False):
    dest=ROOT/'evidence/figures/builds/F19b-mobile.json';old=json.loads(dest.read_text()) if dest.exists() else None
    targets=[ROOT/'assets/figures'/(STEM+'-mobile.'+e) for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing mobile outputs; --overwrite only for an observed authorized repair.')
    d,checks=checked_data();now=datetime.datetime.now(datetime.timezone.utc).isoformat();attempt={'started_at_utc':now,'status':'running','command':'python3 -B assets/reproduction/figures/generators/F19b-mobile/generate.py'+(' --overwrite' if overwrite else ''),'asset_writes':0,'layout_exports':0}
    rec={'id':'F19b-mobile','parent_id':'F19b','step':'6.21','amendment':'FIG-AM005','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':(old or {}).get('execution_history',[])+[attempt],'actual_PNG_views':(old or {}).get('actual_PNG_views',0),'views':(old or {}).get('views',[]),'repairs':(old or {}).get('repairs',[]),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,DATA,BASE/'figstyle.py',DESKTOP]],'exact_checks':checks,'original_desktop_sha256_before':DESKTOP_SHA,'original_desktop_write_count':0,'scope':'Three mobile exports only, with exact selected state arithmetic. Public JSON/style/original SVG identity are runtime inputs; no private fixture, chapter, example or contract is needed. No original R source, enumeration, solver, simulation, model or package run.','publication_and_licenses':'Deferred'}
    if old:rec['previous_export_history']=old.get('previous_export_history',[])+[{'created_at_utc':old['created_at_utc'],'inputs':old['inputs'],'outputs':old.get('outputs',[])}]
    dest.write_text(json.dumps(rec,indent=2)+'\n')
    try:
        fig,layout=draw(d);rec['outputs']=fs.export(fig,STEM,True);rec['layout']=layout;attempt['layout_exports']=1;attempt['asset_writes']=3
        after=hashlib.sha256(DESKTOP.read_bytes()).hexdigest();assert after==DESKTOP_SHA;rec['original_desktop_sha256_after']=after;rec['status']='rendered';attempt['status']='succeeded'
    except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);rec['status']='render_failed';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':rec['outputs']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
