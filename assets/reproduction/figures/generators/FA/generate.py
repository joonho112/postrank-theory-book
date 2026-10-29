#!/usr/bin/env python3
"""FA: selected proof routes and the qualified half-cost refinement argument.

Public literal symbolic labels, public route module and frozen style suffice.
The uniform refinement law is a proof device, not a reporting policy.
"""
from pathlib import Path
import sys,json,hashlib,datetime,argparse,importlib.util
HERE=Path(__file__).resolve();BASE=HERE.parents[2];sys.path.insert(0,str(BASE))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch
ROUTE=BASE/'generators/FA-route/route_panel.py'
spec=importlib.util.spec_from_file_location('fa_public_route_panel',ROUTE)
route=importlib.util.module_from_spec(spec);spec.loader.exec_module(route)
ROOT=fs.ROOT;DEST=ROOT/'evidence/figures/builds/FA.json';STEM='proof-route-and-refinement'

def identity(p):return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}

def mechanism(fig,rect,mobile):
    ax=fs.diagram_axis(fig,rect);size=14 if mobile else 12.5
    nodes={};texts=[];edges=[]
    if mobile:
        positions={
          'premise':(.04,.875,.92,.105),
          'weak':(.04,.724,.92,.112),
          'neutral':(.04,.552,.92,.137),
          'average':(.04,.386,.92,.127),
          'lower':(.04,.281,.92,.071),
          'mean':(.04,.180,.92,.071),
          'conclusion':(.04,.103,.92,.047)}
    else:
        positions={
          'premise':(.03,.866,.94,.108),
          'weak':(.03,.650,.43,.170),
          'neutral':(.54,.650,.43,.170),
          'average':(.03,.427,.94,.171),
          'lower':(.03,.254,.43,.123),
          'mean':(.54,.254,.43,.123),
          'conclusion':(.20,.141,.60,.069)}
    labels={
      'premise':'One law, one loss and one family\n'+r'$g^*$'+' is an EXACT half-cost minimizer.\nEVERY required child is feasible.',
      'weak':'WEAK: full unit refinements\n'+r'$\bar e_{ij}+\bar e_{ji}=1$'+'\nFull unrestricted '+r'$\mathcal{A}_n$'+'\nAll strict unit-order children\n'+r'$q=M-N(g^*)$',
      'neutral':'NEUTRAL: full class refinements\n'+r'$c_{ij}+c_{ji}=\delta_{ij}$'+'\nFull active-profile equality classes\nAll class-strict children feasible\nOriginal unit-pair multiplicities\n'+r'$q=T-Q(g^*)$',
      'average':'Uniform average over ALL required children\nMean added error '+r'$=q/2$'+'\nHalf-cost withholding reduction '+r'$=q/2$'+'\n'+r'$\mathrm{Mean}\,R(r)=R(g^*)=R^*$',
      'lower':'Exact optimum + child feasibility\n'+r'$R(r)-R^*\geq 0$'+' for every child',
      'mean':'Uniform mean of all child gaps\n'+r'$\frac{1}{L}\sum_{\ell=1}^{L}[R(r_\ell)-R^*]=0$',
      'conclusion':'Every required child: '+r'$R(r)=R^*$'}
    # Explicit wraps retain14pt rather than shrink mathematical text on mobile.
    if mobile:
      labels['premise']='One law, one loss and one family\n'+r'$g^*$'+' is an EXACT minimizer\nat '+r'$\tau=1/2$'+'. EVERY required\nchild is feasible.'
      labels['average']='Uniform average over\nALL required children\nMean added error '+r'$=q/2$'+'\nWithholding reduction '+r'$=q/2$'+'\n'+r'$\mathrm{Mean}\,R(r)=R(g^*)=R^*$'
      labels['lower']='Exact optimum + child feasibility\n'+r'$R(r)-R^*\geq 0$'+' for every child'
      labels['mean']='Uniform mean of all child gaps\n'+r'$\frac{1}{L}\sum_{\ell=1}^{L}[R(r_\ell)-R^*]=0$'
    for key,(x,y,w,h) in positions.items():
      p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.003,rounding_size=0.008',
        facecolor=fs.PALETTE['light'] if key in ['premise','conclusion'] else 'white',
        edgecolor=fs.PALETTE['ochre'] if key in ['weak','neutral'] else fs.PALETTE['line'],linewidth=1.2,zorder=2)
      ax.add_patch(p);nodes[key]=p
      t=ax.text(x+w/2,y+h/2,labels[key],ha='center',va='center',fontsize=size,
        fontweight='semibold' if key in ['premise','conclusion'] else 'normal',linespacing=1.22,zorder=5);texts.append((key,t))
    def center(key):
      x,y,w,h=positions[key];return x+w/2,y+h/2
    def edge(a,b):
      fs.arrow(ax,center(a),center(b),patchA=nodes[a],patchB=nodes[b]);edges.append({'source':a,'target':b})
    if mobile:
      # Separate neutral premise: not a consequence of weak complementarity.
      edge('premise','weak');x,y,w,h=positions['premise'];xx,yy,ww,hh=positions['neutral']
      ax.plot([x,.014,.014,xx-.008],[y+h/2,y+h/2,yy+hh/2,yy+hh/2],color=fs.PALETTE['muted'],lw=1.2,zorder=1)
      fs.arrow(ax,(.014,yy+hh/2),(xx,yy+hh/2),patchB=nodes['neutral']);edges.append({'source':'premise','target':'neutral','routing':'left margin'})
      # Both premise cards supply their own q to the same algebra, via two spines.
      x,y,w,h=positions['weak'];xx,yy,ww,hh=positions['average']
      ax.plot([x+w,.985,.985,xx+ww+.008],[y+h/2,y+h/2,yy+hh/2,yy+hh/2],color=fs.PALETTE['muted'],lw=1.2,zorder=1)
      fs.arrow(ax,(.985,yy+hh/2),(xx+ww,yy+hh/2),patchB=nodes['average']);edges.append({'source':'weak','target':'average','routing':'right margin'})
      edge('neutral','average')
      for a,b,spine in [('average','mean',.985),('lower','conclusion',.014)]:
        x,y,w,h=positions[a];xx,yy,ww,hh=positions[b]
        sx=x+w if spine>.5 else x;tx=xx+ww if spine>.5 else xx
        ax.plot([sx,spine,spine,tx+(.008 if spine>.5 else -.008)],
          [y+h/2,y+h/2,yy+hh/2,yy+hh/2],color=fs.PALETTE['muted'],lw=1.2,zorder=1)
        fs.arrow(ax,(spine,yy+hh/2),(tx,yy+hh/2),patchB=nodes[b])
        edges.append({'source':a,'target':b,'routing':'right margin' if spine>.5 else 'left margin'})
      edge('mean','conclusion')
    else:
      for a,b in [('premise','weak'),('premise','neutral'),('weak','average'),('neutral','average'),('premise','lower'),('average','mean'),('lower','conclusion'),('mean','conclusion')]:
        # The lower bound has its own premise, not the average-identity alone.
        if (a,b)==('premise','lower'):
          x,y,w,h=positions[a];xx,yy,ww,hh=positions[b]
          ax.plot([x,.013,.013,xx-.008],[y+h/2,y+h/2,yy+hh/2,yy+hh/2],color=fs.PALETTE['muted'],lw=1.2,zorder=1)
          fs.arrow(ax,(.013,yy+hh/2),(xx,yy+hh/2),patchB=nodes[b]);edges.append({'source':a,'target':b,'routing':'left margin'})
        else:edge(a,b)
    if mobile:
      endpoint='Endpoints: weak '+r'$N=M$'+'; neutral '+r'$Q=T$'+'.\nNeutral raw '+r'$N$'+' need not equal '+r'$M$'+'.\nGuarded '+r'$T=0$'+': one class, all-withhold;\npoint frontier; '+r'$Q/T$'+' undefined.'
      scope='Uniform averaging is a proof device.\nCaps, fixed orders or protections need\nseparate arguments. T11 is not this\nendpoint. No arbitrary refinement\nguarantee for an approximate optimizer.'
      y1=.065;y2=-.022
    else:
      endpoint='Endpoints: weak '+r'$N=M$'+'; neutral '+r'$Q=T$'+' (raw '+r'$N$'+' may stay below '+r'$M$'+').\nGuarded '+r'$T=0$'+': one class/all-withhold, point frontier; '+r'$Q/T$'+' undefined.'
      scope='Uniform averaging is a proof device, not a reporting policy. Caps, fixed orders, protections and T11\nneed separate arguments. No arbitrary-refinement guarantee for an approximate optimizer.'
      y1=.092;y2=.012
    for key,text,y in [('endpoints',endpoint,y1),('scope',scope,y2)]:
      t=ax.text(.5,y,text,ha='center',va='center',fontsize=size if mobile else 11.5,
        linespacing=1.22,color=fs.PALETTE['muted'],zorder=5);texts.append((key,t))
    fig.canvas.draw();ren=fig.canvas.get_renderer();checks=[]
    for key,t in texts:
      bb=t.get_window_extent(ren)
      if key in nodes:
        pb=nodes[key].get_window_extent(ren);ok=bb.x0>=pb.x0+2 and bb.x1<=pb.x1-2 and bb.y0>=pb.y0+2 and bb.y1<=pb.y1-2
        checks.append({'node':key,'font_pt':t.get_fontsize(),'text_inside_node':bool(ok)})
        if not ok:raise RuntimeError('Mechanism text outside node: '+key+' '+str(bb)+' vs '+str(pb))
      if not(bb.x0>=1 and bb.x1<=fig.bbox.width-1 and bb.y0>=1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Mechanism text outside canvas: '+key)
    for i,(key,t) in enumerate(texts):
      for key2,u in texts[i+1:]:
        if t.get_window_extent(ren).overlaps(u.get_window_extent(ren)):raise RuntimeError('Mechanism overlap: '+key+' / '+key2)
    return {'nodes':{k:{'rectangle':list(positions[k]),'label':labels[k]} for k in positions},'edges':edges,'text_geometry':checks,'all_text_inside_canvas':True,'all_text_pairwise_nonoverlap':True,
      'scope':'Symbolic proof: all required refinements, exact parent optimum, common family/law/loss. No numeric fixture, simulated child risks or theorem extension.'}

def main(overwrite=False):
    targets=[ROOT/'assets/figures'/(STEM+s+'.'+e) for s in ['', '-mobile'] for e in ['svg','pdf','png']]
    if not overwrite and (DEST.exists() or any(p.exists() for p in targets)):raise SystemExit('Existing outputs; --overwrite only for observed repair.')
    old=json.loads(DEST.read_text()) if DEST.exists() else {};now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    a={'started_at_utc':now,'command':'python -B assets/reproduction/figures/generators/FA/generate.py'+(' --overwrite' if overwrite else ''),'status':'running','asset_writes':0,'layout_exports':0}
    r={'id':'FA','step':'7.15','author':'JoonHo Lee (jlee296@ua.edu)','created_at_utc':now,'status':'RENDERING',
      'scope':'Original symbolic proof-route/half-cost diagram only. No numerical fixture, optimizer, package, model, simulation or proof-program execution.',
      'inputs':[identity(p) for p in [HERE,ROUTE,BASE/'figstyle.py']],
      'scientific_runtime_inputs':'Public literal symbolic labels, public route_panel.py and figstyle.py. Canonical QMD/contract/private staging/receipts are not required scientific inputs. Previous own receipt is optional history only.',
      'source_refs':['appendices/A-proofs.qmd selected proof guides','chapters/16-evaluation-frontiers.qmd weak full-refinement proof and prp-tie-aware-half-cost','chapters/11-multicriteria-loss.qmd risk and existence-only guard scopes'],
      'execution_history':old.get('execution_history',[])+[a],'views':old.get('views',[]),'repairs':old.get('repairs',[]),'publication_and_licenses':'Deferred'}
    try:
      outputs=[];layouts=[]
      for mobile in [False,True]:
        fig=fs.canvas(4.8 if mobile else 10.8,37 if mobile else 18.9,mobile)
        route_rect=(.025,.565,.95,.419) if mobile else (.025,.58,.95,.40)
        mechanism_rect=(.025,.060,.95,.480) if mobile else (.025,.035,.95,.50)
        layoutA=route.draw_route_panel(fig,route_rect,mobile)
        layoutB=mechanism(fig,mechanism_rect,mobile)
        fig.text(.04,.994,'A  Selected proof routes',ha='left',va='top',fontsize=15 if mobile else 15,fontweight='bold')
        fig.text(.04,.550 if mobile else .556,'B  Why every required refinement is optimal',ha='left',va='top',fontsize=14 if mobile else 15,fontweight='bold',wrap=True)
        # Check title width separately before any layout export.
        fig.canvas.draw();ren=fig.canvas.get_renderer()
        for t in fig.texts:
          bb=t.get_window_extent(ren)
          if bb.x1>fig.bbox.width-2:raise RuntimeError('Panel heading too wide: '+t.get_text())
        layouts.append({'mobile':mobile,'figure_inches':list(fig.get_size_inches()),'route_panel':layoutA,'mechanism_panel':layoutB})
        for ext in ['svg','pdf','png']:
          p=ROOT/'assets/figures'/(STEM+('-mobile' if mobile else '')+'.'+ext);p.parent.mkdir(parents=True,exist_ok=True)
          metadata={'Date':None,'Creator':'JoonHo Lee (jlee296@ua.edu)'} if ext=='svg' else {'CreationDate': None, 'ModDate': None, 'Creator': 'JoonHo Lee (jlee296@ua.edu)', 'Author': 'JoonHo Lee (jlee296@ua.edu)'} if ext=='pdf' else {'Author': 'JoonHo Lee (jlee296@ua.edu)', 'Software': 'Matplotlib'}
          fig.savefig(p,dpi=160,metadata=metadata);outputs.append(identity(p));a['asset_writes']+=1
        fs.plt.close(fig);a['layout_exports']+=1
      r.update(outputs=outputs,layouts=layouts,status='exported');a['status']='succeeded'
    except Exception as exc:a.update(status='failed',error=str(exc));r['status']='RENDER_FAILED';raise
    finally:
      a['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();hist=r['execution_history']
      r['actual_execution_summary']={'producer_commands':len(hist),'complete_commands':sum(x['status']=='succeeded' for x in hist),'failed_commands':sum(x['status']=='failed' for x in hist),'asset_writes':sum(x['asset_writes'] for x in hist),'layout_exports':sum(x['layout_exports'] for x in hist),'actual_author_PNG_views':len(r['views']),'scientific_runs':0}
      DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'id':'FA','outputs':r.get('outputs'),'execution':r['actual_execution_summary']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--overwrite',action='store_true');main(p.parse_args().overwrite)
