"""Reusable conceptual proof-route panel; literal public labels, no data runs.

Each arrow names an actual selected prerequisite route. Guard existence is
shown separately from the stronger domain needed for half-cost refinement.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import figstyle as fs
from matplotlib.patches import FancyBboxPatch


def draw_route_panel(fig, rect=(.025,.035,.95,.93), mobile=False):
    ax=fs.diagram_axis(fig,rect)
    size=14 if mobile else 12.5
    nodes={};text_records=[];edge_records=[]
    if mobile:
        positions={
            'common':(.04,.91,.92,.07),
            'weak':(.04,.75,.92,.105),
            'weak_compare':(.04,.60,.44,.105),'weak_hull':(.52,.60,.44,.105),
            'weak_half':(.04,.49,.92,.075),
            'neutral':(.04,.332,.92,.105),
            'guard':(.04,.177,.44,.115),'neutral_hull':(.52,.177,.44,.115),
            'neutral_half':(.04,.055,.92,.085)}
    else:
        positions={
            'common':(.03,.89,.94,.095),
            'weak':(.03,.64,.43,.18),'neutral':(.54,.64,.43,.18),
            'weak_compare':(.03,.35,.20,.20),'weak_hull':(.26,.35,.20,.20),
            'guard':(.54,.35,.20,.20),'neutral_hull':(.77,.35,.20,.20),
            'weak_half':(.03,.08,.43,.17),'neutral_half':(.54,.08,.43,.17)}
    labels={
      'common':'Target, law, loss, feasible family\nOriginal units and M',
      'weak':'Weak-error route\nEquality counts as wrong\n'+r'$R^s=[A^s+\tau(M-N)]/M$',
      'neutral':'Equality-neutral route\nStrict error + distinct withholding\n'+r'$R^s_{\mathrm{TA}}=[A^s_{\mathrm{TA}}+\tau(T-Q)]/M$',
      'weak_compare':'Own-risk optimum\nEligible competitors\nSame law and loss\nSame family',
      'weak_hull':'Count hull\n(N, A)\nFixed family\nWhole reports',
      'guard':'Guarded minimizer\nexists\nFull at-most G\nNo extras\nRetain pairs\nExistence only',
      'neutral_hull':'Distinct-mass\nhull (Q, A)\nFixed family\nWhole reports',
      'weak_half':'Extra for half cost:\ncomplementarity; full '+r'$\mathcal{A}_n$'+'\nall strict children feasible',
      'neutral_half':'Extra for half cost:\nfull-profile class domain\nall class-strict children feasible\nnot guard existence alone'}
    for key,(x,y,w,h) in positions.items():
        patch=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.003,rounding_size=0.008',
            facecolor=fs.PALETTE['light'] if key=='common' else 'white',
            edgecolor=fs.PALETTE['ochre'] if key.endswith('half') else fs.PALETTE['line'],linewidth=1.2,zorder=2)
        ax.add_patch(patch);nodes[key]=patch
        t=ax.text(x+w/2,y+h/2,labels[key],ha='center',va='center',fontsize=size,
            fontweight='semibold' if key=='common' else 'normal',linespacing=1.22,zorder=4)
        text_records.append((key,t))
    def center(key):
        x,y,w,h=positions[key];return x+w/2,y+h/2
    def edge(source,target):
        fs.arrow(ax,center(source),center(target),patchA=nodes[source],patchB=nodes[target])
        edge_records.append({'source':source,'target':target})
    edge('common','weak')
    if mobile:
        # Neutral shares the declaration directly; it is not derived from weak loss.
        x,y,w,h=positions['common'];xx,yy,ww,hh=positions['neutral']
        ax.plot([x,.014,.014,xx-.008],[y+h/2,y+h/2,yy+hh/2,yy+hh/2],color=fs.PALETTE['muted'],lw=1.2,zorder=1)
        fs.arrow(ax,(.014,yy+hh/2),(xx,yy+hh/2),patchB=nodes['neutral'])
        edge_records.append({'source':'common','target':'neutral','routing':'left side, avoids weak-route nodes'})
    else:edge('common','neutral')
    for source,target in [('weak','weak_compare'),('weak','weak_hull'),('neutral','guard'),('neutral','neutral_hull'),('weak_hull','weak_half'),('neutral_hull','neutral_half')]:edge(source,target)
    footer='Selected routes, not a complete proof graph.\nNo criterion independence is assumed.' if mobile else 'Selected prerequisites only; finite-sum risk needs no criterion independence.'
    t=ax.text(.5,.020,footer,ha='center',va='center',fontsize=14 if mobile else 11.5,color=fs.PALETTE['muted'],linespacing=1.2,zorder=4);text_records.append(('scope footer',t))
    fig.canvas.draw();ren=fig.canvas.get_renderer();geometry=[]
    for key,t in text_records:
        bb=t.get_window_extent(ren)
        if key in nodes:
            pb=nodes[key].get_window_extent(ren)
            inside=bb.x0>=pb.x0+2 and bb.x1<=pb.x1-2 and bb.y0>=pb.y0+2 and bb.y1<=pb.y1-2
            geometry.append({'node':key,'font_pt':t.get_fontsize(),'text_inside_node':bool(inside)})
            if not inside:raise RuntimeError('Text outside node: '+key+' '+str(bb)+' vs '+str(pb))
        if not(bb.x0>=1 and bb.x1<=fig.bbox.width-1 and bb.y0>=1 and bb.y1<=fig.bbox.height-1):raise RuntimeError('Text outside canvas: '+t.get_text())
    overlaps=[]
    for i,(key,t) in enumerate(text_records):
        for key2,u in text_records[i+1:]:
            if t.get_window_extent(ren).overlaps(u.get_window_extent(ren)):overlaps.append((key,key2))
    if overlaps:raise RuntimeError('Text overlaps: '+str(overlaps))
    return {'mobile':mobile,'nodes':{k:{'rectangle':list(positions[k]),'label':labels[k]} for k in positions},
            'edges':edge_records,'text_geometry':geometry,'all_text_inside_canvas':True,
            'all_text_pairwise_nonoverlap':True,'guard_has_no_edge_to_half_cost_node':True,
            'scope':'Selected symbolic prerequisite routes. No numerical fixture, independent criterion assumption or theorem derived solely from graph order.'}
