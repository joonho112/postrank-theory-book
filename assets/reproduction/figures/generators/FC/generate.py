"""FC: complementary evidence roles and the scope of their support."""
from pathlib import Path
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();BASE=HERE.parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;C=fs.PALETTE;STEM='fc-what-each-evidence-type-supports'
LANES=[('Inspected\nprimary passage','Documents a stated target,\nmethod or claim in the\ninspected edition.','Suitability for this problem;\na complete source-proof audit.'),('Local\nderivation','Stated conclusion under\nthe declared assumptions\nand supplied argument.','Transfer to another law,\nobjective or feasible family.'),('Exact\nfinite check','Arithmetic for the specified\nfinite law and the checked\nactions.','A general theorem,\nempirical prevalence\nor calibration.'),('File\nfingerprint','Exact inspected bytes\nor a pinned inventory.','Scientific argument,\nalgorithmic correctness\nor statistical calibration.'),('Dated\nexecution record','Output of the identified\nprogram, inputs and\nexecuted checks.','Unexecuted capabilities\nor fitted-model correctness.')]

def geometry(fig,objects):
    fig.canvas.draw();ren=fig.canvas.get_renderer();texts=list(fig.texts)
    for ax in fig.axes:texts+=list(ax.texts)
    texts=[t for t in texts if t.get_text()]
    for t in texts:
        b=t.get_window_extent(ren)
        assert b.x0>=1 and b.x1<=fig.bbox.width-1 and b.y0>=1 and b.y1<=fig.bbox.height-1,('text outside canvas',t.get_text())
    for i,t in enumerate(texts):
        for u in texts[i+1:]:assert not t.get_window_extent(ren).overlaps(u.get_window_extent(ren)),('overlap',t.get_text(),u.get_text())
    for patch,text in objects:
        p=patch.get_window_extent(ren);b=text.get_window_extent(ren);assert b.x0>=p.x0+2 and b.x1<=p.x1-2 and b.y0>=p.y0+2 and b.y1<=p.y1-2,('text outside evidence card',text.get_text())
    return {'explicit_texts':len(texts),'card_text_containment_checks':len(objects),'canvas_containment':True,'pairwise_nonoverlap':True,'quantitative_encoding':False}

def draw(mobile=False):
    objects=[]
    if mobile:
        fig=fs.canvas(4.8,24,True)
        fig.text(.055,.982,'What each evidence\ntype supports',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.055,.932,'Discovery locates sources.\nInspected primary passages\nsupport substantive attribution.',ha='left',va='top',fontsize=14,linespacing=1.25)
        ax=fs.diagram_axis(fig,[.05,.09,.90,.79]);ax.set(xlim=(-.02,1.02),ylim=(-.015,1.015))
        for i,(name,support,boundary) in enumerate(LANES):
            y=.82-i*.20;p=fs.box(ax,0,y,1,.17,'',fc=C['light'] if i%2==0 else 'white')
            items=[ax.text(.035,y+.162,name.replace('\n',' '),ha='left',va='top',fontsize=15,fontweight='bold'),ax.text(.035,y+.133,'Supports',ha='left',va='top',fontsize=14,fontweight='bold'),ax.text(.035,y+.113,support,ha='left',va='top',fontsize=14,linespacing=1.2),ax.text(.035,y+.065,'Does not establish',ha='left',va='top',fontsize=14,fontweight='bold'),ax.text(.035,y+.045,boundary,ha='left',va='top',fontsize=14,linespacing=1.2)]
            objects.extend((p,t) for t in items)
        fig.text(.055,.071,'Keep editions, assumptions, pinned inputs\nand actual execution dates attached.\nNo lane establishes unperformed\nempirical work.',ha='left',va='top',fontsize=14,linespacing=1.25)
    else:
        fig=fs.canvas(11.8,12.5)
        fig.text(.05,.98,'What each evidence type supports',ha='left',va='top',fontsize=18,fontweight='bold')
        fig.text(.05,.935,'Discovery locates sources; inspected primary passages support substantive attribution.',ha='left',va='top',fontsize=13.5)
        ax=fs.diagram_axis(fig,[.05,.12,.90,.75]);ax.set(xlim=(-.015,1.015),ylim=(-.02,1.02))
        for x,label in [(.025,'Evidence'),(.315,'Supports'),(.675,'Does not establish')]:ax.text(x,.985,label,ha='left',va='top',fontsize=14,fontweight='bold')
        for i,(name,support,boundary) in enumerate(LANES):
            y=.79-i*.185;p=fs.box(ax,0,y,1,.155,'',fc=C['light'] if i%2==0 else 'white')
            for x in [.285,.65]:ax.plot([x,x],[y+.015,y+.140],color=C['line'],lw=.8)
            items=[ax.text(.025,y+.0775,name,ha='left',va='center',fontsize=14,fontweight='bold',linespacing=1.2),ax.text(.315,y+.0775,support,ha='left',va='center',fontsize=13.5,linespacing=1.25),ax.text(.675,y+.0775,boundary,ha='left',va='center',fontsize=13.5,linespacing=1.25)]
            objects.extend((p,t) for t in items)
        fig.text(.05,.083,'Keep editions, assumptions, pinned inputs and actual execution dates attached.\nNo lane establishes unperformed empirical work.',ha='left',va='top',fontsize=13.5,linespacing=1.3)
    return fig,{'evidence_lanes':[{'evidence':n.replace('\n',' '),'supports':s.replace('\n',' '),'does_not_establish':b.replace('\n',' ')} for n,s,b in LANES],'geometry':geometry(fig,objects)}

def main(overwrite=False):
    dest=ROOT/'evidence/figures/builds/FC.json';old=json.loads(dest.read_text()) if dest.exists() else None
    targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite only for an observed authorized repair.')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();attempt={'started_at_utc':now,'status':'running','command':'python -B assets/reproduction/figures/generators/FC/generate.py'+(' --overwrite' if overwrite else ''),'asset_writes':0,'layout_exports':0}
    rec={'id':'FC','step':'7.11','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':(old or {}).get('execution_history',[])+[attempt],'views':(old or {}).get('views',[]),'actual_PNG_views':(old or {}).get('actual_PNG_views',0),'repairs':(old or {}).get('repairs',[]),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,BASE/'figstyle.py']],'scientific_inputs':'Literal conceptual lane labels in public source only. No numeric fixture, canonical chapter or private scientific runtime input. Optional previous own receipt supplies bookkeeping only.','scope':'Original conceptual figure rendering only; no new theorem, source-paper audit, numerical experiment, package, optimizer, simulation or empirical analysis.','publication_and_licenses':'Deferred'}
    if old:rec['previous_export_history']=old.get('previous_export_history',[])+[{'created_at_utc':old['created_at_utc'],'inputs':old['inputs'],'outputs':old.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(rec,indent=2)+'\n')
    try:
        outputs=[];layouts=[]
        for mobile in [False,True]:
            fig,layout=draw(mobile);layouts.append(layout);outputs+=fs.export(fig,STEM,mobile);rec['outputs']=outputs;attempt['layout_exports']+=1;attempt['asset_writes']+=3
        assert layouts[0]['evidence_lanes']==layouts[1]['evidence_lanes'];rec['layouts']=layouts;attempt['status']='succeeded';rec['status']='rendered'
    except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);rec['status']='render_failed';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':rec['outputs']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
