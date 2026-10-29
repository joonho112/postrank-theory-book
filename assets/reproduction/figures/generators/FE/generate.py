"""FE: public plotting dependencies, scoped checks and separate audit evidence."""
from pathlib import Path
import argparse,datetime,hashlib,json,sys
HERE=Path(__file__).resolve();BASE=HERE.parents[2]
sys.path.insert(0,str(BASE))
import figstyle as fs
ROOT=fs.ROOT;C=fs.PALETTE;STEM='fe-reproduce-one-figure'
STAGES=[('Public plotting\ninputs','Declared finite fixture\nor accepted results.\nKeep source scope.'),('Plot program\nand shared style','Declared dependencies.\nBounded input checks\nare explicit.'),('Desktop / mobile\nfigure assets','SVG / PDF / PNG.\nRetained originals keep\ntheir identities.'),('Quarto source\nand HTML','Image, caption, alt text.\nRender with scientific\nexecution disabled.')]
CHECKS=[('Check inputs','Source scope and\nexact-value readback.'),('Check assets','File identities and\nactual figure review.'),('Check HTML','Captions, alt text, resources\nand responsive display.')]

def geometry(fig,objects):
    fig.canvas.draw();ren=fig.canvas.get_renderer();texts=list(fig.texts)
    for ax in fig.axes:texts+=list(ax.texts)
    texts=[t for t in texts if t.get_text()]
    for t in texts:
        b=t.get_window_extent(ren);assert b.x0>=1 and b.x1<=fig.bbox.width-1 and b.y0>=1 and b.y1<=fig.bbox.height-1,('outside canvas',t.get_text())
    for i,t in enumerate(texts):
        for u in texts[i+1:]:assert not t.get_window_extent(ren).overlaps(u.get_window_extent(ren)),('overlap',t.get_text(),u.get_text())
    for patch,text in objects:
        p=patch.get_window_extent(ren);b=text.get_window_extent(ren);assert b.x0>=p.x0+2 and b.x1<=p.x1-2 and b.y0>=p.y0+2 and b.y1<=p.y1-2,('card containment',text.get_text())
    return {'visible_text_records':len(texts),'card_text_containment_checks':len(objects),'canvas_containment':True,'pairwise_text_nonoverlap':True,'quantitative_encoding':False}

def draw(mobile=False):
    objects=[];arrows=[]
    if mobile:
        fig=fs.canvas(4.8,26.5,True)
        fig.text(.055,.983,'Reproduce one\ndeclared figure',ha='left',va='top',fontsize=16,fontweight='bold',linespacing=1.2)
        fig.text(.055,.940,'Public dependencies, scoped checks\nand a separate execution record.',ha='left',va='top',fontsize=14,linespacing=1.25)
        ax=fs.diagram_axis(fig,[.05,.085,.90,.80]);ax.set(xlim=(-.02,1.02),ylim=(-.015,1.015))
        def card(y,h,title,body,fc='white'):
            p=fs.box(ax,0,y,1,h,'',fc=fc)
            a=ax.text(.035,y+h-.015,title,ha='left',va='top',fontsize=14.5,fontweight='bold',linespacing=1.15)
            b=ax.text(.035,y+.047 if h<=.10 else y+.092,body,ha='left',va='top',fontsize=14,linespacing=1.2)
            objects.extend([(p,a),(p,b)]);return p
        optional=card(.875,.10,'Optional upstream\nscientific recomputation','Separate declared program\n→ accepted saved results.\nA separately requested operation.',C['light'])
        ys=[.735,.595,.455,.315];ps=[]
        for y,(heading,body) in zip(ys,STAGES):ps.append(card(y,.10,heading,body))
        fs.arrow(ax,(.50,.875),(.50,.835),style='--',patchA=optional,patchB=ps[0]);arrows.append({'from':'optional scientific program','to':'public plotting inputs','kind':'optional upstream result, not a required run'})
        for i in range(3):
            fs.arrow(ax,(.50,ys[i]),(.50,ys[i+1]+.10),patchA=ps[i],patchB=ps[i+1]);arrows.append({'from':i,'to':i+1,'kind':'public dependency'})
        checks=card(.135,.14,'Separate checks\naccompany the route','Inputs: scope and exact values.\nAssets: identities and actual figures.\nHTML: captions, alt text, resources\nand responsive display.',C['light'])
        fs.arrow(ax,(.50,.315),(.50,.275),style='--',patchA=ps[-1],patchB=checks);arrows.append({'from':'public route','to':'scoped checks','kind':'check record; not scientific validation'})
        audit=card(.005,.09,'Separate audit evidence','Record commands, identities and views.\nPrivate audit records are not required\nscientific plotting inputs.',C['light'])
        fs.arrow(ax,(.50,.135),(.50,.095),style='--',patchA=checks,patchB=audit);arrows.append({'from':'scoped checks','to':'audit evidence','kind':'record only; no return dependency'})
        fig.text(.055,.069,'Solid arrows: public dependencies.\nDashed arrows: optional work or checks.\nA historical receipt is not a new run.\nNo complete portfolio replay is asserted.',ha='left',va='top',fontsize=14,linespacing=1.25)
    else:
        fig=fs.canvas(12.6,11)
        fig.text(.045,.98,'Reproduce one declared figure',ha='left',va='top',fontsize=18,fontweight='bold')
        fig.text(.045,.93,'A public dependency chain, with separate scientific recomputation, checks and audit records.',ha='left',va='top',fontsize=13.5)
        ax=fs.diagram_axis(fig,[.04,.12,.92,.74]);ax.set(xlim=(-.02,1.02),ylim=(-.015,1.015))
        optional=fs.box(ax,0,.81,.58,.14,'',fc=C['light'])
        a=ax.text(.025,.925,'Optional upstream scientific recomputation',ha='left',va='center',fontsize=14,fontweight='bold')
        b=ax.text(.025,.865,'Declared scientific program → accepted saved results.\nSeparate operation; plotting does not execute it.',ha='left',va='center',fontsize=13.5,linespacing=1.25);objects.extend([(optional,a),(optional,b)])
        xs=[0,.265,.53,.795];ps=[]
        for x,(heading,body) in zip(xs,STAGES):
            p=fs.box(ax,x,.535,.205,.215,'',fc='white');ps.append(p)
            a=ax.text(x+.1025,.705,heading,ha='center',va='center',fontsize=14,fontweight='bold',linespacing=1.15)
            b=ax.text(x+.1025,.605,body,ha='center',va='center',fontsize=13.2,linespacing=1.25);objects.extend([(p,a),(p,b)])
        fs.arrow(ax,(.1025,.81),(.1025,.75),style='--',patchA=optional,patchB=ps[0]);arrows.append({'from':'optional scientific program','to':'public plotting inputs','kind':'optional upstream result, not a required run'})
        for i in range(3):
            fs.arrow(ax,(xs[i]+.205,.6425),(xs[i+1],.6425),patchA=ps[i],patchB=ps[i+1]);arrows.append({'from':i,'to':i+1,'kind':'public dependency'})
        checks=[]
        for x,(heading,body) in zip([0,.355,.71],CHECKS):
            p=fs.box(ax,x,.29,.29,.17,'',fc=C['light']);checks.append(p)
            a=ax.text(x+.145,.42,heading,ha='center',va='center',fontsize=14,fontweight='bold')
            b=ax.text(x+.145,.35,body,ha='center',va='center',fontsize=13.5,linespacing=1.25);objects.extend([(p,a),(p,b)])
        for source,target,sx,tx in [(ps[0],checks[0],.1025,.145),(ps[2],checks[1],.6325,.50),(ps[3],checks[2],.8975,.855)]:
            fs.arrow(ax,(sx,.535),(tx,.46),style='--',patchA=source,patchB=target);arrows.append({'from':'public stage','to':'scoped check','kind':'check record; not scientific validation'})
        audit=fs.box(ax,0,.055,1,.15,'',fc=C['light'])
        a=ax.text(.025,.175,'Separate audit evidence',ha='left',va='center',fontsize=14,fontweight='bold')
        b=ax.text(.025,.108,'Record actual commands, input/output identities and actual views.\nPrivate audit records are not required scientific plotting inputs.',ha='left',va='center',fontsize=13.5,linespacing=1.25);objects.extend([(audit,a),(audit,b)])
        for p,x in zip(checks,[.145,.50,.855]):fs.arrow(ax,(x,.29),(x,.205),style='--',patchA=p,patchB=audit)
        arrows.extend([{'from':'scoped checks','to':'audit evidence','kind':'record only; no return dependency'}]*3)
        fig.text(.045,.082,'Solid arrows: public dependencies. Dashed arrows: optional operation, checks or records.\nA historical receipt is not a new run. This recipe does not assert a complete portfolio replay.',ha='left',va='top',fontsize=13.2,linespacing=1.3)
    return fig,{'stages':[{'heading':h.replace('\n',' '),'body':b.replace('\n',' ')} for h,b in STAGES],'arrows':arrows,'audit_is_required_scientific_input':False,'geometry':geometry(fig,objects)}

def main(overwrite=False):
    dest=ROOT/'evidence/figures/builds/FE.json';old=json.loads(dest.read_text()) if dest.exists() else None
    targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (dest.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite only for an observed authorized repair.')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();attempt={'started_at_utc':now,'status':'running','command':'python -B assets/reproduction/figures/generators/FE/generate.py'+(' --overwrite' if overwrite else ''),'asset_writes':0,'layout_exports':0}
    rec={'id':'FE','step':'7.13','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'rendering','execution_history':(old or {}).get('execution_history',[])+[attempt],'views':(old or {}).get('views',[]),'actual_PNG_views':(old or {}).get('actual_PNG_views',0),'repairs':(old or {}).get('repairs',[]),'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE,BASE/'figstyle.py']],'scientific_inputs':'Literal conceptual labels in public source plus public style only. No numeric fixture, canonical chapter or private scientific input. Optional previous own receipt supplies bookkeeping only.','scope':'Render a reproducibility recipe, not a scientific, package, archive, solver, simulation or full figure-portfolio replay. No private paths are plotted.','publication_and_licenses':'Deferred'}
    if old:rec['previous_export_history']=old.get('previous_export_history',[])+[{'created_at_utc':old['created_at_utc'],'inputs':old['inputs'],'outputs':old.get('outputs',[])}]
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(rec,indent=2)+'\n')
    try:
        outputs=[];layouts=[]
        for mobile in [False,True]:
            fig,layout=draw(mobile);layouts.append(layout);outputs+=fs.export(fig,STEM,mobile);rec['outputs']=outputs;attempt['layout_exports']+=1;attempt['asset_writes']+=3
        assert layouts[0]['stages']==layouts[1]['stages'];rec['layouts']=layouts;attempt['status']='succeeded';rec['status']='rendered'
    except Exception as exc:attempt['status']='failed';attempt['error']=str(exc);rec['status']='render_failed';raise
    finally:
        attempt['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'receipt':str(dest.relative_to(ROOT)),'outputs':rec['outputs']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
