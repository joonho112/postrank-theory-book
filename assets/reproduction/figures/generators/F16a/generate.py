"""Mobile companion to the retained original F16a SVG.

Only public saved exact coordinates are read. No hull, report enumeration,
Monte Carlo or original R plotting program is run. The desktop SVG is immutable.
"""
from pathlib import Path
import sys, json, hashlib
from fractions import Fraction as Q
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import figstyle as fs
from matplotlib.lines import Line2D

ROOT = fs.ROOT
DATA = ROOT / 'assets/reproduction/figures/data/f16a-frontier.json'
DESKTOP = ROOT / 'assets/figures/matched-disclosure-frontier.svg'
RECEIPT = ROOT / 'evidence/figures/builds/F16a-mobile.json'
STEM = 'matched-disclosure-frontier'
P = fs.PALETTE

def identity(path):
    return {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

def values(vertices):
    return ([float(Q(str(v[0]))) for v in vertices], [float(Q(str(v[1]))) for v in vertices])

def check(data):
    f = data['families']
    assert f['unrestricted']['vertices'] == [[0,'0'],[3,'3/10'],[5,'13/20'],[6,'21/20']]
    assert f['order_DCBA']['vertices'] == [[0,'0'],[5,'81/20'],[6,'99/20']]
    assert f['sparse_endpoints']['vertices'] == [[0,'0'],[6,'21/20']]
    assert len(data['gray_distinct_coordinates']) == 55
    assert sum(z['source_reports_at_coordinate'] for z in data['gray_distinct_coordinates']) == 75
    assert (Q(3,10)+Q(13,20))/2 == Q(19,40)
    assert (Q(3)+Q(5))/2 == 4
    assert Q(21,20)*Q(5,6) == Q(7,8)
    assert Q(7,8)-Q(13,20) == Q(9,40)
    return {'copied_vertex_lists': True, 'distinct_gray_coordinates': 55, 'source_reports_represented': 75,
            'mixture_mean_N': '4', 'mixture_mean_A': '19/40', 'sparse_N5_gap': '9/40',
            'scientific_enumeration_or_hull_runs': 0}

def render(data):
    fig = fs.canvas(4.8, 20.5, mobile=True)
    texts = []
    def text(x,y,s,**kw):
        obj = fig.text(x,y,s,fontsize=14,ha='left',va='top',linespacing=1.22,**kw)
        texts.append(obj); return obj
    def key(y,label,color,style='-',marker='o'):
        fig.add_artist(Line2D([.065,.165],[y-.004,y-.004],transform=fig.transFigure,color=color,linestyle=style,marker=marker,markersize=4,linewidth=2))
        text(.195,y,label)
    text(.06,.98,'Matched disclosure: one exact law',fontweight='bold')
    text(.06,.958,'Four units; six unordered pairs.\nAxes show expected raw counts.')
    text(.06,.911,'A. Same law, different report families',fontweight='bold')
    text(.06,.891,'Full vertical scale: A = 0 to 5')
    left = fig.add_axes([.245,.673,.705,.194])
    gray = data['gray_distinct_coordinates']
    left.scatter([z['N'] for z in gray],[float(Q(z['A'])) for z in gray],s=18,color='#B7C2C6',zorder=2)
    for name,col,style in [('unrestricted',P['teal'],'-'),('order_DCBA',P['rust'],'--')]:
        x,y=values(data['families'][name]['vertices']);left.plot(x,y,color=col,linestyle=style,marker='o',markersize=4,linewidth=2,zorder=3)
    left.set(xlim=(-.15,6.15),ylim=(-.12,5.12),xticks=range(7),yticks=range(6))
    key(.632,'Exact frontier: all 75 reports',P['teal'])
    key(.610,'Imposed reverse order DCBA',P['rust'],'--')
    text(.06,.585,'Grey points: 55 distinct coordinates\nfrom 75 reports; equal point sizes.',color=P['muted'])
    text(.06,.548,'B. Whole-report mixing and a sparse hull',fontweight='bold')
    text(.06,.528,'Enlarged vertical scale: A = 0 to 1.1')
    right = fig.add_axes([.245,.309,.705,.195])
    for name,col,style in [('unrestricted',P['teal'],'-'),('sparse_endpoints',P['ochre'],':')]:
        x,y=values(data['families'][name]['vertices']);right.plot(x,y,color=col,linestyle=style,marker='o',markersize=4,linewidth=2,zorder=3)
    right.scatter([4],[.7],color=P['ink'],marker='s',s=48,zorder=5)
    right.scatter([4],[float(Q(19,40))],color=P['ink'],marker='D',s=48,zorder=5)
    right.set(xlim=(-.15,6.15),ylim=(-.03,1.12),xticks=range(7),yticks=[0,.25,.5,.75,1])
    for ax in (left,right):
        fs.clean(ax);ax.tick_params(labelsize=14)
        ax.set_xlabel('Expected disclosed count, N',fontsize=14,labelpad=9)
        ax.set_ylabel('Expected weighted\nwrong-count, A',fontsize=14,labelpad=10)
    key(.268,'Exact frontier',P['teal'])
    key(.247,'Two-endpoint candidate hull',P['ochre'],':')
    fig.add_artist(Line2D([.10],[.219],transform=fig.transFigure,color=P['ink'],marker='s',linestyle='None',markersize=6))
    text(.195,.225,'Best deterministic report at N = 4:\nA = 7/10')
    fig.add_artist(Line2D([.10],[.183],transform=fig.transFigure,color=P['ink'],marker='D',linestyle='None',markersize=6))
    text(.195,.189,'Whole-report mixture at mean N = 4:\nmean A = 19/40')
    text(.06,.149,'Choose g = (1,1,1,2) or (1,2,2,3),\neach with probability 1/2, independently\nof the latent state. Do not mix pairs.')
    text(.06,.099,'At N = 5: sparse A = 7/8;\nexact A = 13/20; gap = 9/40.')
    text(.06,.064,'Panel vertical scales differ. The sparse\nhull omits feasible reports and lies\non or above this exact frontier.',color=P['muted'])
    text(.06,.018,'Fixed law: weights (3/5, 2/5); M = 6.',color=P['muted'])
    fig.canvas.draw();renderer=fig.canvas.get_renderer();canvas=fig.bbox
    all_text=texts+[ax.xaxis.label for ax in (left,right)]+[ax.yaxis.label for ax in (left,right)]
    all_text += [t for ax in (left,right) for t in ax.get_xticklabels()+ax.get_yticklabels() if t.get_visible()]
    bboxes=[t.get_window_extent(renderer) for t in all_text]
    failures=[]
    for t,b in zip(all_text,bboxes):
        if b.x0<0 or b.y0<0 or b.x1>canvas.width or b.y1>canvas.height:failures.append('canvas: '+t.get_text())
    for i in range(len(texts)):
        for j in range(i):
            if bboxes[i].overlaps(bboxes[j]):failures.append('text overlap: '+texts[i].get_text()+' / '+texts[j].get_text())
    for ax in (left,right):
        box=ax.get_window_extent(renderer)
        for t in texts:
            if box.overlaps(t.get_window_extent(renderer)): failures.append('figure text overlaps plot: '+t.get_text())
    assert not failures, '\n'.join(failures)
    checks={'mobile_width_inches':4.8,'mobile_height_inches':20.5,'minimum_font_pt':14,
            'core_font_css_px_at_332px':14*332/(4.8*72),'canvas_text_count':len(all_text),
            'figure_text_nonoverlap_count':len(texts),'canvas_containment':True,
            'figure_text_nonoverlap':True,'figure_text_plot_nonoverlap':True,
            'separate_y_limits':[list(left.get_ylim()),list(right.get_ylim())],
            'gray_point_sizes_equal':True}
    return fig,checks

if __name__ == '__main__':
    before=identity(DESKTOP);data=json.loads(DATA.read_text());numerical=check(data)
    fig,geometry=render(data)
    outputs=fs.export(fig,STEM,mobile=True)
    after=identity(DESKTOP);assert before==after
    receipt={'id':'F16a','scope':'Amendment Step6.20 mobile companion only; original desktop retained byte-for-byte.',
             'author':'JoonHo Lee (jlee296@ua.edu)',
             'timestamp_utc':datetime.now(timezone.utc).isoformat(),
             'input_files':[identity(DATA)],'generator':identity(Path(__file__)),
             'original_desktop_before':before,'original_desktop_after':after,'outputs':outputs,
             'numerical_checks':numerical,'geometry_checks':geometry,
             'execution':{'renderer_commands_this_attempt':1,'complete_layouts_this_attempt':1,'asset_writes_this_attempt':3,
                          'public_coordinate_readbacks_this_attempt':1,'hull_or_report_enumeration_runs':0},
             'views':[],'status':'rendered',
             'boundaries':['Original retention receipt F16a.json is untouched.','No new desktop PDF/PNG is implied.',
                           'Coordinates are saved exact plotting inputs, not a fresh scientific computation.',
                           'Expected raw counts; panel vertical scales differ; whole-report randomization only.']}
    RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
